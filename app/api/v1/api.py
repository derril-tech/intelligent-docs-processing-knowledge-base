from fastapi import APIRouter
from app.api.v1.endpoints import auth, documents, knowledge_base, processing, validation, users

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(processing.router, prefix="/processing", tags=["processing"])
api_router.include_router(validation.router, prefix="/validation", tags=["validation"])
api_router.include_router(knowledge_base.router, prefix="/knowledge", tags=["knowledge-base"])
