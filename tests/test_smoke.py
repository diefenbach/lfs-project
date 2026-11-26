"""The shop starts with the template's settings: storefront, search, and management interface respond."""

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
