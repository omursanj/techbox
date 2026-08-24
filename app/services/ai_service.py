import json
from typing import Any

from openai import OpenAI

from app.config import settings
from app.prompts.system_prompt import SYSTEM_PROMPT

from app.tools.search_products import search_products_tool
from app.tools.get_product import get_product_tool
from app.tools.compare_products import compare_products_tool
from app.tools.check_stock import check_stock_tool
from app.tools.check_delivery import check_delivery_tool
from app.tools.create_order import create_order_tool


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key,
)

# =========================================================
# TOOL DEFINITIONS
# Эти схемы OpenAI видит и по ним решает,
# какую функцию вызвать.
# =========================================================

TOOLS = [
    {
        "type": "function",
        "name": "search_products",
        "description": (
            "Ищет товары в каталоге TechBox. "
            "Используй, когда пользователь хочет найти товар "
            "по названию, категории, цене или наличию."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": ["string", "null"],
                    "description": (
                        "Поисковая строка, например Logitech, "
                        "wireless или charger."
                    ),
                },
                "category": {
                    "type": ["string", "null"],
                    "description": (
                        "Категория товара: headphones, keyboard, "
                        "mouse или charger."
                    ),
                },
                "min_price": {
                    "type": ["integer", "null"],
                    "description": "Минимальная цена в тенге.",
                },
                "max_price": {
                    "type": ["integer", "null"],
                    "description": "Максимальная цена в тенге.",
                },
                "in_stock_only": {
                    "type": "boolean",
                    "description": (
                        "Если true, показывать только товары "
                        "с положительным остатком."
                    ),
                },
            },
            "required": [
                "query",
                "category",
                "min_price",
                "max_price",
                "in_stock_only",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    },

    {
        "type": "function",
        "name": "get_product",
        "description": (
            "Получает полную информацию о конкретном товаре "
            "TechBox по его ID."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "integer",
                    "description": "ID товара в каталоге TechBox.",
                },
            },
            "required": ["product_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },

    {
        "type": "function",
        "name": "compare_products",
        "description": (
            "Сравнивает несколько товаров только по данным "
            "каталога TechBox."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "product_ids": {
                    "type": "array",
                    "items": {
                        "type": "integer",
                    },
                    "minItems": 2,
                    "description": "ID товаров для сравнения.",
                },
            },
            "required": ["product_ids"],
            "additionalProperties": False,
        },
        "strict": True,
    },

    {
        "type": "function",
        "name": "check_stock",
        "description": (
            "Проверяет складской остаток товара и можно ли "
            "заказать указанное количество."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "integer",
                    "description": "ID товара.",
                },
                "quantity": {
                    "type": "integer",
                    "minimum": 1,
                    "description": (
                        "Количество единиц, которое хочет пользователь."
                    ),
                },
            },
            "required": [
                "product_id",
                "quantity",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    },

    {
        "type": "function",
        "name": "check_delivery",
        "description": (
            "Проверяет, доступна ли доставка TechBox "
            "в указанный город и сколько она стоит."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Город доставки.",
                },
            },
            "required": ["city"],
            "additionalProperties": False,
        },
        "strict": True,
    },

    {
        "type": "function",
        "name": "create_order",
        "description": (
            "Создаёт заказ TechBox. Используй только после того, "
            "как пользователь явно подтвердил заказ и известны "
            "товары, количество, имя, телефон и город."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "customer_name": {
                    "type": "string",
                    "description": "Имя покупателя.",
                },
                "customer_phone": {
                    "type": "string",
                    "description": "Телефон покупателя.",
                },
                "city": {
                    "type": "string",
                    "description": "Город доставки.",
                },
                "items": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "properties": {
                            "product_id": {
                                "type": "integer",
                            },
                            "quantity": {
                                "type": "integer",
                                "minimum": 1,
                            },
                        },
                        "required": [
                            "product_id",
                            "quantity",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
            "required": [
                "customer_name",
                "customer_phone",
                "city",
                "items",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


# =========================================================
# TOOL DISPATCHER
# Связывает имя function call от OpenAI
# с нашей реальной Python-функцией.
# =========================================================

def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:

    if tool_name == "search_products":
        return search_products_tool(
            query=arguments.get("query"),
            category=arguments.get("category"),
            min_price=arguments.get("min_price"),
            max_price=arguments.get("max_price"),
            in_stock_only=arguments.get(
                "in_stock_only",
                True,
            ),
        )

    if tool_name == "get_product":
        return get_product_tool(
            product_id=arguments["product_id"],
        )

    if tool_name == "compare_products":
        return compare_products_tool(
            product_ids=arguments["product_ids"],
        )

    if tool_name == "check_stock":
        return check_stock_tool(
            product_id=arguments["product_id"],
            quantity=arguments["quantity"],
        )

    if tool_name == "check_delivery":
        return check_delivery_tool(
            city=arguments["city"],
        )

    if tool_name == "create_order":
        return create_order_tool(
            customer_name=arguments["customer_name"],
            customer_phone=arguments["customer_phone"],
            city=arguments["city"],
            items=arguments["items"],
        )

    return {
        "success": False,
        "message": f"Неизвестный инструмент: {tool_name}",
    }


# =========================================================
# HISTORY
# Преобразуем историю нашего ChatRequest
# в формат Responses API.
# =========================================================

def build_input(
    message: str,
    history: list[Any] | None = None,
) -> list[dict[str, Any]]:

    input_items: list[dict[str, Any]] = []

    if history:
        for history_message in history:

            if isinstance(history_message, dict):
                role = history_message.get("role")
                content = history_message.get("content")
            else:
                role = history_message.role
                content = history_message.content

            if role not in {"user", "assistant"}:
                continue

            if not content:
                continue

            input_items.append(
                {
                    "role": role,
                    "content": content,
                }
            )

    input_items.append(
        {
            "role": "user",
            "content": message,
        }
    )

    return input_items


# =========================================================
# MAIN AI AGENT
# =========================================================

def run_ai_agent(
    message: str,
    history: list[Any] | None = None,
) -> dict[str, Any]:

    input_items = build_input(
        message=message,
        history=history,
    )

    response = client.responses.create(
        model=settings.openrouter_model,
        instructions=SYSTEM_PROMPT,
        tools=TOOLS,
        input=input_items,
    )

    created_order_id: int | None = None

    # Защита от бесконечных циклов tool calling
    max_tool_rounds = 8

    for _ in range(max_tool_rounds):

        function_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        # Если модель больше не вызывает tools,
        # значит у нас готов финальный ответ.
        if not function_calls:
            return {
                "message": response.output_text,
                "order_id": created_order_id,
            }

        # Сохраняем output модели в conversation context.
        input_items.extend(response.output)

        for function_call in function_calls:

            try:
                arguments = json.loads(
                    function_call.arguments
                )

                result = execute_tool(
                    tool_name=function_call.name,
                    arguments=arguments,
                )

                # Если только что был создан заказ,
                # запоминаем его ID.
                if (
                    function_call.name == "create_order"
                    and result.get("success")
                    and result.get("order")
                ):
                    created_order_id = (
                        result["order"].get("order_id")
                    )

            except Exception as error:
                result = {
                    "success": False,
                    "message": (
                        "Не удалось выполнить операцию: "
                        f"{str(error)}"
                    ),
                }

            # Возвращаем результат функции обратно модели.
            input_items.append(
                {
                    "type": "function_call_output",
                    "call_id": function_call.call_id,
                    "output": json.dumps(
                        result,
                        ensure_ascii=False,
                    ),
                }
            )

        # Теперь модель получает результаты tools
        # и решает: ответить пользователю или
        # вызвать следующий инструмент.
        response = client.responses.create(
            model=settings.openrouter_model,
            instructions=SYSTEM_PROMPT,
            tools=TOOLS,
            input=input_items,
        )

    return {
        "message": (
            "Не удалось завершить запрос: "
            "превышено допустимое количество операций."
        ),
        "order_id": created_order_id,
    }