import pytest

from app import app, DISCOUNTS


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_discount_state():
    # Keep each test independent.
    DISCOUNTS["WELCOME10"]["used"] = False


def test_user_cannot_read_another_users_invoice(client):
    response = client.get(
        "/invoices/1002",
        headers={"X-User": "alice"},
    )

    assert response.status_code == 403


def test_discount_code_cannot_be_reused(client):
    first = client.post("/discounts/WELCOME10/apply")
    second = client.post("/discounts/WELCOME10/apply")

    assert first.status_code == 200
    assert second.status_code == 409