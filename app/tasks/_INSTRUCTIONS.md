# Background Tasks Development Instructions

## Overview
This directory contains Celery background tasks for the DocuMind™ application. These tasks handle heavy operations like document processing, embedding generation, and batch operations that should not block the main application.

## CLAUDE_TASK: Task Development Guidelines

### 1. Task Architecture
- Use Celery for background task processing
- Implement proper error handling and retry logic
- Use Redis as message broker and result backend
- Follow task naming conventions

### 2. Task Design
- Keep tasks idempotent when possible
- Implement proper logging and monitoring
- Use task routing for different worker types
- Handle task cancellation gracefully

### 3. Performance Considerations
- Use async/await for I/O operations
- Implement task batching for efficiency
- Use task priorities for critical operations
- Monitor task queue health

### 4. Error Handling
- Implement exponential backoff for retries
- Log detailed error information
- Handle task timeouts appropriately
- Provide meaningful error messages

## File Structure
```
tasks/
├── document_processing.py    # Document processing tasks
├── ai_processing.py         # AI/ML processing tasks
├── validation_tasks.py      # Validation workflow tasks
├── search_tasks.py          # Search indexing tasks
├── maintenance_tasks.py     # System maintenance tasks
└── __init__.py             # Task registration
```

## Example Task Pattern
```python
from celery import Celery
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.core.celery import celery_app
from app.core.database import SessionLocal
from app.core.logging import logger
from app.services.rag_service import RAGService
from app.models.document import Document

@celery_app.task(
    bind=True,
    name="process_document",
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 3, 'countdown': 60},
    retry_backoff=True
)
def process_document_task(self, document_id: int) -> Dict[str, Any]:
    """
    Process a document through the complete pipeline.
    
    Args:
        document_id: ID of the document to process
        
    Returns:
        Dict containing processing results
        
    Raises:
        Exception: If processing fails after retries
    """
    logger.info(f"Starting document processing", 
               document_id=document_id, task_id=self.request.id)
    
    db = SessionLocal()
    try:
        # Get document
        document = db.query(Document).filter(
            Document.id == document_id
        ).first()
        
        if not document:
            raise ValueError(f"Document {document_id} not found")
        
        # Update status
        document.status = "processing"
        db.commit()
        
        # Process document
        rag_service = RAGService()
        
        # Step 1: Extract text content
        content = await extract_document_content(document.file_path)
        
        # Step 2: Create chunks and embeddings
        chunks = await rag_service.process_document(db, document, content)
        
        # Step 3: Index for search
        await index_document_chunks(db, chunks)
        
        # Update status
        document.status = "completed"
        document.processed_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Document processing completed", 
                   document_id=document_id, chunks_created=len(chunks))
        
        return {
            "document_id": document_id,
            "status": "completed",
            "chunks_created": len(chunks),
            "processing_time": time.time() - self.request.start_time
        }
        
    except Exception as e:
        logger.error(f"Document processing failed", 
                    document_id=document_id, error=str(e))
        
        # Update status
        if document:
            document.status = "failed"
            document.error_message = str(e)
            db.commit()
        
        # Re-raise for retry
        raise
        
    finally:
        db.close()

@celery_app.task(
    bind=True,
    name="generate_embeddings",
    queue="ai_processing"
)
def generate_embeddings_task(self, chunk_ids: List[int]) -> Dict[str, Any]:
    """
    Generate embeddings for document chunks.
    
    Args:
        chunk_ids: List of chunk IDs to process
        
    Returns:
        Dict containing embedding generation results
    """
    logger.info(f"Starting embedding generation", 
               chunk_count=len(chunk_ids), task_id=self.request.id)
    
    db = SessionLocal()
    try:
        rag_service = RAGService()
        processed_count = 0
        
        for chunk_id in chunk_ids:
            try:
                # Get chunk
                chunk = db.query(DocumentChunk).filter(
                    DocumentChunk.id == chunk_id
                ).first()
                
                if not chunk:
                    logger.warning(f"Chunk {chunk_id} not found")
                    continue
                
                # Generate embedding
                embedding = await rag_service.embeddings.aembed_query(chunk.content)
                
                # Update chunk
                chunk.embedding = embedding
                chunk.embedding_updated_at = datetime.utcnow()
                processed_count += 1
                
            except Exception as e:
                logger.error(f"Failed to process chunk {chunk_id}", error=str(e))
                continue
        
        db.commit()
        
        logger.info(f"Embedding generation completed", 
                   processed_count=processed_count, total_count=len(chunk_ids))
        
        return {
            "processed_count": processed_count,
            "total_count": len(chunk_ids),
            "success_rate": processed_count / len(chunk_ids) if chunk_ids else 0
        }
        
    finally:
        db.close()

@celery_app.task(
    bind=True,
    name="validate_document",
    queue="validation"
)
def validate_document_task(self, document_id: int, validator_id: int) -> Dict[str, Any]:
    """
    Create validation tasks for a document.
    
    Args:
        document_id: ID of the document to validate
        validator_id: ID of the assigned validator
        
    Returns:
        Dict containing validation task results
    """
    logger.info(f"Creating validation tasks", 
               document_id=document_id, validator_id=validator_id)
    
    db = SessionLocal()
    try:
        # Get document and chunks
        document = db.query(Document).filter(
            Document.id == document_id
        ).first()
        
        if not document:
            raise ValueError(f"Document {document_id} not found")
        
        chunks = db.query(DocumentChunk).filter(
            DocumentChunk.document_id == document_id
        ).all()
        
        # Create validation tasks for low-confidence chunks
        validation_tasks = []
        for chunk in chunks:
            if chunk.confidence_score and chunk.confidence_score < 0.8:
                task = ValidationTask(
                    document_id=document_id,
                    chunk_id=chunk.id,
                    assigned_user_id=validator_id,
                    priority="medium",
                    status="pending"
                )
                db.add(task)
                validation_tasks.append(task)
        
        db.commit()
        
        logger.info(f"Validation tasks created", 
                   task_count=len(validation_tasks))
        
        return {
            "document_id": document_id,
            "validation_tasks_created": len(validation_tasks),
            "total_chunks": len(chunks)
        }
        
    finally:
        db.close()
```

