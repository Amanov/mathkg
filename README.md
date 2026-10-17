# mathkg

Kyrgyz-language math materials site. Django 4.2, served on Railway.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

`manage.py` and `config/wsgi.py` default to `config.settings.development`: SQLite at `db.sqlite3`, `DEBUG` on, email printed to the console. Production (`config/settings/production.py`) refuses to start without `SECRET_KEY` and either `DATABASE_URL` or `SQLITE_PATH`. Set `DJANGO_SETTINGS_MODULE=config.settings.production` for that module. The container start command is in `nixpacks.json`.

Resource downloads read files from `MEDIA_ROOT` (`media/resources/files/`). A fresh checkout has the git-tracked library; production does not see new git files until they are copied onto the media volume. See [docs/deployment-notes.md](docs/deployment-notes.md).

PDF export (the Tarsia builder and other WeasyPrint views) needs the system libraries listed in `nixpacks.json` (`pango`, `harfbuzz`, `gdk-pixbuf`, `fontconfig`, and the related glib stack). PPTX export uses `python-pptx` from `requirements.txt` and does not need those libraries.

## Where to read next

| Topic | Doc |
|---|---|
| Topic-page layout, the one free file, download limits, missing-file fallbacks | [docs/topic-pages-and-downloads.md](docs/topic-pages-and-downloads.md) |
| Railway, media volume, R2, management commands in production | [docs/deployment-notes.md](docs/deployment-notes.md) |
| Tarsia triangle jigsaw and loop cards | [tools/tarsia/README.md](tools/tarsia/README.md) |
| Curriculum notes | [docs/curriculum-framework.md](docs/curriculum-framework.md) |

Tests: `python manage.py test`.
