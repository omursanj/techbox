from app.database import supabase


DELIVERY_CITIES = [
    {
        "city": "Astana",
        "delivery_price": 2000,
        "is_available": True,
    },
    {
        "city": "Almaty",
        "delivery_price": 2500,
        "is_available": True,
    },
    {
        "city": "Karaganda",
        "delivery_price": 2500,
        "is_available": True,
    },
    {
        "city": "Shymkent",
        "delivery_price": 3000,
        "is_available": True,
    },
    {
        "city": "Pavlodar",
        "delivery_price": 3000,
        "is_available": False,
    },
]


def seed_delivery() -> None:
    response = (
        supabase
        .table("delivery_cities")
        .insert(DELIVERY_CITIES)
        .execute()
    )

    if not response.data:
        raise RuntimeError(
            "Не удалось добавить тестовые города доставки."
        )

    print(
        f"Добавлено городов доставки: {len(response.data)}"
    )


if __name__ == "__main__":
    seed_delivery()