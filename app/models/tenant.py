from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    domain = Column(String(255), unique=True, index=True)
    
    # Tenant configuration
    is_active = Column(Boolean, default=True)
    max_users = Column(Integer, default=100)
    max_documents = Column(Integer, default=10000)
    max_storage_gb = Column(Integer, default=100)
    
    # RAG Pipeline configuration
    default_embedding_model = Column(String(100), default="text-embedding-3-large")
    default_llm_provider = Column(String(50), default="openai")
    citation_confidence_threshold = Column(Integer, default=85)  # Percentage
    
    # Security settings
    require_2fa = Column(Boolean, default=False)
    session_timeout_minutes = Column(Integer, default=480)  # 8 hours
    password_policy = Column(JSON)  # JSON config for password requirements
    
    # Audit and compliance
    audit_logging_enabled = Column(Boolean, default=True)
    data_retention_days = Column(Integer, default=2555)  # 7 years
    compliance_frameworks = Column(JSON)  # ["SOC2", "GDPR", "HIPAA"]
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    users = relationship("User", back_populates="tenant")
    documents = relationship("Document", back_populates="tenant")
    knowledge_bases = relationship("KnowledgeBase", back_populates="tenant")
    
    def __repr__(self):
        return f"<Tenant(id={self.id}, name='{self.name}', slug='{self.slug}')>"
