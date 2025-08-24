from fastapi import APIRouter
from app.api.v1.endpoints import auth, documents, knowledge_base, processing, validation, users, rag

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(processing.router, prefix="/processing", tags=["processing"])
api_router.include_router(validation.router, prefix="/validation", tags=["validation"])
api_router.include_router(knowledge_base.router, prefix="/knowledge", tags=["knowledge-base"])
api_router.include_router(rag.router, prefix="/rag", tags=["rag"])

# WebSocket endpoint for real-time communication
from app.core.websocket import websocket_endpoint
api_router.add_websocket_route("/ws", websocket_endpoint)
