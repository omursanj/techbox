from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., min_length=1, max_length=20)
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)

    # История диалога пока необязательная.
    # Позже можно будет хранить её в базе.
    history: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    message: str

    # Если AI создал заказ, сюда можно вернуть его ID.
    order_id: int | None = None