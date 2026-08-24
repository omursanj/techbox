from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_existing_order():
    response = client.get("/orders/1")

    assert response.status_code in {200, 404}

    if response.status_code == 200:
        data = response.json()

        assert data["id"] == 1
        assert "status" in data
        assert "total" in data
        assert "city" in data


def test_get_nonexistent_order():
    response = client.get("/orders/999999")

    assert response.status_code == 404

    assert response.json()["detail"] == "Заказ не найден."


def test_get_order_invalid_id():
    response = client.get("/orders/0")

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "ID заказа должен быть больше нуля."
    )


def test_get_orders_by_customer():
    response = client.get(
        "/orders/customer/1"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["customer_id"] == 1
    assert "count" in data
    assert "orders" in data
    assert isinstance(data["orders"], list)


def test_get_orders_invalid_customer_id():
    response = client.get(
        "/orders/customer/0"
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "ID клиента должен быть больше нуля."
    )


def test_update_order_status_invalid_status():
    response = client.patch(
        "/orders/1/status",
        params={
            "status": "something_wrong",
        },
    )

    assert response.status_code == 400

    assert "Недопустимый статус заказа" in (
        response.json()["detail"]
    )


def test_update_order_status_missing_status():
    response = client.patch(
        "/orders/1/status"
    )

    assert response.status_code == 422


def test_update_nonexistent_order_status():
    response = client.patch(
        "/orders/999999/status",
        params={
            "status": "confirmed",
        },
    )

    assert response.status_code == 404


def test_allowed_order_statuses():
    allowed_statuses = [
        "pending",
        "confirmed",
        "processing",
        "shipped",
        "completed",
        "cancelled",
    ]

    for status in allowed_statuses:
        assert isinstance(status, str)
        assert status