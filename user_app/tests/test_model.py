import pytest
from user_app.models import User
from public_apps.company.models import Company
from public_apps.employee.models import Employee


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def create_test_user(
    db,
):
    payload = {
        "email": "test.test@example.com",
        "username": "testuser",
        "password": "secret123",
        "role": "employee",
        "is_active": True,
        "is_company_admin": True,
    }
    user, _ = User.objects.get_or_create(email=payload["email"], defaults=payload)
    return user


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def create_company(db, create_test_user):
    payload = {
        "title": "test_company",
        "business_description": "indivitual",
        "phone_number": "01143306714",
        "city": "test",
        "country": "EG",
        "address_line": "test_address",
        "zip": "12345",
        "role": "internal",
        "active": True,
        "owner": create_test_user,
    }
    company, _ = Company.objects.get_or_create(title=payload["title"], defaults=payload)
    return company


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def create_employee(db, create_test_user, create_company):
    payload = {
        "user": create_test_user,
        "company": create_company,
        "position": "vendors",
        "phone_number": "01001002030",
        "role": "vendors",
    }
    employee, _ = Employee.objects.get_or_create(user=payload["user"], defaults=payload)
    return employee


def test_user_model(create_test_user, create_company, create_employee):
    assert isinstance(create_test_user, User)
    assert create_test_user.username == "testuser"
    assert create_test_user.email == "test.test@example.com"
    assert create_test_user.password == "secret123"
    assert create_test_user.is_active == True
    assert create_test_user.is_admin == False
    assert create_test_user.is_staff == False
    assert create_test_user.is_company_admin == True
    assert create_test_user.role == "employee"
    assert create_test_user.company.title == "test_company"
    assert create_test_user.company.business_description == "indivitual"
    assert create_test_user.company.phone_number == "01143306714"
    assert create_test_user.company.city == "test"
    assert create_test_user.company.country == "EG"
    assert create_test_user.company.address_line == "test_address"
    assert create_test_user.company.zip == "12345"
    assert create_test_user.company.role == "internal"
    assert create_test_user.employee.company == create_test_user.company
    assert create_test_user.employee.position == "vendors"
    assert create_test_user.employee.phone_number == "01001002030"
    assert create_test_user.employee.role == "vendors"
