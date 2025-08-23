import { BaseEntity, ValidationStatus } from './common';

export interface ValidationTask extends BaseEntity {
  document_id: string;
  assigned_to?: string;
  status: ValidationStatus;
  priority: ValidationPriority;
  task_type: ValidationTaskType;
  validation_criteria: ValidationCriteria[];
  results: ValidationResult[];
  comments: ValidationComment[];
  due_date?: string;
  completed_at?: string;
}

export type ValidationPriority = 'low' | 'medium' | 'high' | 'critical';

export type ValidationTaskType = 
  | 'content_accuracy'
  | 'entity_recognition'
  | 'relationship_validation'
  | 'data_quality'
  | 'compliance_check'
  | 'custom_validation';

export interface ValidationCriteria {
  id: string;
  name: string;
  description: string;
  criteria_type: ValidationCriteriaType;
  required: boolean;
  weight: number;
  validation_rules: ValidationRule[];
}

export type ValidationCriteriaType = 
  | 'text_accuracy'
  | 'entity_completeness'
  | 'relationship_consistency'
  | 'format_compliance'
  | 'business_rules'
  | 'custom';

export interface ValidationRule {
  id: string;
  rule_type: ValidationRuleType;
  parameters: Record<string, any>;
  description: string;
}

export type ValidationRuleType = 
  | 'required_field'
  | 'format_check'
  | 'range_validation'
  | 'pattern_match'
  | 'cross_reference'
  | 'custom_rule';

export interface ValidationResult {
  id: string;
  criteria_id: string;
  status: ValidationResultStatus;
  score: number;
  feedback: string;
  evidence: ValidationEvidence[];
  timestamp: string;
}

export type ValidationResultStatus = 'passed' | 'failed' | 'warning' | 'needs_review';

export interface ValidationEvidence {
  id: string;
  evidence_type: ValidationEvidenceType;
  content: string;
  location?: {
    page: number;
    position: [number, number, number, number];
  };
  confidence: number;
  metadata?: Record<string, any>;
}

export type ValidationEvidenceType = 
  | 'text_excerpt'
  | 'entity_highlight'
  | 'relationship_diagram'
  | 'data_table'
  | 'screenshot'
  | 'annotation';

export interface ValidationComment extends BaseEntity {
  author_id: string;
  content: string;
  type: CommentType;
  parent_comment_id?: string;
  attachments?: ValidationAttachment[];
}

export type CommentType = 'general' | 'correction' | 'question' | 'approval' | 'rejection';

export interface ValidationAttachment {
  id: string;
  filename: string;
  file_type: string;
  size: number;
  url: string;
}

export interface ValidationTaskRequest {
  document_id: string;
  assigned_to?: string;
  priority: ValidationPriority;
  task_type: ValidationTaskType;
  validation_criteria: string[];
  due_date?: string;
}

export interface ValidationResultRequest {
  task_id: string;
  results: {
    criteria_id: string;
    status: ValidationResultStatus;
    score: number;
    feedback: string;
    evidence?: ValidationEvidence[];
  }[];
  comments?: string;
}

export interface ValidationTaskSearchRequest {
  status?: ValidationStatus[];
  priority?: ValidationPriority[];
  task_type?: ValidationTaskType[];
  assigned_to?: string;
  document_id?: string;
  date_range?: {
    start: string;
    end: string;
  };
  pagination: {
    page: number;
    size: number;
  };
}
