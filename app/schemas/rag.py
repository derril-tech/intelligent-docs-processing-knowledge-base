"""
RAG API Schemas for DocuMind™
Pydantic models for RAG-related API requests and responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class QuestionRequest(BaseModel):
    """Request model for asking a question"""
    question: str = Field(..., min_length=1, max_length=1000, description="The question to ask")
    context: Optional[str] = Field(None, max_length=5000, description="Additional context for the question")
    max_citations: Optional[int] = Field(5, ge=1, le=20, description="Maximum number of citations to include")

class CitationResponse(BaseModel):
    """Response model for a citation"""
    chunk_id: int = Field(..., description="ID of the source chunk")
    document_id: int = Field(..., description="ID of the source document")
    span_start: Optional[int] = Field(None, description="Start position of the citation span")
    span_end: Optional[int] = Field(None, description="End position of the citation span")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for this citation")
    content_preview: Optional[str] = Field(None, description="Preview of the cited content")

class AnswerResponse(BaseModel):
    """Response model for a RAG answer"""
    answer: str = Field(..., description="The generated answer")
    citations: List[CitationResponse] = Field(default_factory=list, description="List of citations")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Overall confidence score")
    answer_id: int = Field(..., description="ID of the saved answer")
    model_used: str = Field(..., description="LLM model used for generation")
    processing_time_ms: Optional[int] = Field(None, description="Time taken to generate answer")
    created_at: Optional[datetime] = Field(None, description="When the answer was created")

class ChunkSearchRequest(BaseModel):
    """Request model for searching chunks"""
    query: str = Field(..., min_length=1, max_length=500, description="Search query")
    limit: int = Field(10, ge=1, le=100, description="Maximum number of results")
    score_threshold: float = Field(0.7, ge=0.0, le=1.0, description="Minimum similarity score")
    filters: Optional[dict] = Field(None, description="Additional filters for search")

class ChunkSearchResponse(BaseModel):
    """Response model for chunk search results"""
    content: str = Field(..., description="Chunk content")
    metadata: dict = Field(..., description="Chunk metadata")
    score: float = Field(..., ge=0.0, le=1.0, description="Similarity score")
    document_id: int = Field(..., description="Source document ID")
    chunk_id: int = Field(..., description="Chunk ID")

class DocumentProcessingRequest(BaseModel):
    """Request model for processing a document"""
    document_id: int = Field(..., description="ID of the document to process")
    chunk_size: Optional[int] = Field(1000, ge=100, le=2000, description="Size of text chunks")
    chunk_overlap: Optional[int] = Field(200, ge=0, le=500, description="Overlap between chunks")
    embedding_model: Optional[str] = Field("text-embedding-3-large", description="Embedding model to use")

class DocumentProcessingResponse(BaseModel):
    """Response model for document processing"""
    message: str = Field(..., description="Processing status message")
    chunks_created: int = Field(..., ge=0, description="Number of chunks created")
    document_id: int = Field(..., description="ID of the processed document")
    processing_time_ms: Optional[int] = Field(None, description="Time taken to process")
    embedding_model: str = Field(..., description="Embedding model used")

class RAGStatsResponse(BaseModel):
    """Response model for RAG statistics"""
    total_chunks: int = Field(..., description="Total number of chunks")
    total_answers: int = Field(..., description="Total number of answers")
    total_citations: int = Field(..., description="Total number of citations")
    avg_confidence_score: float = Field(..., ge=0.0, le=1.0, description="Average confidence score")
    most_used_embedding_model: str = Field(..., description="Most frequently used embedding model")
    most_used_llm_model: str = Field(..., description="Most frequently used LLM model")
