from app.database import supabase


DELIVERY_CITIES = [
    {
        "city": "Астана",
        "delivery_price": 2000,
        "is_available": True,
    },
    {
        "city": "Алматы",
        "delivery_price": 2500,
        "is_available": True,
    },
    {
        "city": "Караганда",
        "delivery_price": 2500,
        "is_available": True,
    },
    {
        "city": "Шымкент",
        "delivery_price": 3000,
        "is_available": True,
    },
    {
        "city": "Павлодар",
        "delivery_price": 3000,
        "is_available": True,
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
