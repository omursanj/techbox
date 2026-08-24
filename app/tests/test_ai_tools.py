from app.tools.check_delivery import check_delivery_tool
from app.tools.check_stock import check_stock_tool
from app.tools.compare_products import compare_products_tool
from app.tools.get_product import get_product_tool
from app.tools.search_products import search_products_tool


def test_search_products_tool_returns_structure():
    result = search_products_tool(
        category="mouse",
        in_stock_only=True,
    )

    assert "count" in result
    assert "products" in result
    assert isinstance(result["products"], list)


def test_get_product_tool_existing_or_missing():
    result = get_product_tool(
        product_id=1,
    )

    assert "found" in result
    assert "product" in result

    if result["found"]:
        assert result["product"]["id"] == 1
    else:
        assert result["product"] is None


def test_get_product_tool_missing_product():
    result = get_product_tool(
        product_id=999999,
    )

    assert result["found"] is False
    assert result["product"] is None


def test_compare_products_requires_two_products():
    result = compare_products_tool(
        product_ids=[1],
    )

    assert result["success"] is False
    assert result["comparison"] == {}


def test_compare_products_tool():
    result = compare_products_tool(
        product_ids=[1, 2],
    )

    assert "success" in result
    assert "products" in result
    assert "comparison" in result

    if result["success"]:
        assert len(result["products"]) >= 2
        assert isinstance(
            result["comparison"],
            dict,
        )


def test_check_stock_invalid_quantity():
    result = check_stock_tool(
        product_id=1,
        quantity=0,
    )

    assert result["success"] is False
    assert result["available"] is False


def test_check_stock_missing_product():
    result = check_stock_tool(
        product_id=999999,
        quantity=1,
    )

    assert result["success"] is False
    assert result["available"] is False
    assert result["stock"] is None


def test_check_stock_existing_product():
    result = check_stock_tool(
        product_id=1,
        quantity=1,
    )

    assert "success" in result
    assert "available" in result
    assert "stock" in result


def test_check_delivery_available_city():
    result = check_delivery_tool(
        city="Astana",
    )

    assert "success" in result
    assert "available" in result
    assert "delivery_price" in result

    if result["available"]:
        assert result["delivery_price"] is not None


def test_check_delivery_unknown_city():
    result = check_delivery_tool(
        city="UnknownCity",
    )

    assert result["available"] is False
    assert result["delivery_price"] is None


def test_check_delivery_empty_city():
    result = check_delivery_tool(
        city="",
    )

    assert result["success"] is False
    assert result["available"] is False