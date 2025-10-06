from app.dependencies import get_user_id
from app.schemas import ChatResponse, ChatRequest
from app.services.rag_pipeline import generate_agent_response

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    chat_input: ChatRequest,
    user_id: str = Depends(get_user_id)
):
    response = await generate_agent_response(user_id=user_id, query=chat_input.query)
    return ChatResponse(response=response)