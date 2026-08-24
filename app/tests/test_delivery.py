from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_delivery_cities():
    response = client.get("/delivery")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_check_available_city():
    response = client.get(
        "/delivery/check",
        params={
            "city": "Astana",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["city"].lower() == "astana"
    assert data["available"] is True
    assert data["delivery_price"] is not None


def test_check_unavailable_city():
    response = client.get(
        "/delivery/check",
        params={
            "city": "Pavlodar",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["available"] is False
    assert data["delivery_price"] is None


def test_check_unknown_city():
    response = client.get(
        "/delivery/check",
        params={
            "city": "UnknownCity",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["available"] is False
    assert data["delivery_price"] is None


def test_get_available_city_directly():
    response = client.get(
        "/delivery/Astana"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["available"] is True
    assert data["city"].lower() == "astana"


def test_get_unavailable_city_directly():
    response = client.get(
        "/delivery/Pavlodar"
    )

    assert response.status_code == 404


def test_get_unknown_city_directly():
    response = client.get(
        "/delivery/UnknownCity"
    )

    assert response.status_code == 404


def test_delivery_city_required():
    response = client.get(
        "/delivery/check"
    )

    assert response.status_code == 422