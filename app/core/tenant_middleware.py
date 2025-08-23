"""
Multi-Tenant Security Middleware for DocuMind™
Implements tenant isolation and row-level security
"""

from typing import Optional
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.models.user import User
from app.models.tenant import Tenant
from app.core.security import get_current_user
import logging

logger = logging.getLogger(__name__)

class TenantMiddleware:
    """Middleware for handling multi-tenant security"""
    
    def __init__(self):
        self.tenant_header = "X-Tenant-ID"
        self.tenant_domain_header = "X-Tenant-Domain"
    
    async def __call__(self, request: Request, call_next):
        """Process request with tenant context"""
        # Extract tenant information
        tenant_id = request.headers.get(self.tenant_header)
        tenant_domain = request.headers.get(self.tenant_domain_header)
        
        # Set tenant context
        request.state.tenant_id = tenant_id
        request.state.tenant_domain = tenant_domain
        
        # Continue processing
        response = await call_next(request)
        return response

def get_current_tenant(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Tenant:
    """Get current tenant for the authenticated user"""
    tenant_id = request.state.tenant_id
    
    if not tenant_id:
        raise HTTPException(
            status_code=400,
            detail="Tenant ID is required"
        )
    
    # Verify tenant exists and user has access
    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id,
        Tenant.is_active == True
    ).first()
    
    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )
    
    # Verify user belongs to this tenant
    if current_user.tenant_id != tenant_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied to this tenant"
        )
    
    return tenant

def set_tenant_context(db: Session, tenant_id: int):
    """Set tenant context for database operations"""
    # Set tenant context for row-level security
    db.execute(text(f"SET app.current_tenant_id = {tenant_id}"))

def create_tenant_policies(db: Session):
    """Create row-level security policies for multi-tenant isolation"""
    
    # Enable RLS on all tables
    tables = [
        "users", "documents", "document_chunks", "answers", 
        "citations", "knowledge_base_entries", "validation_tasks"
    ]
    
    for table in tables:
        # Enable RLS
        db.execute(text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY"))
        
        # Create tenant isolation policy
        policy_sql = f"""
        CREATE POLICY tenant_isolation_{table} ON {table}
        FOR ALL USING (tenant_id = current_setting('app.current_tenant_id')::integer)
        """
        
        try:
            db.execute(text(policy_sql))
        except Exception as e:
            logger.warning(f"Policy for {table} may already exist: {e}")
    
    db.commit()

def create_tenant(
    db: Session,
    name: str,
    slug: str,
    domain: Optional[str] = None,
    max_users: int = 100,
    max_documents: int = 10000,
    max_storage_gb: int = 100
) -> Tenant:
    """Create a new tenant"""
    
    tenant = Tenant(
        name=name,
        slug=slug,
        domain=domain,
        max_users=max_users,
        max_documents=max_documents,
        max_storage_gb=max_storage_gb,
        default_embedding_model="text-embedding-3-large",
        default_llm_provider="openai",
        citation_confidence_threshold=85,
        require_2fa=False,
        session_timeout_minutes=480,
        audit_logging_enabled=True,
        data_retention_days=2555,
        compliance_frameworks=["SOC2", "GDPR"]
    )
    
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    
    return tenant

def check_tenant_limits(
    db: Session,
    tenant: Tenant,
    check_type: str,
    current_count: int = 0
) -> bool:
    """Check if tenant has reached their limits"""
    
    if check_type == "users":
        return current_count < tenant.max_users
    elif check_type == "documents":
        return current_count < tenant.max_documents
    elif check_type == "storage":
        # Calculate current storage usage
        storage_query = """
        SELECT COALESCE(SUM(file_size), 0) as total_size
        FROM documents 
        WHERE tenant_id = :tenant_id
        """
        result = db.execute(text(storage_query), {"tenant_id": tenant.id})
        current_storage_gb = result.scalar() / (1024 * 1024 * 1024)  # Convert to GB
        return current_storage_gb < tenant.max_storage_gb
    
    return True

def get_tenant_usage_stats(db: Session, tenant_id: int) -> dict:
    """Get usage statistics for a tenant"""
    
    stats_query = """
    SELECT 
        COUNT(DISTINCT u.id) as user_count,
        COUNT(DISTINCT d.id) as document_count,
        COALESCE(SUM(d.file_size), 0) as total_storage_bytes,
        COUNT(DISTINCT dc.id) as chunk_count,
        COUNT(DISTINCT a.id) as answer_count
    FROM tenants t
    LEFT JOIN users u ON u.tenant_id = t.id
    LEFT JOIN documents d ON d.tenant_id = t.id
    LEFT JOIN document_chunks dc ON dc.document_id = d.id
    LEFT JOIN answers a ON a.user_id = u.id
    WHERE t.id = :tenant_id
    GROUP BY t.id
    """
    
    result = db.execute(text(stats_query), {"tenant_id": tenant_id})
    row = result.fetchone()
    
    if not row:
        return {
            "user_count": 0,
            "document_count": 0,
            "total_storage_gb": 0,
            "chunk_count": 0,
            "answer_count": 0
        }
    
    return {
        "user_count": row.user_count,
        "document_count": row.document_count,
        "total_storage_gb": row.total_storage_bytes / (1024 * 1024 * 1024),
        "chunk_count": row.chunk_count,
        "answer_count": row.answer_count
    }
