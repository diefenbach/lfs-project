# LFS shop

A new online shop with [LFS](https://github.com/diefenbach/django-lfs) (django-lfs): a Django project with the
default theme and the standard add-ons, configured through environment variables.

## Quick start

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/diefenbach/lfs-project.git myshop && cd myshop
cp .env.example .env
uv sync
uv run --env-file .env python manage.py migrate
uv run --env-file .env python manage.py lfs_init
uv run --env-file .env python manage.py createsuperuser
uv run --env-file .env python manage.py runserver
```

Then open http://127.0.0.1:8000/ for the shop and http://127.0.0.1:8000/manage/dashboard/ to add categories, products, and
pages. Without `POSTGRES_DB` the shop uses SQLite (`db.sqlite3`).

## What is included

- **django-lfs** with the add-ons it needs: portlets, reviews, postal, contact form, order numbers, PayPal.
- **lfs-theme**, the default theme. Templates in `templates/` override it for your shop.
- **lfs-canonical** and **lfs-cookie-consent**.
- Optional extras: `uv sync --extra postgres` (PostgreSQL; the search then ignores accents), `--extra stripe`
  (card payments; also add `"lfs_stripe"` to `INSTALLED_APPS`), `--extra production` (gunicorn).

## Settings

Everything that differs between installations is an environment variable; `.env.example` lists them all. The LFS
settings themselves (price calculators, units, criteria, ...) are in `shop/settings.py`.

## Production

- Set `DJANGO_DEBUG=false`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, the
  `POSTGRES_*` and `EMAIL_*` variables, and your PayPal credentials.
- `uv sync --extra postgres --extra production`, then `python manage.py collectstatic`.
- Run `gunicorn shop.wsgi` behind a web server (nginx, Caddy) that terminates HTTPS, redirects HTTP to HTTPS, and
  serves `static/` and `media/`. Behind such a proxy set `DJANGO_BEHIND_PROXY=true`.

## Before django-lfs 1.0 is on PyPI

Until then the packages come from a local package folder:

```sh
UV_FIND_LINKS=/path/to/packages uv sync
```

When a package in that folder is rebuilt with the same version number, add `--reinstall --no-cache`, otherwise uv
keeps the copy it installed before.

## License

BSD (django-lfs, lfs-theme). The management interface bundles TinyMCE under GPL-2.0-or-later; see the django-lfs
README.
