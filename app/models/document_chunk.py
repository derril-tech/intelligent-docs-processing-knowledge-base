from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from pgvector.sqlalchemy import Vector
import enum

class ChunkType(enum.Enum):
    TEXT = "text"
    TABLE = "table"
    IMAGE = "image"
    HEADER = "header"
    FOOTER = "footer"

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    
    # Chunk content and metadata
    chunk_type = Column(Enum(ChunkType), default=ChunkType.TEXT)
    content = Column(Text, nullable=False)
    content_hash = Column(String(64), nullable=False, index=True)  # For deduplication
    
    # Position information
    page_number = Column(Integer)
    start_position = Column(Integer)  # Character position in original document
    end_position = Column(Integer)
    
    # Vector embeddings for RAG
    embedding_model = Column(String(100), nullable=False)  # e.g., "text-embedding-3-large"
    embedding = Column(Vector(3072), nullable=True)  # OpenAI text-embedding-3-large dimensions
    embedding_updated_at = Column(DateTime(timezone=True))
    
    # RAG metadata
    metadata = Column(JSON)  # Additional chunk metadata
    tags = Column(JSON)  # Tags for filtering
    confidence_score = Column(Float)  # AI confidence in chunk quality
    
    # Processing information
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    document = relationship("Document", back_populates="chunks")
    citations = relationship("Citation", back_populates="source_chunk")
    
    def __repr__(self):
        return f"<DocumentChunk(id={self.id}, document_id={self.document_id}, type='{self.chunk_type}')>"

class Citation(Base):
    __tablename__ = "citations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Citation source
    source_chunk_id = Column(Integer, ForeignKey("document_chunks.id"), nullable=False)
    source_document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    
    # Citation target (answer or generated content)
    answer_id = Column(Integer, ForeignKey("answers.id"), nullable=False)
    
    # Citation details
    span_start = Column(Integer)  # Start position in the answer
    span_end = Column(Integer)    # End position in the answer
    confidence_score = Column(Float)  # Confidence in this citation
    citation_type = Column(String(50), default="direct")  # direct, indirect, reference
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    source_chunk = relationship("DocumentChunk", back_populates="citations")
    source_document = relationship("Document")
    answer = relationship("Answer", back_populates="citations")
    
    def __repr__(self):
        return f"<Citation(id={self.id}, answer_id={self.answer_id}, chunk_id={self.source_chunk_id})>"

class Answer(Base):
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Answer content
    question = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=False)
    answer_hash = Column(String(64), nullable=False, index=True)  # For deduplication
    
    # RAG metadata
    model_used = Column(String(100), nullable=False)  # e.g., "gpt-4", "claude-3"
    prompt_template = Column(String(255))
    context_chunks_used = Column(JSON)  # List of chunk IDs used as context
    
    # Quality metrics
    confidence_score = Column(Float)
    factuality_score = Column(Float)
    citation_count = Column(Integer, default=0)
    
    # User and session info
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    citations = relationship("Citation", back_populates="answer")
    
    def __repr__(self):
        return f"<Answer(id={self.id}, question='{self.question[:50]}...')>"
