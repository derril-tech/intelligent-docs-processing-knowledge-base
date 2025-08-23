"""
Logging Configuration for DocuMind™
Provides structured logging with proper formatting and levels
"""

import logging
import sys
from typing import Any, Dict
from pathlib import Path
from app.core.config import settings

# Configure structured logging
def setup_logging(
    log_level: str = "INFO",
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    log_file: str = None
) -> None:
    """
    Setup application logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log message format
        log_file: Optional log file path
    """
    
    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file) if log_file else logging.NullHandler()
        ]
    )
    
    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("celery").setLevel(logging.INFO)
    logging.getLogger("redis").setLevel(logging.WARNING)
    logging.getLogger("elasticsearch").setLevel(logging.WARNING)
    
    # Set our app loggers to DEBUG in development
    if settings.DEBUG:
        logging.getLogger("app").setLevel(logging.DEBUG)

# Create logger instance
logger = logging.getLogger("app")

# Structured logging helpers
def log_event(
    event: str,
    level: str = "info",
    **kwargs: Any
) -> None:
    """
    Log a structured event with additional context.
    
    Args:
        event: Event name/description
        level: Log level
        **kwargs: Additional context data
    """
    log_func = getattr(logger, level.lower())
    
    # Format the message with context
    context_str = " ".join([f"{k}={v}" for k, v in kwargs.items()])
    message = f"{event} {context_str}".strip()
    
    log_func(message)

def log_api_request(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    user_id: str = None,
    tenant_id: str = None,
    **kwargs: Any
) -> None:
    """
    Log API request details.
    
    Args:
        method: HTTP method
        path: Request path
        status_code: Response status code
        duration_ms: Request duration in milliseconds
        user_id: User ID (if authenticated)
        tenant_id: Tenant ID (if multi-tenant)
        **kwargs: Additional request context
    """
    level = "warning" if status_code >= 400 else "info"
    
    log_event(
        "api_request",
        level=level,
        method=method,
        path=path,
        status_code=status_code,
        duration_ms=duration_ms,
        user_id=user_id,
        tenant_id=tenant_id,
        **kwargs
    )

def log_document_processing(
    document_id: int,
    stage: str,
    status: str,
    duration_ms: float = None,
    error: str = None,
    **kwargs: Any
) -> None:
    """
    Log document processing events.
    
    Args:
        document_id: Document ID
        stage: Processing stage
        status: Processing status
        duration_ms: Processing duration in milliseconds
        error: Error message (if any)
        **kwargs: Additional processing context
    """
    level = "error" if error else "info"
    
    log_event(
        "document_processing",
        level=level,
        document_id=document_id,
        stage=stage,
        status=status,
        duration_ms=duration_ms,
        error=error,
        **kwargs
    )

def log_rag_query(
    query: str,
    answer_length: int,
    citation_count: int,
    confidence_score: float,
    duration_ms: float,
    user_id: str = None,
    **kwargs: Any
) -> None:
    """
    Log RAG query events.
    
    Args:
        query: User query
        answer_length: Length of generated answer
        citation_count: Number of citations
        confidence_score: Confidence score
        duration_ms: Query duration in milliseconds
        user_id: User ID
        **kwargs: Additional query context
    """
    log_event(
        "rag_query",
        level="info",
        query_length=len(query),
        answer_length=answer_length,
        citation_count=citation_count,
        confidence_score=confidence_score,
        duration_ms=duration_ms,
        user_id=user_id,
        **kwargs
    )

def log_security_event(
    event_type: str,
    user_id: str = None,
    ip_address: str = None,
    details: str = None,
    **kwargs: Any
) -> None:
    """
    Log security-related events.
    
    Args:
        event_type: Type of security event
        user_id: User ID (if applicable)
        ip_address: IP address
        details: Event details
        **kwargs: Additional security context
    """
    log_event(
        "security_event",
        level="warning",
        event_type=event_type,
        user_id=user_id,
        ip_address=ip_address,
        details=details,
        **kwargs
    )

def log_performance_metric(
    metric_name: str,
    value: float,
    unit: str = None,
    tags: Dict[str, str] = None,
    **kwargs: Any
) -> None:
    """
    Log performance metrics.
    
    Args:
        metric_name: Name of the metric
        value: Metric value
        unit: Unit of measurement
        tags: Additional tags
        **kwargs: Additional metric context
    """
    log_event(
        "performance_metric",
        level="info",
        metric_name=metric_name,
        value=value,
        unit=unit,
        tags=tags,
        **kwargs
    )

# Initialize logging on module import
setup_logging(
    log_level=settings.LOG_LEVEL,
    log_file=settings.LOG_FILE if hasattr(settings, 'LOG_FILE') else None
)
