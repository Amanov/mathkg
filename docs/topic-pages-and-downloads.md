# Topic pages and downloads

How a lesson page finds its files, which file is free, and what `download_resource` checks before streaming bytes. Infrastructure (the Railway volume, copying git files onto it, R2) stays in [deployment-notes.md](deployment-notes.md).

## Pages on the topic-page layout

These views call `build_topic_page` (`apps/resources/topic_pages.py`) and render `templates/resources/topic_materials.html`.

| URL | Spec | `page_key` | `downloads_gated` |
|---|---|---|---|
| `/to-fractions/` | `TO_FRACTIONS` | `Ekvivalenettuuluk_Onduktardan_menen_Bolchoktor-` (the `file_prefix`; no explicit `page_key`) | `True` |
| `/four_basic_operations/` | `FOUR_BASIC_OPERATIONS` | `four_basic_operations` | `True` |
| `/calculator-fractions/` | `CALCULATOR_FRACTIONS` | `KalkulyatorKoldonuu_Bolchoktor-` (the `file_prefix`) | omitted, so `False` |

`page_key` is `page['page_key']` when set, otherwise `file_prefix`. An empty `file_prefix` (as on four basic operations) must keep an explicit `page_key`, or every such page would share the key `''`.

Older lesson templates (the `operation_block.html` pages and the hand-built `ekvivalenttuuluk/*.html` pages) look files up themselves with `res|get_item:'exact-title'`. They do not call `build_topic_page`. `operation_page_context` in `apps/resources/free_download.py` can annotate those section lists, and no view calls it, so those pages do not pick a free file.

## Page spec

A spec is a dict: `title`, `svg_dir`, `file_prefix`, `sections`, and optionally `images`, `page_key`, `downloads_gated`, `standard`, `teacher_resources`, `model_label`, `stages_label`.

Each section has `stage`, `title`, `title_en`, `when`, `summary`, `bloom` (a list of level names), and `items`. Each item has `title`, `note`, `svg`, `level`, and `files` as `(button label, filename)` pairs.

`level` must be one of `BLOOM_LEVELS` (`Эстеп калуу`, `Түшүнүү`, `Колдонуу`, `Талдоо`, `Баалоо`, `Жаратуу`). `build_topic_page` indexes that tuple for the ladder; an unknown level raises `ValueError`.

Files resolve through `get_active_resources()`, a dict of **active** `Resource` rows keyed by `Resource.title`. The lookup key is `file_prefix + filename`. A title that does not match that string exactly, or a row with `is_active=False`, produces no button. A missing file on a gated page still counts as locked, so the register/renew prompt stays.

Thumbnails: if `images[svg]` is set, the template uses that static path (designed PNGs). Otherwise it inlines `templates/<svg_dir>/<svg>.svg`.

`/to-fractions/` and `/four_basic_operations/` group sections as a 5E + 3C lesson. `/calculator-fractions/` groups by material type and sets `model_label` / `stages_label` because that skill is not taught as a 5E lesson. Items there still carry a Bloom `level`; the staircase reads it.

## One free file

`choose_free_resource(page_key, candidates)` stores one `PageFreeDownload` row per page (`apps/resources/models.py`, admin label "Free downloads").

- Candidates are the page's active resources, in spec order, de-duplicated by id.
- No candidates: returns `None`. No file is marked free.
- No row yet: picks `random.choice` and inserts it. A concurrent insert is caught and the winner is re-read.
- Later requests return the stored resource while it is still a candidate.
- The stored resource has left the candidate list and `pinned` is false: a new random candidate replaces it.
- `pinned` is true: that resource is returned even when it is not in the candidate list. Changing `resource` in admin sets `pinned` automatically (`PageFreeDownloadAdmin.save_model`). Clearing `pinned` in the list editor leaves the current choice in place until it drops out of the candidate list.

The template adds an "Акысыз" badge on the link whose resource id equals that choice. `is_free_resource` is true for that resource id on **any** download URL, not only on the page that chose it. `download_resource_view` lets that id through with no login, no active subscription, and no daily quota.

