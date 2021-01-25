from urllib.parse import urljoin

from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

import pytest

from app.common.enums import AdminGroup
from app.content.factories.user_factory import UserFactory
from app.content.models import Page

PAGE_PATH = "/api/v1/page/"
PAGE_POST_TEST_DATA = {
    "title": "foo",
    "content": "foobar",
}


@pytest.fixture()
def client():
    test_user = UserFactory(
        user_id="dev", password="123", first_name="member", last_name="user"
    )
    test_user.groups.add(Group.objects.create(name=AdminGroup.INDEX))
    token = Token.objects.get(user_id=test_user.user_id)
    client = APIClient()
    client.credentials(HTTP_X_CSRF_TOKEN=token)
    return client


def create_test_post(**kwargs):
    post = Page(**{**PAGE_POST_TEST_DATA, **kwargs})
    post.save()
    return post


@pytest.fixture()
def test_post():
    return create_test_post()



@pytest.mark.django_db
def test_create_post_without_permissions(client, test_post):
    """
    Validate that one can not create a Page without the correct permissions.
    """
    response = client.post(PAGE_PATH, PAGE_POST_TEST_DATA, format="json")
    assert not status.is_success(response.status_code)


@pytest.mark.django_db
def test_create_post(client):
    """
    Validate that creation of Page via the endpoint works
    """
    response = client.post(PAGE_PATH, PAGE_POST_TEST_DATA, format="json")
    assert status.is_success(response.status_code)

    post = Page.objects.get()
    assert post.title == PAGE_POST_TEST_DATA["title"]
    assert post.content == PAGE_POST_TEST_DATA["content"]


@pytest.mark.django_db
def test_get_list(client):
    """
    Validate that getting Page as a list works as intended and has correct format.
    """
    posts = [create_test_post(title="post1"), create_test_post(title="post2")]
    want_posts = []
    posts.reverse()
    for post in posts:
        want_posts.append(
            {"slug": post.slug, "title": post.title}
        )

    response = client.get(PAGE_PATH)

    assert status.is_success(response.status_code)
    got_posts = response.json()
    assert got_posts == want_posts


@pytest.mark.django_db
def test_get_post(client, test_post):
    path = urljoin(PAGE_PATH, str(test_post.slug) + "/")
    response = client.get(path)

    assert status.is_success(response.status_code)
    got_post = response.json()

    assert got_post["slug"] == str(test_post.slug)
    assert got_post["title"] == test_post.title
    assert got_post["content"] == test_post.content
