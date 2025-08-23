"""
RAG API Endpoints for DocuMind™
Provides endpoints for asking questions and getting RAG-powered answers
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.core.tenant_middleware import get_current_tenant, set_tenant_context
from app.models.user import User
from app.models.tenant import Tenant
from app.services.rag_service import RAGService
from app.schemas.rag import QuestionRequest, AnswerResponse, CitationResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
rag_service = RAGService()

@router.post("/ask", response_model=AnswerResponse)
async def ask_question(
    request: QuestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """
    Ask a question and get a RAG-powered answer with citations
    """
    try:
        # Set tenant context for database operations
        set_tenant_context(db, current_tenant.id)
        
        # Ask question using RAG service
        result = await rag_service.ask_question(
            db=db,
            question=request.question,
            user_id=current_user.id,
            tenant_id=current_tenant.id
        )
        
        # Format citations for response
        citations = []
        for citation_data in result["citations"]:
            citation = CitationResponse(
                chunk_id=citation_data["chunk_id"],
                document_id=citation_data["document_id"],
                span_start=citation_data["span_start"],
                span_end=citation_data["span_end"],
                confidence=citation_data["confidence"]
            )
            citations.append(citation)
        
        return AnswerResponse(
            answer=result["answer"],
            citations=citations,
            confidence_score=result["confidence_score"],
            answer_id=result["answer_id"]
        )
        
    except Exception as e:
        logger.error(f"Error asking question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process question"
        )

@router.get("/answers", response_model=List[AnswerResponse])
async def get_user_answers(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """
    Get user's previous answers
    """
    try:
        set_tenant_context(db, current_tenant.id)
        
        # Get answers for current user
        from app.models.document_chunk import Answer, Citation
        
        answers = db.query(Answer).filter(
            Answer.user_id == current_user.id
        ).offset(skip).limit(limit).all()
        
        result = []
        for answer in answers:
            # Get citations for this answer
            citations = db.query(Citation).filter(
                Citation.answer_id == answer.id
            ).all()
            
            citation_responses = []
            for citation in citations:
                citation_response = CitationResponse(
                    chunk_id=citation.source_chunk_id,
                    document_id=citation.source_document_id,
                    span_start=citation.span_start,
                    span_end=citation.span_end,
                    confidence=citation.confidence_score
                )
                citation_responses.append(citation_response)
            
            answer_response = AnswerResponse(
                answer=answer.answer_text,
                citations=citation_responses,
                confidence_score=answer.confidence_score,
                answer_id=answer.id
            )
            result.append(answer_response)
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting user answers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve answers"
        )

@router.get("/search", response_model=List[Dict[str, Any]])
async def search_chunks(
    query: str,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """
    Search document chunks using vector similarity
    """
    try:
        set_tenant_context(db, current_tenant.id)
        
        # Search using vector similarity
        results = rag_service.vector_store.similarity_search(
            query,
            k=limit,
            score_threshold=0.7
        )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "content": result.page_content,
                "metadata": result.metadata,
                "score": getattr(result, 'score', 0.0)
            })
        
        return formatted_results
        
    except Exception as e:
        logger.error(f"Error searching chunks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search chunks"
        )

@router.post("/process-document/{document_id}")
async def process_document_for_rag(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """
    Process a document to create chunks and embeddings for RAG
    """
    try:
        set_tenant_context(db, current_tenant.id)
        
        # Get document
        from app.models.document import Document
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.tenant_id == current_tenant.id
        ).first()
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Get document content (simplified - would need actual file reading)
        # For now, we'll use a placeholder
        content = "Sample document content for processing..."
        
        # Process document with RAG service
        chunks = await rag_service.process_document(
            db=db,
            document=document,
            content=content
        )
        
        return {
            "message": "Document processed successfully",
            "chunks_created": len(chunks),
            "document_id": document_id
        }
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process document"
        )
