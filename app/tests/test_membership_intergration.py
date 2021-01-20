from rest_framework import status

import pytest

from app.common.enums import AdminGroup, MembershipType
from app.util.test_utils import get_api_client

GROUP_URL = "/api/v1/group"


def _get_membership_url(membership):
    return f"{GROUP_URL}/{membership.group.slug}/membership/"


def _get_membership_url_detail(membership):
    return f"{GROUP_URL}/{membership.group.slug}/membership/{membership.user.user_id}/"


def _get_membership_data(membership, leader=False):
    return {
        "user": {"user_id": membership.user.user_id},
        "group": {"name": membership.group.name},
        "membership_type": "LEADER" if (leader) else "MEMBER",
    }


@pytest.mark.django_db
def test_list_as_anonymous_user(default_client, membership):
    """Tests if an anonymous user can list memberships for a group"""

    url = _get_membership_url(membership)
    response = default_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_retrieve_as_anonymous_user(default_client, membership):
    """Tests if an anonymous user can retrieve a membership"""
    url = _get_membership_url_detail(membership)
    response = default_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_retrieve_as_user(membership, user):
    """Tests if a logged in user can retrieve a membership"""

    client = get_api_client(user=user)
    url = _get_membership_url_detail(membership)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_as_anonymous_user(default_client, membership):
    """Tests if an anonymous user can fails to update a membership"""

    url = _get_membership_url_detail(membership)
    response = default_client.put(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_as_user(user, membership):
    """Tests if a logged in user can fails to update a membership"""

    client = get_api_client(user=user)
    url = _get_membership_url_detail(membership)
    response = client.put(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("group_name", "expected_status_code", "membership_type"),
    [
        (AdminGroup.HS, status.HTTP_200_OK, MembershipType.LEADER),
        (AdminGroup.INDEX, status.HTTP_200_OK, MembershipType.LEADER),
        (AdminGroup.NOK, status.HTTP_200_OK, MembershipType.LEADER),
        (AdminGroup.PROMO, status.HTTP_200_OK, MembershipType.LEADER),
        ("Non_admin_group", status.HTTP_403_FORBIDDEN, None),
    ],
)
def test_update_as_group_user(
    membership, user, group_name, expected_status_code, membership_type,
):
    """Tests if diffierent groups ability to update a membership """
    expected_membership_type = (
        membership_type if membership_type else membership.membership_type
    )

    client = get_api_client(user=user, group_name=group_name)
    url = _get_membership_url_detail(membership)
    data = _get_membership_data(membership, leader=True)
    response = client.put(url, data=data, format="json")
    membership.refresh_from_db()

    assert response.status_code == expected_status_code
    assert membership.membership_type == expected_membership_type


@pytest.mark.django_db
def test_create_member_membership(admin_user, membership):

    client = get_api_client(user=admin_user)
    url = _get_membership_url(membership)
    data = _get_membership_data(membership)
    response = client.post(url, data=data, format="json")
    membership.refresh_from_db()

    assert membership.membership_type == MembershipType.MEMBER
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_leader_membership(admin_user, membership_leader):

    client = get_api_client(user=admin_user)
    url = _get_membership_url(membership_leader)
    data = _get_membership_data(membership_leader, leader=True)
    response = client.post(url, data=data, format="json")
    membership_leader.refresh_from_db()

    assert membership_leader.membership_type == MembershipType.LEADER
    assert response.status_code == status.HTTP_200_OK
