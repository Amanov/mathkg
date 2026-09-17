# Deployment & infrastructure notes

Running notes on infrastructure decisions and open follow-ups that don't
belong in code comments but shouldn't get lost between sessions either.

## Custom domain

Not set up yet — the site runs on Railway's default
`mathkg-production.up.railway.app`. No action needed until you want one.

When you do: Railway supports custom domains on the **Trial plan**, no
upgrade required — you just need to own the domain and point its DNS at
Railway (Settings → Networking → Custom Domain on the app service).

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
