"""The shop starts with the template's settings: storefront, search, and management interface respond."""

import re

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

PAGES = ["/", "/search/?q=x", "/livesearch/?q=x", "/contact", "/cart/", "/robots.txt", "/sitemap.xml", "/login/"]


@pytest.fixture
def shop(db):
    call_command("lfs_init")


@pytest.mark.parametrize("url", PAGES)
def test_storefront_page_responds(client, shop, url):
    assert client.get(url, follow=True).status_code == 200


def test_management_interface_responds_for_a_superuser(client, shop):
    client.force_login(get_user_model().objects.create_superuser("admin", "admin@example.com", "x"))
    assert client.get("/manage/dashboard/").status_code == 200


def test_storefront_shows_no_cookie_banner_without_tracking(client, shop):
    """The template sets only necessary cookies, so it must not ask for a consent it has no use for."""
    assert "lcc-cookie-banner" not in client.get("/").content.decode()


def test_mobile_menu_is_loaded_from_the_theme_urls(client, shop):
    """With the theme's URLs included, pages only name the mobile menu's URL, and that URL returns the menu."""
    from lfs.catalog.models import Category

    Category.objects.create(name="Garden", slug="garden")
    html = client.get("/").content.decode()

    src = re.search(r'<nav class="mobile-nav-sidebar"[^>]*data-src="([^"]+)"', html)
    assert src, "the page should name the URL of the mobile menu"
    menu = client.get(src.group(1).replace("&amp;", "&"))
    assert menu.status_code == 200 and "Garden" in menu.content.decode()
