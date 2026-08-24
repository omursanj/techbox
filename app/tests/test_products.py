from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_products():
    response = client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_products_by_category():
    response = client.get(
        "/products/search",
        params={
            "category": "mouse",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for product in data:
        assert product["category"].lower() == "mouse"


def test_search_products_by_max_price():
    response = client.get(
        "/products/search",
        params={
            "max_price": 30000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    for product in data:
        assert product["price"] <= 30000


def test_search_products_invalid_price_range():
    response = client.get(
        "/products/search",
        params={
            "min_price": 50000,
            "max_price": 10000,
        },
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "min_price не может быть больше max_price."
    )


def test_get_existing_product():
    response = client.get("/products/1")

    assert response.status_code == 200

    product = response.json()

    assert product["id"] == 1
    assert "name" in product
    assert "price" in product
    assert "stock" in product
    assert "specifications" in product


def test_get_nonexistent_product():
    response = client.get("/products/999999")

    assert response.status_code == 404

    assert response.json()["detail"] == "Товар не найден."


def test_get_product_invalid_id():
    response = client.get("/products/0")

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "ID товара должен быть больше нуля."
    )


def test_products_in_stock_filter():
    response = client.get(
        "/products/search",
        params={
            "in_stock_only": True,
        },
    )

    assert response.status_code == 200

    products = response.json()

    for product in products:
        assert product["stock"] > 0