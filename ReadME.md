# TechBox AI Store

TechBox — backend для интернет-магазина электроники с AI-агентом.

Магазин продаёт:

- наушники;
- клавиатуры;
- мыши;
- зарядные устройства.

AI-агент умеет:

- искать товары по запросу;
- показывать цену;
- показывать характеристики;
- проверять наличие;
- сравнивать товары;
- проверять доставку;
- создавать заявку на заказ;
- не разрешать заказать больше товара, чем есть на складе;
- не придумывать отсутствующие характеристики;
- не обещать доставку в неподдерживаемый город.

## Tech Stack

- Python
- FastAPI
- Supabase
- PostgreSQL
- OpenAI API
- Pydantic
- Pytest

## Project Structure

```text
techbox/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── products.py
│   │   ├── delivery.py
│   │   ├── orders.py
│   │   └── chat.py
│   │
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── system_prompt.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── delivery.py
│   │   ├── customer.py
│   │   ├── order.py
│   │   └── chat.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── product_repository.py
│   │   ├── delivery_repository.py
│   │   ├── customer_repository.py
│   │   └── order_repository.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── product_service.py
│   │   ├── delivery_service.py
│   │   ├── order_service.py
│   │   └── ai_service.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── search_products.py
│   │   ├── get_product.py
│   │   ├── compare_products.py
│   │   ├── check_stock.py
│   │   ├── check_delivery.py
│   │   └── create_order.py
│   │
│   └── utils/
│       ├── validators.py
│       ├── phone.py
│       └── calculations.py
│
├── scripts/
│   ├── seed_products.py
│   ├── seed_delivery.py
│   └── seed_orders.py
│
├── tests/
│   ├── test_products.py
│   ├── test_delivery.py
│   ├── test_orders.py
│   └── test_ai_tools.py
│
├── supabase/
│   └── migrations/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md