## CLAUDE_TASK: Implementation Checklist

### Document Processing Tasks
- [ ] Document upload and validation
- [ ] OCR and text extraction
- [ ] Document chunking
- [ ] Metadata extraction
- [ ] File format conversion
- [ ] Processing status updates

### AI Processing Tasks
- [ ] Embedding generation
- [ ] Document classification
- [ ] Entity extraction
- [ ] Sentiment analysis
- [ ] Quality assessment
- [ ] Model fine-tuning

### Validation Tasks
- [ ] Validation task creation
- [ ] Task assignment
- [ ] Validation result processing
- [ ] Confidence scoring
- [ ] Batch validation
- [ ] Audit trail updates

### Search Tasks
- [ ] Search index updates
- [ ] Vector index maintenance
- [ ] Search result caching
- [ ] Index optimization
- [ ] Search analytics
- [ ] Query logging

### Maintenance Tasks
- [ ] Database cleanup
- [ ] File storage cleanup
- [ ] Cache invalidation
- [ ] Performance monitoring
- [ ] Health checks
- [ ] Backup operations

## Task Configuration

### Celery Configuration
```python
# app/core/celery.py
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "documind",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.document_processing",
        "app.tasks.ai_processing",
        "app.tasks.validation_tasks",
        "app.tasks.search_tasks",
        "app.tasks.maintenance_tasks"
    ]
)

# Task configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    result_expires=3600,  # 1 hour
)
```

### Task Routing
```python
# Task routing configuration
CELERY_ROUTES = {
    'app.tasks.document_processing.*': {'queue': 'document_processing'},
    'app.tasks.ai_processing.*': {'queue': 'ai_processing'},
    'app.tasks.validation_tasks.*': {'queue': 'validation'},
    'app.tasks.search_tasks.*': {'queue': 'search'},
    'app.tasks.maintenance_tasks.*': {'queue': 'maintenance'},
}
```

## Error Handling Patterns

### Retry Logic
```python
@celery_app.task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_kwargs={'max_retries': 3, 'countdown': 60},
    retry_backoff=True
)
def task_with_retry(self, *args, **kwargs):
    """Task with automatic retry for transient errors."""
    pass
```

### Manual Retry
```python
@celery_app.task(bind=True)
def task_with_manual_retry(self, *args, **kwargs):
    """Task with manual retry logic."""
    try:
        # Task logic
        pass
    except TransientError as e:
        # Retry with exponential backoff
        countdown = 60 * (2 ** self.request.retries)
        raise self.retry(countdown=countdown, max_retries=3)
```

## Monitoring and Logging

### Task Monitoring
```python
import time
from celery.signals import task_prerun, task_postrun, task_failure

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **extras):
    """Log task start."""
    logger.info(f"Task started", 
               task_name=task.name, task_id=task_id)

@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, retval=None, state=None, **extras):
    """Log task completion."""
    logger.info(f"Task completed", 
               task_name=task.name, task_id=task_id, state=state)

@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, args=None, kwargs=None, traceback=None, einfo=None, **extras):
    """Log task failure."""
    logger.error(f"Task failed", 
                task_name=sender.name, task_id=task_id, exception=str(exception))
```

## Testing Requirements
- Unit tests for task logic
- Integration tests with Celery workers
- Mock external dependencies
- Test error conditions and retries
- Performance tests for heavy tasks

## Performance Considerations
- Use task batching for efficiency
- Implement proper task priorities
- Monitor queue lengths and processing times
- Use appropriate worker concurrency
- Implement task result caching
