# Deployment & infrastructure notes

Running notes on infrastructure decisions and open follow-ups that don't
belong in code comments but shouldn't get lost between sessions either.

## Custom domain

`mathkg.com` and `www.mathkg.com` are attached in Railway, and DNS/TLS
are in place. The app allows those hosts plus
`mathkg-production.up.railway.app` by default. Requests to `www` or the
Railway hostname 301 to `https://mathkg.com` with the same path and
query.

No new Railway variables are required for that. Optional overrides
(Variables tab), if you ever need them:

```
SITE_URL=https://mathkg.com
EXTRA_ALLOWED_HOSTS=another.example
EXTRA_CSRF_TRUSTED_ORIGINS=https://another.example
```

`SITE_URL` is the origin used in canonical tags, the sitemap, robots.txt,
and email links. `EXTRA_ALLOWED_HOSTS` is a hostname with no scheme.
`EXTRA_CSRF_TRUSTED_ORIGINS` needs `https://`. Setting `ALLOWED_HOSTS`
or `CSRF_TRUSTED_ORIGINS` adds to the defaults; it does not remove
`mathkg.com`.

`django.contrib.sites` is not installed, so there is no Site row and no
data migration. `nixpacks.json` does not set a healthcheck path, and
there is no `railway.toml`. Railway's probe hostname, when you add a
path later, is `healthcheck.railway.app`. That host is allowed and is
not redirected (a 301 would fail the deploy).

After this ships, run `python manage.py seed_launch_news` in production
so the news page mentions the new address. See the search-engines
section below.

## PDF downloads (WeasyPrint)

Test PDFs (`/test-tuzuu/<id>/pdf/`) and the Big 4 worksheet PDF are
rendered by WeasyPrint when the request arrives. That import loads
Pango, GObject, HarfBuzz, and fontconfig with `dlopen`. Nix packages
in the old `nixpacks.json` `pkgs` list land in `/nix/store` and are not
on that search path, so production raised:

```
OSError: cannot load library 'libgobject-2.0-0': libgobject-2.0-0:
cannot open shared object file: No such file or directory
```

Django turned that into the plain “Server Error (500)” page. The same
code returns a PDF on a machine where those `.so` files are in the
system library path.

Railway’s current builder is Railpack, which does not read
`nixpacks.json`. Runtime packages belong in `railpack.json` under
`deploy.aptPackages` (keep the `"..."` entry so Railpack’s own packages
stay). `nixpacks.json` lists the same apt packages for an older
Nixpacks build. Do not switch them back to Nix `pkgs` names: cffi will
not find those libraries, and every PDF download will 500 again.
`fonts-dejavu-core` is the Kyrgyz-capable font the test PDF already
looks up at `/usr/share/fonts/truetype/dejavu/`.

No migration. No new Railway variable.

## Search engines (robots.txt and sitemap.xml)

`/robots.txt` and `/sitemap.xml` are Django views, not files under
`static/`. WhiteNoise and `collectstatic` do not serve them, and there
is no migration. They work on a fresh Railway container.

The sitemap lists:

- every public lesson page registered in the URL conf, including bridge
  pages generated from `apps/resources/data/bridge/pages/`
- every `Topic`, `Subtopic`, and `SubSubtopic` page
  (`/resources/topic/...`), via `get_absolute_url()`

It does not list `/login/`, `/register/`, `/resources/download/`,
account and password pages, or the staff dashboard. Resource files do
not have their own public HTML page; they appear on those topic pages.
The download URLs stay out of the sitemap.

Absolute URLs use ``SITE_URL`` (`https://mathkg.com`), including when the
file is fetched from another allowed host. `django.contrib.sites` is
**not** installed. Leave it off.

The live hosts are in `ALLOWED_HOSTS` (`config/settings/production.py`).
Production must keep `DJANGO_SETTINGS_MODULE=config.settings.production`
(that is what makes `DATABASE_URL` apply).

Submit this sitemap in Google Search Console and Yandex Webmaster:

```
https://mathkg.com/sitemap.xml
```

## Activation email (Brevo)

Railway blocks outbound SMTP, so `EMAIL_HOST` cannot deliver the
registration email (the request used to die with a 500). Mail now goes
through Brevo's HTTP API when this variable is set on the app service:

```
BREVO_API_KEY=<key from Brevo → SMTP & API → API keys>
```

Sender defaults to `MathKG <no-reply@mathkg.com>` (the mathkg.com domain
is authenticated in Brevo). Optional overrides, unset unless you need
them:

```
BREVO_SENDER_EMAIL=no-reply@mathkg.com
BREVO_SENDER_NAME=MathKG
DEFAULT_FROM_EMAIL=MathKG <no-reply@mathkg.com>
DEFAULT_REPLY_TO_EMAIL=mathematicskgz@gmail.com
```

`DEFAULT_FROM_EMAIL`, when set, is the whole From header and wins over
`BREVO_SENDER_EMAIL`. Reply-To defaults to the admin inbox
(`ADMIN_NOTIFICATION_EMAIL`, otherwise `mathematicskgz@gmail.com`)
because `no-reply@mathkg.com` has no mailbox. A failed or missing key
is logged; registration still succeeds. There is no migration for this.

