import { BaseEntity, ProcessingStatus, FileInfo, ProcessingProgress } from './common';

export interface Document extends BaseEntity {
  title: string;
  description?: string;
  file_info: FileInfo;
  status: ProcessingStatus;
  processing_progress: ProcessingProgress;
  metadata: DocumentMetadata;
  tags: string[];
  uploaded_by: string;
  knowledge_base_id?: string;
  extracted_content?: ExtractedContent;
  processing_history: ProcessingEvent[];
}

export interface DocumentMetadata {
  author?: string;
  creation_date?: string;
  modification_date?: string;
  page_count?: number;
  language?: string;
  document_type: DocumentType;
  confidence_score?: number;
  custom_fields?: Record<string, any>;
}

export type DocumentType = 
  | 'pdf'
  | 'docx'
  | 'txt'
  | 'csv'
  | 'image'
  | 'presentation'
  | 'spreadsheet'
  | 'other';

export interface ExtractedContent {
  text_content: string;
  structured_data?: Record<string, any>;
  entities: Entity[];
  relationships: Relationship[];
  summary?: string;
  key_points: string[];
  tables: Table[];
  images: ImageReference[];
}

export interface Entity {
  id: string;
  name: string;
  type: EntityType;
  confidence: number;
  position: Position;
  metadata?: Record<string, any>;
}

export type EntityType = 
  | 'person'
  | 'organization'
  | 'location'
  | 'date'
  | 'money'
  | 'percentage'
  | 'email'
  | 'phone'
  | 'url'
  | 'custom';

export interface Position {
  page: number;
  start: number;
  end: number;
  bounding_box?: [number, number, number, number];
}

export interface Relationship {
  id: string;
  source_entity_id: string;
  target_entity_id: string;
  relationship_type: string;
  confidence: number;
  metadata?: Record<string, any>;
}

export interface Table {
  id: string;
  page: number;
  headers: string[];
  rows: string[][];
  bounding_box: [number, number, number, number];
}

export interface ImageReference {
  id: string;
  page: number;
  description?: string;
  bounding_box: [number, number, number, number];
  extracted_text?: string;
}

export interface ProcessingEvent extends BaseEntity {
  event_type: ProcessingEventType;
  status: ProcessingStatus;
  message: string;
  details?: Record<string, any>;
  duration_ms?: number;
}

export type ProcessingEventType = 
  | 'upload_started'
  | 'file_validation'
  | 'content_extraction'
  | 'entity_recognition'
  | 'relationship_extraction'
  | 'knowledge_base_indexing'
  | 'processing_completed'
  | 'processing_failed';

export interface DocumentUploadRequest {
  file: File;
  title: string;
  description?: string;
  tags?: string[];
  knowledge_base_id?: string;
  metadata?: Partial<DocumentMetadata>;
}

export interface DocumentUpdateRequest {
  title?: string;
  description?: string;
  tags?: string[];
  metadata?: Partial<DocumentMetadata>;
}

export interface DocumentSearchRequest {
  query: string;
  filters?: DocumentSearchFilters;
  pagination: {
    page: number;
    size: number;
  };
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface DocumentSearchFilters {
  status?: ProcessingStatus[];
  document_type?: DocumentType[];
  tags?: string[];
  uploaded_by?: string;
  date_range?: {
    start: string;
    end: string;
  };
  knowledge_base_id?: string;
}
