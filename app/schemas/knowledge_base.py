from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class KnowledgeEntryBase(BaseModel):
    entry_type: str
    title: Optional[str] = None
    description: Optional[str] = None
    structured_data: Dict[str, Any]
    confidence_score: Optional[float] = None
    searchable_text: Optional[str] = None
    tags: Optional[List[str]] = None
    categories: Optional[List[str]] = None

class KnowledgeEntryCreate(KnowledgeEntryBase):
    document_id: int

class KnowledgeEntryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    structured_data: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    searchable_text: Optional[str] = None
    tags: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    is_validated: Optional[bool] = None

class KnowledgeEntryResponse(KnowledgeEntryBase):
    id: int
    document_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_validated: bool
    validated_by: Optional[int] = None
    validated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class EntityBase(BaseModel):
    entity_type: str
    entity_value: str
    entity_text: Optional[str] = None
    confidence_score: Optional[float] = None
    start_position: Optional[int] = None
    end_position: Optional[int] = None
    properties: Optional[Dict[str, Any]] = None

class EntityCreate(EntityBase):
    knowledge_entry_id: int

class EntityResponse(EntityBase):
    id: int
    knowledge_entry_id: int

    class Config:
        from_attributes = True

class RelationshipBase(BaseModel):
    relationship_type: str
    source_entity_id: int
    target_entity_id: int
    confidence_score: Optional[float] = None
    relationship_properties: Optional[Dict[str, Any]] = None

class RelationshipCreate(RelationshipBase):
    knowledge_entry_id: int

class RelationshipResponse(RelationshipBase):
    id: int
    knowledge_entry_id: int

    class Config:
        from_attributes = True

class SearchQuery(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None
    page: int = 1
    size: int = 20
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "desc"

class SearchResult(BaseModel):
    id: int
    entry_type: str
    title: Optional[str] = None
    description: Optional[str] = None
    structured_data: Dict[str, Any]
    confidence_score: Optional[float] = None
    search_score: float
    tags: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    created_at: datetime
    document_id: int

    class Config:
        from_attributes = True

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int
    page: int
    size: int
    pages: int
    query: str
    filters: Optional[Dict[str, Any]] = None

class KnowledgeBaseStats(BaseModel):
    total_entries: int
    total_documents: int
    entries_by_type: Dict[str, int]
    validation_pending: int
    average_confidence: float
    recent_activity: List[Dict[str, Any]]
