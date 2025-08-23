"""
Seed Tenant Data for DocuMind™
Creates sample tenants and users for testing multi-tenant functionality
"""

import asyncio
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.tenant import Tenant
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from app.core.tenant_middleware import create_tenant_policies
import logging

logger = logging.getLogger(__name__)

def create_sample_tenants(db: Session):
    """Create sample tenants for testing"""
    
    tenants = [
        {
            "name": "Acme Corporation",
            "slug": "acme-corp",
            "domain": "acme.documind.com",
            "max_users": 50,
            "max_documents": 5000,
            "max_storage_gb": 100,
            "default_embedding_model": "text-embedding-3-large",
            "default_llm_provider": "openai",
            "citation_confidence_threshold": 85,
            "require_2fa": False,
            "session_timeout_minutes": 480,
            "audit_logging_enabled": True,
            "data_retention_days": 2555,
            "compliance_frameworks": ["SOC2", "GDPR"]
        },
        {
            "name": "TechStart Inc",
            "slug": "techstart",
            "domain": "techstart.documind.com",
            "max_users": 25,
            "max_documents": 2500,
            "max_storage_gb": 50,
            "default_embedding_model": "text-embedding-ada-002",
            "default_llm_provider": "anthropic",
            "citation_confidence_threshold": 80,
            "require_2fa": True,
            "session_timeout_minutes": 240,
            "audit_logging_enabled": True,
            "data_retention_days": 1825,
            "compliance_frameworks": ["GDPR"]
        },
        {
            "name": "Legal Associates LLP",
            "slug": "legal-associates",
            "domain": "legal.documind.com",
            "max_users": 100,
            "max_documents": 10000,
            "max_storage_gb": 200,
            "default_embedding_model": "text-embedding-3-large",
            "default_llm_provider": "openai",
            "citation_confidence_threshold": 90,
            "require_2fa": True,
            "session_timeout_minutes": 120,
            "audit_logging_enabled": True,
            "data_retention_days": 3650,
            "compliance_frameworks": ["SOC2", "GDPR", "HIPAA"]
        }
    ]
    
    created_tenants = []
    for tenant_data in tenants:
        # Check if tenant already exists
        existing_tenant = db.query(Tenant).filter(
            Tenant.slug == tenant_data["slug"]
        ).first()
        
        if existing_tenant:
            logger.info(f"Tenant {tenant_data['name']} already exists, skipping...")
            created_tenants.append(existing_tenant)
            continue
        
        tenant = Tenant(**tenant_data)
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        
        logger.info(f"Created tenant: {tenant.name} (ID: {tenant.id})")
        created_tenants.append(tenant)
    
    return created_tenants

def create_sample_users(db: Session, tenants: list):
    """Create sample users for each tenant"""
    
    users_data = [
        {
            "email": "admin@acme-corp.com",
            "username": "acme_admin",
            "full_name": "Acme Admin",
            "role": UserRole.ADMIN,
            "tenant_slug": "acme-corp"
        },
        {
            "email": "user@acme-corp.com",
            "username": "acme_user",
            "full_name": "Acme User",
            "role": UserRole.USER,
            "tenant_slug": "acme-corp"
        },
        {
            "email": "validator@acme-corp.com",
            "username": "acme_validator",
            "full_name": "Acme Validator",
            "role": UserRole.VALIDATOR,
            "tenant_slug": "acme-corp"
        },
        {
            "email": "admin@techstart.com",
            "username": "techstart_admin",
            "full_name": "TechStart Admin",
            "role": UserRole.ADMIN,
            "tenant_slug": "techstart"
        },
        {
            "email": "user@techstart.com",
            "username": "techstart_user",
            "full_name": "TechStart User",
            "role": UserRole.USER,
            "tenant_slug": "techstart"
        },
        {
            "email": "admin@legal-associates.com",
            "username": "legal_admin",
            "full_name": "Legal Admin",
            "role": UserRole.ADMIN,
            "tenant_slug": "legal-associates"
        },
        {
            "email": "lawyer@legal-associates.com",
            "username": "legal_lawyer",
            "full_name": "Legal Lawyer",
            "role": UserRole.USER,
            "tenant_slug": "legal-associates"
        },
        {
            "email": "reviewer@legal-associates.com",
            "username": "legal_reviewer",
            "full_name": "Legal Reviewer",
            "role": UserRole.VALIDATOR,
            "tenant_slug": "legal-associates"
        }
    ]
    
    created_users = []
    for user_data in users_data:
        # Find tenant
        tenant = next((t for t in tenants if t.slug == user_data["tenant_slug"]), None)
        if not tenant:
            logger.warning(f"Tenant {user_data['tenant_slug']} not found, skipping user {user_data['email']}")
            continue
        
        # Check if user already exists
        existing_user = db.query(User).filter(
            User.email == user_data["email"]
        ).first()
        
        if existing_user:
            logger.info(f"User {user_data['email']} already exists, skipping...")
            created_users.append(existing_user)
            continue
        
        # Create user
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            full_name=user_data["full_name"],
            hashed_password=get_password_hash("password123"),  # Default password
            role=user_data["role"],
            tenant_id=tenant.id,
            is_active=True
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Created user: {user.email} (Role: {user.role.value}) in tenant: {tenant.name}")
        created_users.append(user)
    
    return created_users

def main():
    """Main function to seed tenant and user data"""
    db = SessionLocal()
    
    try:
        logger.info("Starting tenant and user data seeding...")
        
        # Create sample tenants
        tenants = create_sample_tenants(db)
        logger.info(f"Created {len(tenants)} tenants")
        
        # Create sample users
        users = create_sample_users(db, tenants)
        logger.info(f"Created {len(users)} users")
        
        # Create tenant policies
        create_tenant_policies(db)
        logger.info("Created tenant security policies")
        
        logger.info("Tenant and user data seeding completed successfully!")
        
    except Exception as e:
        logger.error(f"Error seeding tenant data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
