from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import structlog

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.knowledge_base import KnowledgeBaseEntry, Entity, Relationship
from app.schemas.knowledge_base import (
    KnowledgeEntryResponse, 
    SearchQuery, 
    SearchResponse,
    KnowledgeBaseStats,
    EntityResponse,
    RelationshipResponse
)
from app.services.search import SearchService

logger = structlog.get_logger()
router = APIRouter()

@router.get("/search", response_model=SearchResponse)
async def search_knowledge_base(
    query: str,
    filters: Optional[str] = None,
    page: int = 1,
    size: int = 20,
    sort_by: Optional[str] = None,
    sort_order: str = "desc",
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Search knowledge base entries"""
    try:
        search_service = SearchService()
        results = await search_service.search(
            query=query,
            filters=filters,
            page=page,
            size=size,
            sort_by=sort_by,
            sort_order=sort_order,
            user_id=current_user.id
        )
        
        return results
        
    except Exception as e:
        logger.error("Search failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Search failed"
        )

@router.get("/entries", response_model=List[KnowledgeEntryResponse])
async def get_knowledge_entries(
    skip: int = 0,
    limit: int = 20,
    entry_type: Optional[str] = None,
    is_validated: Optional[bool] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get knowledge base entries"""
    query = db.query(KnowledgeBaseEntry)
    
    if entry_type:
        query = query.filter(KnowledgeBaseEntry.entry_type == entry_type)
    if is_validated is not None:
        query = query.filter(KnowledgeBaseEntry.is_validated == is_validated)
    
    entries = query.offset(skip).limit(limit).all()
    return entries

@router.get("/entries/{entry_id}", response_model=KnowledgeEntryResponse)
async def get_knowledge_entry(
    entry_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get knowledge base entry by ID"""
    entry = db.query(KnowledgeBaseEntry).filter(KnowledgeBaseEntry.id == entry_id).first()
    
    if entry is None:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")
    
    return entry

@router.get("/entries/{entry_id}/entities", response_model=List[EntityResponse])
async def get_entry_entities(
    entry_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get entities for a knowledge base entry"""
    entities = db.query(Entity).filter(Entity.knowledge_entry_id == entry_id).all()
    return entities

@router.get("/entries/{entry_id}/relationships", response_model=List[RelationshipResponse])
async def get_entry_relationships(
    entry_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get relationships for a knowledge base entry"""
    relationships = db.query(Relationship).filter(
        Relationship.knowledge_entry_id == entry_id
    ).all()
    return relationships

@router.get("/stats", response_model=KnowledgeBaseStats)
async def get_knowledge_base_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get knowledge base statistics"""
    try:
        total_entries = db.query(KnowledgeBaseEntry).count()
        total_documents = db.query(KnowledgeBaseEntry.document_id).distinct().count()
        validation_pending = db.query(KnowledgeBaseEntry).filter(
            KnowledgeBaseEntry.is_validated == False
        ).count()
        
        # Get entries by type
        entries_by_type = {}
        type_counts = db.query(
            KnowledgeBaseEntry.entry_type,
            db.func.count(KnowledgeBaseEntry.id)
        ).group_by(KnowledgeBaseEntry.entry_type).all()
        
        for entry_type, count in type_counts:
            entries_by_type[entry_type] = count
        
        # Calculate average confidence
        avg_confidence = db.query(
            db.func.avg(KnowledgeBaseEntry.confidence_score)
        ).scalar() or 0.0
        
        # Get recent activity
        recent_entries = db.query(KnowledgeBaseEntry).order_by(
            KnowledgeBaseEntry.created_at.desc()
        ).limit(10).all()
        
        recent_activity = [
            {
                "id": entry.id,
                "entry_type": entry.entry_type,
                "title": entry.title,
                "created_at": entry.created_at.isoformat()
            }
            for entry in recent_entries
        ]
        
        return KnowledgeBaseStats(
            total_entries=total_entries,
            total_documents=total_documents,
            entries_by_type=entries_by_type,
            validation_pending=validation_pending,
            average_confidence=float(avg_confidence),
            recent_activity=recent_activity
        )
        
    except Exception as e:
        logger.error("Failed to get knowledge base stats", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get statistics"
        )
