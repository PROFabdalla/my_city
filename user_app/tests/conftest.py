import os

import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django

django.setup()


@pytest.fixture
def citizen_payload():
    payload = {
        "password": 1234.1234,
        "username": "test_citizen",
        "email": "citizen@test.test",
    }

    return payload


@pytest.fixture
def company_admin_payload():
    payload = dict(
        password=1234.1234,
        username="test_company_admin",
        email="company_admin@test.test",
        company=dict(
            title="test_company_admin",
            business_description="indivitual",
            phone_number="01143306714",
            role="internal",
        ),
        employee=dict(
            position="test_company_admin",
            phone_number="01001002030",
            role="vendors",
        ),
    )
    return payload


@pytest.fixture
def employee_payload():
    payload = dict(
        password=1234.1234,
        username="test_employee",
        email="employee@test.test",
        company="id",
        employee=dict(
            position="test_employee",
            phone_number="01001002030",
            role="vendors",
        ),
    )
    return payload
