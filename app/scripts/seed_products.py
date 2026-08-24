from app.database import supabase


PRODUCTS = [
    {
        "name": "Logitech G305",
        "category": "mouse",
        "brand": "Logitech",
        "description": "Wireless gaming mouse",
        "price": 24990,
        "stock": 8,
        "specifications": {
            "connection": "Wireless",
            "dpi": 12000,
        },
        "image_url": None,
    },
    {
        "name": "Razer DeathAdder Essential",
        "category": "mouse",
        "brand": "Razer",
        "description": "Wired gaming mouse",
        "price": 17990,
        "stock": 6,
        "specifications": {
            "connection": "Wired",
            "dpi": 6400,
        },
        "image_url": None,
    },
    {
        "name": "Keychron K2",
        "category": "keyboard",
        "brand": "Keychron",
        "description": "Wireless mechanical keyboard",
        "price": 34990,
        "stock": 5,
        "specifications": {
            "connection": "Bluetooth",
            "layout": "US",
        },
        "image_url": None,
    },
    {
        "name": "Logitech K380",
        "category": "keyboard",
        "brand": "Logitech",
        "description": "Compact wireless keyboard",
        "price": 19990,
        "stock": 10,
        "specifications": {
            "connection": "Bluetooth",
        },
        "image_url": None,
    },
    {
        "name": "JBL Tune 520BT",
        "category": "headphones",
        "brand": "JBL",
        "description": "Wireless on-ear headphones",
        "price": 22990,
        "stock": 7,
        "specifications": {
            "connection": "Bluetooth",
        },
        "image_url": None,
    },
    {
        "name": "Sony WH-CH520",
        "category": "headphones",
        "brand": "Sony",
        "description": "Wireless headphones",
        "price": 27990,
        "stock": 4,
        "specifications": {
            "connection": "Bluetooth",
        },
        "image_url": None,
    },
    {
        "name": "Anker 323 Charger",
        "category": "charger",
        "brand": "Anker",
        "description": "USB-C wall charger",
        "price": 14990,
        "stock": 12,
        "specifications": {
            "power_w": 33,
            "ports": 2,
        },
        "image_url": None,
    },
    {
        "name": "Baseus GaN5 Pro",
        "category": "charger",
        "brand": "Baseus",
        "description": "GaN USB-C charger",
        "price": 26990,
        "stock": 6,
        "specifications": {
            "power_w": 65,
            "ports": 3,
        },
        "image_url": None,
    },
]


def seed_products() -> None:
    response = (
        supabase
        .table("products")
        .insert(PRODUCTS)
        .execute()
    )

    if not response.data:
        raise RuntimeError(
            "Не удалось добавить тестовые товары."
        )

    print(
        f"Добавлено товаров: {len(response.data)}"
    )


if __name__ == "__main__":
    seed_products()