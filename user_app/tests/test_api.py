import pytest
from rest_framework.test import APIClient
from user_app.models import User


clint = APIClient()


@pytest.fixture
@pytest.mark.django_db
def citizen_token(citizen_payload):
    response0 = clint.post("/auth/users/", citizen_payload)
    user = User.objects.filter(email=citizen_payload["email"]).update(is_active=True)
    payload = dict(
        email=citizen_payload["email"],
        password=citizen_payload["password"],
    )
    response1 = clint.post("/auth/login/", payload)
    response = response1.json()
    return response["token"]


@pytest.mark.django_db
def test_citizen_login(citizen_payload):
    response0 = clint.post("/auth/users/", citizen_payload)
    db_user = User.objects.filter(email=citizen_payload["email"]).update(is_active=True)
    response0_data = response0.json()

    payload = dict(
        email=citizen_payload["email"],
        password=citizen_payload["password"],
    )
    response1 = clint.post("/auth/login/", payload)
    response1_data = response1.json()

    # ---------------------- register test ------------- #
    assert response0.status_code == 201
    assert response0_data["username"] == citizen_payload["username"]
    assert response0_data["email"] == citizen_payload["email"]
    assert response0_data["role"] == "citizen"
    assert response0_data["company"] is None
    assert response0_data["employee"] is None

    # --------------------- login test ------------------- #
    assert response1.status_code == 200
    assert response1_data["user"]["username"] == citizen_payload["username"]
    assert response1_data["user"]["email"] == citizen_payload["email"]
    assert response1_data["user"]["role"] == "citizen"
    assert response1_data["user"]["is_admin"] == False
    assert response1_data["user"]["is_company_admin"] == False
