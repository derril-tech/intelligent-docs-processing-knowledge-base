"""Add RAG and multi-tenant support

Revision ID: 002
Revises: 001
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Create tenants table
    op.create_table('tenants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('domain', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('max_users', sa.Integer(), nullable=True),
        sa.Column('max_documents', sa.Integer(), nullable=True),
        sa.Column('max_storage_gb', sa.Integer(), nullable=True),
        sa.Column('default_embedding_model', sa.String(length=100), nullable=True),
        sa.Column('default_llm_provider', sa.String(length=50), nullable=True),
        sa.Column('citation_confidence_threshold', sa.Integer(), nullable=True),
        sa.Column('require_2fa', sa.Boolean(), nullable=True),
        sa.Column('session_timeout_minutes', sa.Integer(), nullable=True),
        sa.Column('password_policy', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('audit_logging_enabled', sa.Boolean(), nullable=True),
        sa.Column('data_retention_days', sa.Integer(), nullable=True),
        sa.Column('compliance_frameworks', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tenants_domain'), 'tenants', ['domain'], unique=True)
    op.create_index(op.f('ix_tenants_id'), 'tenants', ['id'], unique=False)
    op.create_index(op.f('ix_tenants_slug'), 'tenants', ['slug'], unique=True)

    # Add tenant_id to users table
    op.add_column('users', sa.Column('role', sa.Enum('admin', 'user', 'validator', 'viewer', name='userrole'), nullable=True))
    op.add_column('users', sa.Column('tenant_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'users', 'tenants', ['tenant_id'], ['id'])

    # Add tenant_id to documents table
    op.add_column('documents', sa.Column('tenant_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'documents', 'tenants', ['tenant_id'], ['id'])

    # Create document_chunks table
    op.create_table('document_chunks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('document_id', sa.Integer(), nullable=False),
        sa.Column('chunk_type', sa.Enum('text', 'table', 'image', 'header', 'footer', name='chunktype'), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('content_hash', sa.String(length=64), nullable=False),
        sa.Column('page_number', sa.Integer(), nullable=True),
        sa.Column('start_position', sa.Integer(), nullable=True),
        sa.Column('end_position', sa.Integer(), nullable=True),
        sa.Column('embedding_model', sa.String(length=100), nullable=False),
        sa.Column('embedding', postgresql.VECTOR(3072), nullable=True),
        sa.Column('embedding_updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('tags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_document_chunks_content_hash'), 'document_chunks', ['content_hash'], unique=False)
    op.create_index(op.f('ix_document_chunks_id'), 'document_chunks', ['id'], unique=False)

    # Create answers table
    op.create_table('answers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('answer_text', sa.Text(), nullable=False),
        sa.Column('answer_hash', sa.String(length=64), nullable=False),
        sa.Column('model_used', sa.String(length=100), nullable=False),
        sa.Column('prompt_template', sa.String(length=255), nullable=True),
        sa.Column('context_chunks_used', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('factuality_score', sa.Float(), nullable=True),
        sa.Column('citation_count', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_answers_answer_hash'), 'answers', ['answer_hash'], unique=False)
    op.create_index(op.f('ix_answers_id'), 'answers', ['id'], unique=False)

    # Create citations table
    op.create_table('citations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_chunk_id', sa.Integer(), nullable=False),
        sa.Column('source_document_id', sa.Integer(), nullable=False),
        sa.Column('answer_id', sa.Integer(), nullable=False),
        sa.Column('span_start', sa.Integer(), nullable=True),
        sa.Column('span_end', sa.Integer(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('citation_type', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['answer_id'], ['answers.id'], ),
        sa.ForeignKeyConstraint(['source_chunk_id'], ['document_chunks.id'], ),
        sa.ForeignKeyConstraint(['source_document_id'], ['documents.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_citations_id'), 'citations', ['id'], unique=False)

    # Create vector indexes for similarity search
    op.execute('CREATE INDEX IF NOT EXISTS idx_document_chunks_embedding ON document_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)')

def downgrade():
    # Drop vector index
    op.execute('DROP INDEX IF EXISTS idx_document_chunks_embedding')
    
    # Drop citations table
    op.drop_index(op.f('ix_citations_id'), table_name='citations')
    op.drop_table('citations')
    
    # Drop answers table
    op.drop_index(op.f('ix_answers_id'), table_name='answers')
    op.drop_index(op.f('ix_answers_answer_hash'), table_name='answers')
    op.drop_table('answers')
    
    # Drop document_chunks table
    op.drop_index(op.f('ix_document_chunks_id'), table_name='document_chunks')
    op.drop_index(op.f('ix_document_chunks_content_hash'), table_name='document_chunks')
    op.drop_table('document_chunks')
    
    # Remove tenant_id from documents
    op.drop_constraint(None, 'documents', type_='foreignkey')
    op.drop_column('documents', 'tenant_id')
    
    # Remove tenant_id and role from users
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'tenant_id')
    op.drop_column('users', 'role')
    
    # Drop tenants table
    op.drop_index(op.f('ix_tenants_slug'), table_name='tenants')
    op.drop_index(op.f('ix_tenants_id'), table_name='tenants')
    op.drop_index(op.f('ix_tenants_domain'), table_name='tenants')
    op.drop_table('tenants')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS userrole')
    op.execute('DROP TYPE IF EXISTS chunktype')
