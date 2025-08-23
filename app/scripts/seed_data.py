#!/usr/bin/env python3
"""
Database seeding script for development environment.
This script creates initial data for testing and development.
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.models.user import User
from app.models.document import Document
from app.models.knowledge_base import KnowledgeBase
from app.models.processing_queue import ProcessingQueue
from app.models.validation_queue import ValidationQueue
from app.core.security import get_password_hash


async def create_sample_users(session: AsyncSession) -> List[User]:
    """Create sample users for development."""
    users = []
    
    # Admin user
    admin_user = User(
        id=str(uuid.uuid4()),
        email="admin@intelligentdocs.com",
        username="admin",
        full_name="System Administrator",
        hashed_password=get_password_hash("admin123"),
        role="admin",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    users.append(admin_user)
    
    # Regular user
    user = User(
        id=str(uuid.uuid4()),
        email="user@intelligentdocs.com",
        username="user",
        full_name="Regular User",
        hashed_password=get_password_hash("user123"),
        role="user",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    users.append(user)
    
    # Validator user
    validator = User(
        id=str(uuid.uuid4()),
        email="validator@intelligentdocs.com",
        username="validator",
        full_name="Document Validator",
        hashed_password=get_password_hash("validator123"),
        role="validator",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    users.append(validator)
    
    session.add_all(users)
    await session.commit()
    
    print(f"Created {len(users)} sample users")
    return users


async def create_sample_knowledge_bases(session: AsyncSession) -> List[KnowledgeBase]:
    """Create sample knowledge bases."""
    knowledge_bases = []
    
    kb1 = KnowledgeBase(
        id=str(uuid.uuid4()),
        name="General Documents",
        description="General document processing and knowledge base",
        owner_id=None,  # System-owned
        is_public=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    knowledge_bases.append(kb1)
    
    kb2 = KnowledgeBase(
        id=str(uuid.uuid4()),
        name="Legal Documents",
        description="Legal document processing and compliance",
        owner_id=None,
        is_public=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    knowledge_bases.append(kb2)
    
    session.add_all(knowledge_bases)
    await session.commit()
    
    print(f"Created {len(knowledge_bases)} sample knowledge bases")
    return knowledge_bases


async def create_sample_documents(session: AsyncSession, users: List[User], knowledge_bases: List[KnowledgeBase]) -> List[Document]:
    """Create sample documents."""
    documents = []
    
    # Sample document 1
    doc1 = Document(
        id=str(uuid.uuid4()),
        title="Sample Research Paper",
        description="A sample research paper for testing document processing",
        file_path="/uploads/sample_research.pdf",
        file_size=1024000,
        mime_type="application/pdf",
        status="completed",
        uploaded_by=users[1].id,  # Regular user
        knowledge_base_id=knowledge_bases[0].id,
        metadata={
            "author": "Dr. Jane Smith",
            "page_count": 15,
            "language": "en",
            "document_type": "pdf"
        },
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    documents.append(doc1)
    
    # Sample document 2
    doc2 = Document(
        id=str(uuid.uuid4()),
        title="Legal Contract Template",
        description="Standard legal contract template",
        file_path="/uploads/legal_contract.docx",
        file_size=512000,
        mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        status="processing",
        uploaded_by=users[0].id,  # Admin user
        knowledge_base_id=knowledge_bases[1].id,
        metadata={
            "author": "Legal Department",
            "page_count": 8,
            "language": "en",
            "document_type": "docx"
        },
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    documents.append(doc2)
    
    session.add_all(documents)
    await session.commit()
    
    print(f"Created {len(documents)} sample documents")
    return documents


async def create_sample_processing_queue(session: AsyncSession, documents: List[Document]) -> List[ProcessingQueue]:
    """Create sample processing queue entries."""
    queue_entries = []
    
    # Completed processing
    entry1 = ProcessingQueue(
        id=str(uuid.uuid4()),
        document_id=documents[0].id,
        status="completed",
        priority="medium",
        processing_steps=[
            {"step": "file_validation", "status": "completed", "timestamp": datetime.utcnow().isoformat()},
            {"step": "content_extraction", "status": "completed", "timestamp": datetime.utcnow().isoformat()},
            {"step": "entity_recognition", "status": "completed", "timestamp": datetime.utcnow().isoformat()},
            {"step": "knowledge_base_indexing", "status": "completed", "timestamp": datetime.utcnow().isoformat()}
        ],
        current_step="knowledge_base_indexing",
        progress_percentage=100,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    queue_entries.append(entry1)
    
    # In progress processing
    entry2 = ProcessingQueue(
        id=str(uuid.uuid4()),
        document_id=documents[1].id,
        status="processing",
        priority="high",
        processing_steps=[
            {"step": "file_validation", "status": "completed", "timestamp": datetime.utcnow().isoformat()},
            {"step": "content_extraction", "status": "processing", "timestamp": datetime.utcnow().isoformat()}
        ],
        current_step="content_extraction",
        progress_percentage=35,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    queue_entries.append(entry2)
    
    session.add_all(queue_entries)
    await session.commit()
    
    print(f"Created {len(queue_entries)} sample processing queue entries")
    return queue_entries


async def create_sample_validation_queue(session: AsyncSession, documents: List[Document], users: List[User]) -> List[ValidationQueue]:
    """Create sample validation queue entries."""
    validation_entries = []
    
    # Pending validation
    entry1 = ValidationQueue(
        id=str(uuid.uuid4()),
        document_id=documents[0].id,
        assigned_to=users[2].id,  # Validator
        status="pending",
        priority="medium",
        validation_criteria=[
            {"criteria": "content_accuracy", "weight": 0.4},
            {"criteria": "entity_recognition", "weight": 0.3},
            {"criteria": "format_compliance", "weight": 0.3}
        ],
        due_date=datetime.utcnow() + timedelta(days=3),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    validation_entries.append(entry1)
    
    session.add_all(validation_entries)
    await session.commit()
    
    print(f"Created {len(validation_entries)} sample validation queue entries")
    return validation_entries


async def main():
    """Main seeding function."""
    print("Starting database seeding...")
    
    async for session in get_async_session():
        try:
            # Create sample data
            users = await create_sample_users(session)
            knowledge_bases = await create_sample_knowledge_bases(session)
            documents = await create_sample_documents(session, users, knowledge_bases)
            processing_queue = await create_sample_processing_queue(session, documents)
            validation_queue = await create_sample_validation_queue(session, documents, users)
            
            print("Database seeding completed successfully!")
            print(f"Created: {len(users)} users, {len(knowledge_bases)} knowledge bases, "
                  f"{len(documents)} documents, {len(processing_queue)} processing entries, "
                  f"{len(validation_queue)} validation entries")
            
        except Exception as e:
            print(f"Error during seeding: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


if __name__ == "__main__":
    asyncio.run(main())
