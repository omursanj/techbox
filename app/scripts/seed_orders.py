from app.database import supabase


TEST_CUSTOMERS = [
    {
        "name": "Aigerim",
        "phone": "+77010000001",
    },
    {
        "name": "Dias",
        "phone": "+77010000002",
    },
]


TEST_ORDERS = [
    {
        "customer_phone": "+77010000001",
        "city": "Astana",
        "delivery_price": 2000,
        "total": 51980,
        "status": "pending",
        "items": [
            {
                "product_id": 1,
                "quantity": 2,
                "price": 24990,
            }
        ],
    },
    {
        "customer_phone": "+77010000002",
        "city": "Almaty",
        "delivery_price": 2500,
        "total": 37490,
        "status": "confirmed",
        "items": [
            {
                "product_id": 5,
                "quantity": 1,
                "price": 22990,
            },
            {
                "product_id": 7,
                "quantity": 1,
                "price": 12000,
            },
        ],
    },
]


def create_test_customers() -> dict[str, int]:
    customer_ids: dict[str, int] = {}

    for customer in TEST_CUSTOMERS:
        existing = (
            supabase
            .table("customers")
            .select("id, phone")
            .eq("phone", customer["phone"])
            .limit(1)
            .execute()
        )

        if existing.data:
            customer_ids[customer["phone"]] = existing.data[0]["id"]
            continue

        response = (
            supabase
            .table("customers")
            .insert(customer)
            .select("id, phone")
            .execute()
        )

        if not response.data:
            raise RuntimeError(
                f'Не удалось создать клиента {customer["name"]}.'
            )

        customer_ids[customer["phone"]] = response.data[0]["id"]

    return customer_ids


def create_test_order(
    customer_id: int,
    city: str,
    delivery_price: int,
    total: int,
    status: str,
) -> int:
    response = (
        supabase
        .table("orders")
        .insert(
            {
                "customer_id": customer_id,
                "city": city,
                "delivery_price": delivery_price,
                "total": total,
                "status": status,
            }
        )
        .select("id")
        .execute()
    )

    if not response.data:
        raise RuntimeError(
            "Не удалось создать тестовый заказ."
        )

    return response.data[0]["id"]


def create_test_order_items(
    order_id: int,
    items: list[dict],
) -> None:
    rows = [
        {
            "order_id": order_id,
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "price": item["price"],
        }
        for item in items
    ]

    response = (
        supabase
        .table("order_items")
        .insert(rows)
        .execute()
    )

    if not response.data:
        raise RuntimeError(
            f"Не удалось создать позиции заказа {order_id}."
        )


def seed_orders() -> None:
    customer_ids = create_test_customers()

    created_count = 0

    for order in TEST_ORDERS:
        customer_id = customer_ids[
            order["customer_phone"]
        ]

        order_id = create_test_order(
            customer_id=customer_id,
            city=order["city"],
            delivery_price=order["delivery_price"],
            total=order["total"],
            status=order["status"],
        )

        create_test_order_items(
            order_id=order_id,
            items=order["items"],
        )

        created_count += 1

    print(
        f"Добавлено тестовых заказов: {created_count}"
    )


if __name__ == "__main__":
    seed_orders()