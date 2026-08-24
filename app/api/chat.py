from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import run_ai_agent


router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
    summary="Chat with TechBox AI",
)
def chat_with_ai(
    request: ChatRequest,
) -> ChatResponse:
    try:
        result = run_ai_agent(
            message=request.message,
            history=request.history,
        )

        return ChatResponse(
            message=result["message"],
            order_id=result.get("order_id"),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"AI agent error: {str(error)}",
        ) from error