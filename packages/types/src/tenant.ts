// Multi-Tenant Types

export interface Tenant {
  id: number;
  name: string;
  slug: string;
  domain?: string;
  isActive: boolean;
  maxUsers: number;
  maxDocuments: number;
  maxStorageGb: number;
  defaultEmbeddingModel: string;
  defaultLlmProvider: string;
  citationConfidenceThreshold: number;
  require2fa: boolean;
  sessionTimeoutMinutes: number;
  passwordPolicy?: Record<string, any>;
  auditLoggingEnabled: boolean;
  dataRetentionDays: number;
  complianceFrameworks: string[];
  createdAt: Date;
  updatedAt: Date;
}

export interface TenantCreate {
  name: string;
  slug: string;
  domain?: string;
  maxUsers?: number;
  maxDocuments?: number;
  maxStorageGb?: number;
  defaultEmbeddingModel?: string;
  defaultLlmProvider?: string;
  citationConfidenceThreshold?: number;
  require2fa?: boolean;
  sessionTimeoutMinutes?: number;
  passwordPolicy?: Record<string, any>;
  auditLoggingEnabled?: boolean;
  dataRetentionDays?: number;
  complianceFrameworks?: string[];
}

export interface TenantUpdate {
  name?: string;
  domain?: string;
  isActive?: boolean;
  maxUsers?: number;
  maxDocuments?: number;
  maxStorageGb?: number;
  defaultEmbeddingModel?: string;
  defaultLlmProvider?: string;
  citationConfidenceThreshold?: number;
  require2fa?: boolean;
  sessionTimeoutMinutes?: number;
  passwordPolicy?: Record<string, any>;
  auditLoggingEnabled?: boolean;
  dataRetentionDays?: number;
  complianceFrameworks?: string[];
}

export interface TenantUsageStats {
  userCount: number;
  documentCount: number;
  totalStorageGb: number;
  chunkCount: number;
  answerCount: number;
}

export interface TenantLimits {
  maxUsers: number;
  maxDocuments: number;
  maxStorageGb: number;
  currentUsers: number;
  currentDocuments: number;
  currentStorageGb: number;
}

export interface TenantConfiguration {
  embeddingModel: string;
  llmProvider: string;
  citationThreshold: number;
  securitySettings: {
    require2fa: boolean;
    sessionTimeout: number;
    passwordPolicy: Record<string, any>;
  };
  complianceSettings: {
    auditLogging: boolean;
    dataRetention: number;
    frameworks: string[];
  };
}
