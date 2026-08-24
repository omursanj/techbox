from typing import Any

from app.services.product_service import compare_products


def compare_products_tool(
    product_ids: list[int],
) -> dict[str, Any]:
    if len(product_ids) < 2:
        return {
            "success": False,
            "message": "Для сравнения нужно выбрать минимум два товара.",
            "products": [],
            "comparison": {},
        }

    products = compare_products(product_ids)

    if len(products) < 2:
        return {
            "success": False,
            "message": "Не удалось найти минимум два товара для сравнения.",
            "products": products,
            "comparison": {},
        }

    comparison: dict[str, dict[str, Any]] = {}

    # Базовые поля, которые полезно сравнивать почти всегда
    base_fields = [
        "name",
        "category",
        "brand",
        "price",
        "stock",
    ]

    for field in base_fields:
        comparison[field] = {}

        for product in products:
            product_id = str(product["id"])

            comparison[field][product_id] = product.get(field)

    # Собираем ВСЕ характеристики,
    # которые реально встречаются хотя бы у одного товара
    specification_keys: set[str] = set()

    for product in products:
        specifications = product.get("specifications") or {}

        specification_keys.update(specifications.keys())

    for key in sorted(specification_keys):
        comparison[key] = {}

        for product in products:
            product_id = str(product["id"])
            specifications = product.get("specifications") or {}

            if key in specifications:
                comparison[key][product_id] = specifications[key]
            else:
                comparison[key][product_id] = None

    return {
        "success": True,
        "message": None,
        "products": products,
        "comparison": comparison,
    }