`/four_basic_operations/` is pinned to `amaldar_tartibi_ozun_tuz_v2.pptx` by migration `0028` (`repair_four_basic_free_file`). That repair copies the deck bundled at `apps/resources/bundled_files/` onto `MEDIA_ROOT` when the stored path is empty, and it does not replace a file already there.

## What the visitor sees

`downloads_gated: True` (`topic_materials.html`): a free link is shown to everyone. Other links are shown only when the visitor is logged in and `user.has_active_subscription`. Otherwise the row shows "Катталуу" or "Жазылууну жаңыртуу".

`downloads_gated` false (`/calculator-fractions/`): every resolved file is shown as a pill. For a logged-out visitor, only the free pill points at `download_resource`; the others point at registration. A logged-in visitor gets real download URLs even when the subscription has ended; the view then redirects to the account page with an error.

Hand-built templates that link `download_resource` directly show those buttons without this gate. The view still enforces it.

`has_active_subscription` is date-based: an explicit `subscription_end`, otherwise `date_joined` plus `trial_days` (default 7). It does not read `current_plan`.

## Download view

`download_resource_view` (`apps/resources/views/downloads.py`), URL `/resources/download/<pk>/`:

1. Load an **active** resource. An unknown or inactive id sends an anonymous visitor to login, then 404s.
2. If the resource is not a free download: require login, then `has_active_subscription`, then a remaining daily slot.
3. Open the file. Failure redirects to the account page and does not write a download row.
4. Write `ResourceDownload` (anonymous free downloads store a null user) and increment `Resource.download_count`.

Daily caps (`Account.daily_download_limit`, `DAILY_DOWNLOAD_LIMITS` in `apps/account/models.py`), per category (`presentation`, `worksheet`, `activity`):

| `current_plan` | Cap per category per day |
|---|---|
| empty (trial) or `3m` | 1 |
| `6m` | 5 |
| `1y` | unlimited |

The cap counts distinct resources downloaded today, not raw click events. A resource this user already downloaded today is allowed again and does not consume another slot. A free download is still written to `ResourceDownload`. When the visitor was logged in, that row is what lets the same user download the same resource again later the same day without spending a slot, including after the file is no longer the page's free one. An anonymous free download stores a null user, so it does not create that skip.

## Opening a missing file

`open_resource_file` (`apps/resources/resource_files.py`) tries, in order:

1. The path stored on `Resource.file`.
2. `MEDIA_ROOT/resources/files/<basename>` for the stored name and for `Resource.title`.
3. Exactly one Django collision sibling: `<stem>_<7 alphanumeric chars><ext>` in that same directory. Two or more siblings are not guessed.
4. A file of that basename shipped in `apps/resources/bundled_files/`. The only bundled file today is `amaldar_tartibi_ozun_tuz_v2.pptx`. It is copied onto `MEDIA_ROOT` when that path is empty; a copy error falls back to reading the bundled path.

A fallback that differs from the stored name is written back onto the row so admin's "Currently" link matches the file that was served. The search stays inside `resources/files/`. It does not invent a path.

After a deploy, git-tracked files under `media/resources/files/` are still hidden by the volume until `copy_missing_resource_files` copies the ones the volume lacks. That command never overwrites an existing file. The runbook is in [deployment-notes.md](deployment-notes.md).

## Pitfalls

- Buttons key off `Resource.title`, not the filename stored on `Resource.file`. Renaming a title in admin removes the button until the spec or the title matches again. `import_resources` has the same title check and will create duplicates when titles have been edited; see the 2026-10-06 note in the deployment doc.
- A new file in git is invisible in production until it is on the volume (or bundled and reached by `locate_resource_file`).
- Unpinning a free file does nothing while that resource is still one of the page's active files. Remove it from the spec, or point the row at another resource.
- A pinned resource that is inactive or absent from the spec produces no "Акысыз" button. Its id remains free at the download URL while the row points at it and the row is active.
- `Resource.image` uploads are re-encoded to lossless WebP on save. `Resource.file` is not. Details are in the deployment notes.
