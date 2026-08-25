from unittest.mock import patch

from app.tools.check_order_status import check_order_status_tool


@patch("app.tools.check_order_status.get_order_by_id")
def test_check_order_status_returns_current_status(mock_get_order):
    mock_get_order.return_value = {
        "id": 42,
        "status": "shipped",
    }

    result = check_order_status_tool(order_id=42)

    assert result == {
        "success": True,
        "message": "Статус заказа получен.",
        "order": {
            "order_id": 42,
            "status": "shipped",
            "status_label": "Передан в доставку",
        },
    }


@patch("app.tools.check_order_status.get_order_by_id")
def test_check_order_status_reports_missing_order(mock_get_order):
    mock_get_order.return_value = None

    result = check_order_status_tool(order_id=42)

    assert result["success"] is False
    assert result["message"] == "Заказ №42 не найден."
    assert result["order"] is None
