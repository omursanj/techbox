import re


def validate_non_empty_text(
    value: str,
    field_name: str = "Поле",
) -> str:
    value = value.strip()

    if not value:
        raise ValueError(
            f"{field_name} не может быть пустым."
        )

    return value


def validate_positive_integer(
    value: int,
    field_name: str = "Значение",
) -> int:
    if value <= 0:
        raise ValueError(
            f"{field_name} должно быть больше нуля."
        )

    return value


def validate_non_negative_integer(
    value: int,
    field_name: str = "Значение",
) -> int:
    if value < 0:
        raise ValueError(
            f"{field_name} не может быть отрицательным."
        )

    return value


def validate_price(
    price: int,
) -> int:
    if price <= 0:
        raise ValueError(
            "Цена должна быть больше нуля."
        )

    return price


def validate_stock(
    stock: int,
) -> int:
    if stock < 0:
        raise ValueError(
            "Остаток товара не может быть отрицательным."
        )

    return stock


def validate_quantity(
    quantity: int,
) -> int:
    if quantity <= 0:
        raise ValueError(
            "Количество товара должно быть больше нуля."
        )

    return quantity


def validate_city(
    city: str,
) -> str:
    city = city.strip()

    if not city:
        raise ValueError(
            "Город не указан."
        )

    if len(city) > 100:
        raise ValueError(
            "Название города слишком длинное."
        )

    return city


def validate_customer_name(
    name: str,
) -> str:
    name = name.strip()

    if not name:
        raise ValueError(
            "Имя покупателя не указано."
        )

    if len(name) > 150:
        raise ValueError(
            "Имя покупателя слишком длинное."
        )

    return name


def validate_product_ids(
    product_ids: list[int],
) -> list[int]:
    if not product_ids:
        raise ValueError(
            "Не указан ни один товар."
        )

    for product_id in product_ids:
        if product_id <= 0:
            raise ValueError(
                "ID товара должен быть больше нуля."
            )

    return product_ids


def validate_order_items(
    items: list[dict],
) -> list[dict]:
    if not items:
        raise ValueError(
            "В заказе должен быть хотя бы один товар."
        )

    for item in items:
        if "product_id" not in item:
            raise ValueError(
                "В позиции заказа отсутствует product_id."
            )

        if "quantity" not in item:
            raise ValueError(
                "В позиции заказа отсутствует quantity."
            )

        validate_positive_integer(
            item["product_id"],
            "ID товара",
        )

        validate_quantity(
            item["quantity"]
        )

    return items


def contains_only_safe_search_characters(
    value: str,
) -> bool:
    """
    Проверяет поисковую строку.

    Разрешаем:
    - буквы
    - цифры
    - пробелы
    - дефис
    - точку
    - плюс
    """

    value = value.strip()

    if not value:
        return False

    pattern = r"[\w\s.\-+]+"

    return re.fullmatch(
        pattern,
        value,
        flags=re.UNICODE,
    ) is not None