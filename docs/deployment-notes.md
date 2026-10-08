# Deployment & infrastructure notes

Running notes on infrastructure decisions and open follow-ups that don't
belong in code comments but shouldn't get lost between sessions either.

## Custom domain

Not set up yet — the site runs on Railway's default
`mathkg-production.up.railway.app`. No action needed until you want one.

When you do: Railway supports custom domains on the **Trial plan**, no
upgrade required — you just need to own the domain and point its DNS at
Railway (Settings → Networking → Custom Domain on the app service).

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

Doing this also fixes the standing bug where `resource.image.url` likely
404s in production today — nothing currently serves `/media/*` outside
`DEBUG` mode, so those thumbnails have probably been broken since launch,
separately from the persistence question. Downloads themselves still work
today regardless, since `download_resource_view` streams the file directly
rather than relying on that URL.

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

**Pre-existing bug surfaced by this, not yet fixed:** `directed_numbers.html`
looks up a resource titled `4-amal-BagyttalganSandarJenilOrtoOor-Screenshot.png`
by exact title (`res|get_item:'...'`), but before the above incident no
`Resource` had that exact title — meaning that image lookup was silently
returning nothing. It's unknown how many other pages/images have the same
silent-miss problem elsewhere in the catalog, since `import_resources`'s
title-matching can't tell "already imported, just renamed" apart from
"genuinely new."

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
