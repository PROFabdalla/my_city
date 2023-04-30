import pytest
from rest_framework.test import APIClient

from public_apps.company.models import Company
from user_app.models import User

clint = APIClient()


# /////////////////////////////////////////////////////////
# ====================== CITIZENS ======================= #
# /////////////////////////////////////////////////////////
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
    assert (
        response1_data["user"]["employee"]["permissions"]["is_company_admin"] == False
    )


# /////////////////////////////////////////////////////////
# ====================== COMPANY ADMIN =================== #
# /////////////////////////////////////////////////////////
@pytest.mark.django_db
def test_company_admin_login(company_admin_payload):
    response0 = clint.post("/auth/users/", company_admin_payload, format="json")
    db_user = User.objects.filter(email=company_admin_payload["email"])
    db_user.update(is_active=True)
    company = db_user.first().company
    company.active = True
    company.save()
    response0_data = response0.json()

    payload = dict(
        email=company_admin_payload["email"],
        password=company_admin_payload["password"],
    )
    response1 = clint.post("/auth/login/", payload)
    response1_data = response1.json()

    # ---------------------- register test ------------- #
    # ---- user data ---- #
    assert response0.status_code == 201
    assert response0_data["username"] == company_admin_payload["username"]
    assert response0_data["email"] == company_admin_payload["email"]
    assert response0_data["role"] == "employee"
    # ---- user company data ---- #
    assert (
        response0_data["company"]["title"] == company_admin_payload["company"]["title"]
    )
    assert (
        response0_data["company"]["business_description"]
        == company_admin_payload["company"]["business_description"]
    )
    assert (
        response0_data["company"]["phone_number"]
        == company_admin_payload["company"]["phone_number"]
    )
    assert response0_data["company"]["role"] == company_admin_payload["company"]["role"]

    # ---- user employee data ---- #
    assert (
        response0_data["employee"]["position"]
        == company_admin_payload["employee"]["position"]
    )
    assert (
        response0_data["employee"]["phone_number"]
        == company_admin_payload["employee"]["phone_number"]
    )
    assert (
        response0_data["employee"]["role"] == company_admin_payload["employee"]["role"]
    )

    # # --------------------- login test ------------------- #
    assert response1.status_code == 200
    assert response1_data["user"]["username"] == company_admin_payload["username"]
    assert response1_data["user"]["email"] == company_admin_payload["email"]
    assert response1_data["user"]["role"] == "employee"
    assert response1_data["user"]["is_admin"] == False
    assert response1_data["user"]["is_company_admin"] == True


# /////////////////////////////////////////////////////////
# ====================== COMPANY EMPLOYEE ================ #
# /////////////////////////////////////////////////////////
@pytest.fixture
@pytest.mark.django_db
def exist_company_for_employee(company_admin_payload):
    response0 = clint.post("/auth/users/", company_admin_payload, format="json")
    db_user = User.objects.filter(email=company_admin_payload["email"])
    db_user.update(is_active=True)
    company = db_user.first().company
    company.active = True
    company.save()
    return company


@pytest.mark.django_db
def test_employee_login(exist_company_for_employee, employee_payload):
    employee_payload.update(company=exist_company_for_employee.id.hashid)
    response0 = clint.post("/auth/users/", employee_payload, format="json")
    db_user = User.objects.filter(email=employee_payload["email"])
    db_user.update(is_active=True)
    response0_data = response0.json()

    payload = dict(
        email=employee_payload["email"],
        password=employee_payload["password"],
    )
    response1 = clint.post("/auth/login/", payload)
    response1_data = response1.json()

    # ---------------------- register test ------------- #
    # ---- user data ---- #
    # ---------------------- register test ------------- #
    # ---- user data ---- #
    assert response0.status_code == 201
    assert response0_data["username"] == employee_payload["username"]
    assert response0_data["email"] == employee_payload["email"]
    assert response0_data["role"] == "employee"
    # ---- user company data ---- #
    assert response0_data["company"]["title"] == exist_company_for_employee.title
    assert (
        response0_data["company"]["business_description"]
        == exist_company_for_employee.business_description
    )
    assert (
        response0_data["company"]["phone_number"]
        == exist_company_for_employee.phone_number
    )
    assert response0_data["company"]["role"] == exist_company_for_employee.role

    # ---- user employee data ---- #
    assert (
        response0_data["employee"]["position"]
        == employee_payload["employee"]["position"]
    )
    assert (
        response0_data["employee"]["phone_number"]
        == employee_payload["employee"]["phone_number"]
    )
    assert response0_data["employee"]["role"] == employee_payload["employee"]["role"]

    # # --------------------- login test ------------------- #
    assert response1.status_code == 200
    assert response1_data["user"]["username"] == employee_payload["username"]
    assert response1_data["user"]["email"] == employee_payload["email"]
    assert response1_data["user"]["role"] == "employee"
    assert response1_data["user"]["is_admin"] == False
    assert (
        response1_data["user"]["employee"]["permissions"]["is_company_admin"] == False
    )
