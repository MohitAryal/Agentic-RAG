from app.schemas import ChatResponse, ChatRequest
from app.services.rag_pipeline import generate_agent_response

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_input: ChatRequest):
    response = await generate_agent_response(query=chat_input.query)
    return ChatResponse(response=response)