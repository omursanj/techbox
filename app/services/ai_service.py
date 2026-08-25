import json
import re
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
from app.tools.check_order_status import check_order_status_tool


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key,
)


def normalize_currency_in_response(content: str) -> str:
    """Гарантирует, что AI не вернёт российское обозначение валюты."""
    return re.sub(
        r"(?iu)(?<!\w)(?:₽|руб(?:\.|ль|ля|лей|лях|лями)?)(?!\w)",
        "₸",
        content,
    )


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": (
                "Ищет товары в каталоге TechBox по названию, "
                "модели, бренду, категории, цене и наличию. Поддерживает "
                "неполное название модели. Все цены указаны в тенге (₸)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": ["string", "null"],
                    },
                    "category": {
                        "type": ["string", "null"],
                    },
                    "min_price": {
                        "type": ["integer", "null"],
                    },
                    "max_price": {
                        "type": ["integer", "null"],
                    },
                    "in_stock_only": {
                        "type": "boolean",
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
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_order_status",
            "description": (
                "Получает текущий статус уже созданного заказа "
                "TechBox по его номеру."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "integer",
                        "minimum": 1,
                    },
                },
                "required": ["order_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_product",
            "description": (
                "Получает полную информацию о конкретном товаре "
                "TechBox по ID."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "integer",
                    },
                },
                "required": ["product_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
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
                    },
                },
                "required": ["product_ids"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_stock",
            "description": (
                "Проверяет остаток товара и можно ли "
                "заказать указанное количество по product_id из каталога. "
                "Перед проверкой товара по названию или модели сначала "
                "используй search_products."
            ),
            "parameters": {
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
    {
        "type": "function",
        "function": {
            "name": "check_delivery",
            "description": (
                "Проверяет доступность и стоимость доставки "
                "TechBox в указанный город. Стоимость указана в тенге (₸)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                    },
                },
                "required": ["city"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_order",
            "description": (
                "Создаёт заказ TechBox. "
                "Вызывай только после явного подтверждения пользователя "
                "и только если известны товар, количество, имя, телефон и город."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {
                        "type": "string",
                    },
                    "customer_phone": {
                        "type": "string",
                    },
                    "city": {
                        "type": "string",
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
        },
    },
]


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

    if tool_name == "check_order_status":
        return check_order_status_tool(
            order_id=arguments["order_id"],
        )

    if tool_name == "create_order":
        print("CREATE ORDER TOOL CALLED")
        print(arguments)

        result = create_order_tool(
            customer_name=arguments["customer_name"],
            customer_phone=arguments["customer_phone"],
            city=arguments["city"],
            items=arguments["items"],
        )

        print("CREATE ORDER RESULT")
        print(result)

        return result

    return {
        "success": False,
        "message": f"Неизвестный инструмент: {tool_name}",
    }


def build_messages(
    message: str,
    history: list[Any] | None = None,
) -> list[dict[str, Any]]:

    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

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

            messages.append(
                {
                    "role": role,
                    "content": content,
                }
            )

    messages.append(
        {
            "role": "user",
            "content": message,
        }
    )

    return messages


def run_ai_agent(
    message: str,
    history: list[Any] | None = None,
) -> dict[str, Any]:

    messages = build_messages(
        message=message,
        history=history,
    )

    created_order_id: int | None = None
    created_order_message: str | None = None

    max_tool_rounds = 8

    for _ in range(max_tool_rounds):

        response = client.chat.completions.create(
            model=settings.openrouter_model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        messages.append(
            assistant_message.model_dump(
                exclude_none=True
            )
        )

        tool_calls = assistant_message.tool_calls

        if not tool_calls:
            return {
                "message": normalize_currency_in_response(
                    assistant_message.content or ""
                ),
                "order_id": created_order_id,
            }

        for tool_call in tool_calls:

            try:
                arguments = json.loads(
                    tool_call.function.arguments
                )

                result = execute_tool(
                    tool_name=tool_call.function.name,
                    arguments=arguments,
                )

                if (
                    tool_call.function.name == "create_order"
                    and result.get("success")
                    and result.get("order")
                ):
                    created_order_id = (
                        result["order"].get("order_id")
                    )
                    created_order_message = result.get(
                        "customer_message"
                    )

            except Exception as error:
                result = {
                    "success": False,
                    "message": (
                        "Не удалось выполнить операцию: "
                        f"{str(error)}"
                    ),
                }

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        result,
                        ensure_ascii=False,
                    ),
                }
            )

        if created_order_message:
            return {
                "message": created_order_message,
                "order_id": created_order_id,
            }

    return {
        "message": (
            "Не удалось завершить запрос: "
            "слишком много последовательных операций."
        ),
        "order_id": created_order_id,
    }
