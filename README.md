# LFS shop

A new online shop with [LFS](https://github.com/diefenbach/django-lfs) (django-lfs): a Django project with the
default theme and the standard add-ons, configured through environment variables.

## Quick start

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/diefenbach/lfs-project.git myshop && cd myshop
cp .env.example .env
uv sync
uv run python manage.py migrate
uv run python manage.py lfs_init
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Then open http://127.0.0.1:8000/ for the shop and http://127.0.0.1:8000/manage/dashboard/ to add categories, products, and
pages. Without `POSTGRES_DB` the shop uses SQLite (`db.sqlite3`).

## What is included

- **django-lfs** with the add-ons it needs: portlets, reviews, postal, contact form, order numbers.
- **lfs-theme**, the default theme. Templates in `templates/` override it for your shop.
- **lfs-canonical**.
- Optional extras, combinable (`uv sync --extra paypal --extra gtm`):
  - `postgres`: PostgreSQL; the search then ignores accents.
  - `paypal`: PayPal. Add `"lfs_paypal"` to `INSTALLED_APPS` before running `lfs_init` and set `PAYPAL_*`.
  - `stripe`: card payments. Add `"lfs_stripe"` to `INSTALLED_APPS` and set `STRIPE_*`.
  - `consent`: the cookie consent banner, for tracking you add yourself. Add `"lfs_cookie_consent"` to
    `INSTALLED_APPS`; your scripts listen to its `lfs:consent-changed` event.
  - `gtm`: Google Tag Manager with Consent Mode, including the consent banner. Add `"lfs_cookie_consent"` and
    `"lfs_gtm"` to `INSTALLED_APPS` and set `GTM_ID`.
  - `bulk-prices`: price tiers by quantity. Add `"lfs_bulk_prices"` to `INSTALLED_APPS`, run `migrate`, and choose
    the price calculator "Bulk prices" for a product; it then gets a "Bulk prices" tab.
  - `production`: gunicorn.

Without tracking the shop sets only the cookies it needs to work (session, CSRF), so it shows no consent banner.

## Settings

Everything that differs between installations is an environment variable; `.env.example` lists them all. Locally
put them in `.env`: the settings read that file on every start (`manage.py`, `runserver`, gunicorn). Variables set in
the real environment (server, systemd, Docker) win over the file, so in production you can leave it out. The LFS
settings themselves (price calculators, units, criteria, ...) are in `shop/settings.py`.

## Production

- Set `DJANGO_DEBUG=false`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, the
  `POSTGRES_*` and `EMAIL_*` variables, and the credentials of your payment add-ons (`PAYPAL_*`, `STRIPE_*`).
  With `DJANGO_DEBUG` on and a public host in `DJANGO_ALLOWED_HOSTS` the shop refuses to start, so a `.env` copied
  from `.env.example` cannot switch on debug pages on the server.
- `uv sync --extra postgres --extra production`, then `python manage.py collectstatic` on every deployment: with
  `DJANGO_DEBUG=false` the static files get content-hashed names, so browsers never mix cached old files with new
  pages, and the web server can cache `static/` for a long time.
- Run `gunicorn shop.wsgi` behind a web server (nginx, Caddy) that terminates HTTPS, redirects HTTP to HTTPS, and
  serves `static/` and `media/`. Behind such a proxy set `DJANGO_BEHIND_PROXY=true`.

## License

BSD (django-lfs, lfs-theme). The management interface bundles TinyMCE under GPL-2.0-or-later; see the django-lfs
README.
