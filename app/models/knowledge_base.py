from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class KnowledgeBaseEntry(Base):
    __tablename__ = "knowledge_base_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    
    # Entry metadata
    entry_type = Column(String(100), nullable=False)  # e.g., "invoice_data", "contract_terms", "medical_record"
    title = Column(String(255))
    description = Column(Text)
    
    # Structured data
    structured_data = Column(JSON, nullable=False)  # The actual knowledge data
    confidence_score = Column(Float)  # AI confidence in the extracted data
    
    # Search and indexing
    searchable_text = Column(Text)  # Text for full-text search
    tags = Column(JSON)  # Array of tags for categorization
    categories = Column(JSON)  # Array of categories
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_validated = Column(Boolean, default=False)
    validated_by = Column(Integer, ForeignKey("users.id"))
    validated_at = Column(DateTime(timezone=True))
    
    # Relationships
    entities = relationship("Entity", back_populates="knowledge_entry")
    relationships = relationship("Relationship", back_populates="knowledge_entry")
    
    def __repr__(self):
        return f"<KnowledgeBaseEntry(id={self.id}, type='{self.entry_type}', title='{self.title}')>"

class Entity(Base):
    __tablename__ = "entities"
    
    id = Column(Integer, primary_key=True, index=True)
    knowledge_entry_id = Column(Integer, ForeignKey("knowledge_base_entries.id"), nullable=False)
    
    # Entity information
    entity_type = Column(String(100), nullable=False)  # e.g., "person", "organization", "date", "amount"
    entity_value = Column(String(500), nullable=False)
    entity_text = Column(Text)  # Original text from document
    
    # Entity metadata
    confidence_score = Column(Float)
    start_position = Column(Integer)  # Position in original text
    end_position = Column(Integer)
    
    # Entity properties
    properties = Column(JSON)  # Additional entity properties
    
    # Relationships
    knowledge_entry = relationship("KnowledgeBaseEntry", back_populates="entities")
    
    def __repr__(self):
        return f"<Entity(id={self.id}, type='{self.entity_type}', value='{self.entity_value}')>"

class Relationship(Base):
    __tablename__ = "relationships"
    
    id = Column(Integer, primary_key=True, index=True)
    knowledge_entry_id = Column(Integer, ForeignKey("knowledge_base_entries.id"), nullable=False)
    
    # Relationship information
    relationship_type = Column(String(100), nullable=False)  # e.g., "belongs_to", "contains", "references"
    source_entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    target_entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    
    # Relationship metadata
    confidence_score = Column(Float)
    relationship_properties = Column(JSON)  # Additional relationship properties
    
    # Relationships
    knowledge_entry = relationship("KnowledgeBaseEntry", back_populates="relationships")
    source_entity = relationship("Entity", foreign_keys=[source_entity_id])
    target_entity = relationship("Entity", foreign_keys=[target_entity_id])
    
    def __repr__(self):
        return f"<Relationship(id={self.id}, type='{self.relationship_type}', source={self.source_entity_id}, target={self.target_entity_id})>"