If an older `DEFAULT_FROM_EMAIL` is still set to the Gmail address or
to `noreply@mathkg.com` (no hyphen), remove it or set it to
`MathKG <no-reply@mathkg.com>`. Before this change that variable was
ignored whenever `BREVO_API_KEY` was set, so a stale value would start
to take effect on the next deploy.

## Resource thumbnails auto-convert to WebP (2026-10-08)

`Resource.save()` now re-encodes any newly-uploaded `.image` (the
thumbnail shown on topic pages and the curated lesson-pack pages) as
lossless WebP before storing it — same pixels, but measured 40-60%
smaller than the PNG it replaces on real resource screenshots (73KB PNG
→ 28KB WebP in one real test, zero visible quality loss since it's
lossless). This is automatic: upload a PNG/JPEG through admin as normal,
it gets converted on save, `.image.name` ends up `...webp`. An image
that's already `.webp` is left alone (not re-converted on every save).
A corrupted/unreadable upload is logged and left unconverted rather than
blocking the save — the Resource still saves, it just keeps whatever was
uploaded.

Only applies to `Resource.image`, not `Resource.file` (the actual
downloadable pptx/pdf/etc., which obviously shouldn't be touched) or any
other model's image field (`Question.image`, `PaymentQRCode.image`).

## Persistent media storage (Cloudflare R2)

**Status: code is in, not yet activated.** `PaymentQRCode.image` is wired
to use S3-compatible object storage (`config/storage_backends.py`), but it
silently falls back to local disk until real credentials are set — which
means it doesn't persist across deploys yet.

To activate:
1. Cloudflare dashboard → R2 → create a bucket (e.g. `mathkg-media`).
2. Bucket → Settings → Public Access → enable it (gives a `pub-xxxx.r2.dev` URL).
3. R2 → Manage API Tokens → create one with Object Read & Write, scoped to the bucket.
4. Note the account's S3 endpoint: `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`.
5. Set on the Railway app service (Variables tab):
   ```
   AWS_ACCESS_KEY_ID=<from step 3>
   AWS_SECRET_ACCESS_KEY=<from step 3>
   AWS_STORAGE_BUCKET_NAME=mathkg-media
   AWS_S3_ENDPOINT_URL=https://<ACCOUNT_ID>.r2.cloudflarestorage.com
   AWS_S3_CUSTOM_DOMAIN=pub-xxxxxxxxxxxx.r2.dev
   ```
6. After it redeploys, re-enter the Finik payment link (or re-upload the
   QR image) in Django admin under "Төлөм QR коду" — it'll persist across
   every deploy after that.

Any S3-compatible provider works here (AWS S3, Backblaze B2, DigitalOcean
Spaces) — just different signup steps, same env vars.

## Resource files still on local disk (deliberately, for now)

The ~2073 existing resource files (`media/resources/...` — PPTX/PDF/images
for the 800 `Resource` rows) are git-tracked and load fine today. They are
**not** yet switched to R2, unlike `PaymentQRCode.image`.

Why: switching `Resource.file`/`Resource.image` to the S3 backend before
the actual file bytes exist in a bucket would break every existing
download — Django would look for them in R2, find nothing, and 404/error.

Once a bucket exists (see above), the real fix is two steps, in order:
1. Upload the existing `media/resources/` tree into the bucket (one-time
   migration — a script using `boto3` or the provider's CLI, run once
   credentials exist).
2. Only then add `storage=persistent_media_storage` to `Resource.file` and
   `Resource.image` in `apps/resources/models.py` (same pattern already
   used on `PaymentQRCode.image`), so any *new* resource uploaded via
   admin afterward also persists.

`/media/` is an allowlist (`config/media_views.py`), in development and
in production. Topic-page thumbnails (`resources/images/`) and the
subscribe QR (`payment_qr/`) are served from the local media directory.
Paid files (`resources/files/`, the older `downloads/` folder, and anything
else) are not: a direct link returns 404. Download buttons still go
through `download_resource_view`.

## Railway Volume shadows `/app/media` — caused a production incident (2026-10-06)

**Status: recovered, root cause still open.** `/app/media` in production is
a mounted Railway Volume (persistent disk), created around 2026-09-30. A
mounted volume completely shadows whatever the container image has baked
into that same path — so from that point on, the git-tracked
`media/resources/files/` and `media/resources/images/` content was
invisible to the running app, which saw only whatever was on the empty
volume instead. In practice this meant resource downloads were likely
broken for everyone from ~Sep 30 onward, not just for newly-added files —
it was only noticed when a newly-shipped lesson's download button showed
"Not found."

**How it was found:** `ls -la /app/media/` in a Railway shell showed a
`lost+found` directory — the tell-tale sign of an ext-family filesystem
freshly `mkfs`'d for a volume, not a path backed by the container image.

**Recovery performed:**
1. `git clone --depth 1` the repo into `/tmp` on the Railway container
   (outside the volume-shadowed path), to get the real git-tracked files
   back.
2. `cp -rn` (no-clobber) the recovered `media/resources/{files,images}/`
   trees into the volume-backed `/app/media/resources/...` paths.
3. Ran `python manage.py import_resources` to create the one missing
   `Resource` row for the newly-added lesson file.

**Secondary incident this caused:** step 3 above was a mistake run against
an already-populated database without first checking that `Resource.title`
values still matched their on-disk filenames. `import_resources`'s only
existence check is `Resource.objects.filter(title=filename).exists()` —
naive string matching with no fallback. Because a sizeable fraction of
production's resource titles had been hand-edited in Django admin at some
point (to show nicer, non-filename titles) and no longer matched their
literal filenames, the re-run treated ~1112 already-resourced files as
brand new, creating 1112 duplicate `Resource` rows and 1112 duplicate
files (Django's storage silently appends a random suffix on a filename
collision). This was diagnosed and cleaned up the same day: every
template and data file in the codebase was scanned for titles they
reference by exact string (244 total), cross-referenced against the
duplicates, and the 1111 confirmed-unreferenced duplicates were deleted
(DB rows + files). One duplicate was deliberately kept because
`directed_numbers.html` references that exact title and no other resource
with a matching title exists (a separate, pre-existing, still-open bug —
see below).

**Checked 2026-10-13, not actually a live bug:** `directed_numbers.html`
looks up a resource titled `4-amal-BagyttalganSandarJenilOrtoOor-Screenshot.png`
by exact title (`res|get_item:'...'`). Even when that lookup misses, the
template already falls back to a static file
(`{% if img and img.image %}...{% else %}{% static '...' %}{% endif %}`,
`directed_numbers.html:96`) which exists on disk and renders the real
screenshot — this is the established pattern for every "Screenshot"
resource on the site (none of them have `Resource.image` populated; they
all render from `static/img/`). A full scan of all 142 `get_item` lookups
across every template against the current database turned up only one
other miss (`Ekvivalenettuuluk_BOP_KatanyTap.pptx` in
`Bolchok_Onduk_Payiz.html`), which is guarded by `{% if r %}` and just
omits a download button rather than breaking visibly. `import_resources`'s
title-matching fragility (see above) is still worth hardening if it's
ever run again, but there's no known silent-miss currently live.

**Root cause, still open — two options, either works:**
1. Narrow the Railway Volume's mount path to only what actually needs
   persistent writes (e.g. `payment_qr/`), instead of all of `/app/media`,
   so git-tracked resource files are never shadowed again.
2. Finish the R2/S3 migration already scaffolded in `config/storage_backends.py`
   (see "Persistent media storage" above) for `Resource.file`/`Resource.image`
   — once resources live in a bucket instead of local disk, volume-shadowing
   stops being a risk for them entirely.

Either way, `import_resources` should also be made to not silently create
duplicates — e.g. matching on file content hash or on-disk path in addition
to title, or just retiring the command in favor of manual admin uploads
once persistent storage is in place.

## Copy missing resource files onto the volume after deploy

A file added under `media/resources/files/` in git is not visible to the
running app until it is copied onto the `/app/media` volume. The
`copy_missing_resource_files` command reads those paths from git and
writes a file only when that path is not already on the volume. A file
already there, including one uploaded in admin under the same name, is
left as it is. Nothing is deleted.

From a Railway shell, with the app virtualenv active
(`source /opt/venv/bin/activate` if `python` cannot import Django):

```
git clone --depth 1 https://github.com/Amanov/mathkg.git /tmp/mathkg-media
python manage.py copy_missing_resource_files --source /tmp/mathkg-media
```

Clone the revision that was just deployed. If this container still has
its own git history, the clone can be skipped:

```
python manage.py copy_missing_resource_files
```

`--dry-run` lists the files it would add and writes nothing. A volume
that already holds the library only receives files that are new in git.

Migrations `0026` and `0027` only wrote a path into the resource row.
They did not copy `amaldar_tartibi_ozun_tuz_v2.pptx` onto the volume,
which is why `/resources/download/603/` reports the file as unavailable.
Migration `0028` points `four_basic_operations` back at the v2 lesson,
pins that choice, and copies the bundled deck onto the volume when
that path is empty. It does not replace a file already there.
Run the command above after deploy, or in admin open the change page
whose URL ends in `/personal/resource/603/change/` and replace the
**File** field (not Image).

## Other open items from the full QA audit (2026-09-17)

Lower priority, not yet acted on:
- No admin notification when a new `SubscriptionRequest` comes in — relies
  on manually checking Django admin. Worth an email to the site owner, or
  at least a dashboard badge.
- The resource download button shows to any logged-in user regardless of
  subscription status; it only redirects with an error at click-time
  rather than showing the real state upfront.
- `static_cdn/` and `media_cdn/` (~2700 files, from the very first commit)
  are dead weight — unreferenced by any current setting. Safe to delete.
- `get_client_ip()` in `apps/resources/views/downloads.py` trusts a
  client-supplied `X-Forwarded-For` header without validating a trusted
  proxy chain. Low impact (only affects the IP logged against download
  analytics, not authentication), but worth tightening if that data is
  ever relied on for anything.
