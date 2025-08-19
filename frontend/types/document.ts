export interface Document {
  id: string;
  filename: string;
  original_filename: string;
  file_size: number;
  file_type: string;
  mime_type: string;
  status: DocumentStatus;
  processing_status: ProcessingStatus;
  document_type?: DocumentType;
  category?: string;
  tags: string[];
  metadata: DocumentMetadata;
  extracted_data?: ExtractedData;
  processing_results?: ProcessingResults;
  validation_status: ValidationStatus;
  created_by: string;
  created_at: string;
  updated_at: string;
  processed_at?: string;
  file_url?: string;
  thumbnail_url?: string;
  pages_count?: number;
  confidence_score?: number;
  ai_insights?: AIInsights;
}

export type DocumentStatus = 'uploaded' | 'processing' | 'processed' | 'failed' | 'archived' | 'deleted';

export type ProcessingStatus = 'pending' | 'ocr_processing' | 'nlp_processing' | 'classification' | 'extraction' | 'completed' | 'failed';

export type DocumentType = 
  | 'invoice' 
  | 'receipt' 
  | 'contract' 
  | 'report' 
  | 'form' 
  | 'letter' 
  | 'email' 
  | 'presentation' 
  | 'spreadsheet' 
  | 'image' 
  | 'other';

export type ValidationStatus = 'pending' | 'assigned' | 'in_progress' | 'validated' | 'rejected' | 'requires_review';

export interface DocumentMetadata {
  title?: string;
  author?: string;
  subject?: string;
  keywords?: string[];
  language?: string;
  page_count?: number;
  creation_date?: string;
  modification_date?: string;
  custom_fields?: Record<string, any>;
}

export interface ExtractedData {
  text_content: string;
  structured_data: Record<string, any>;
  entities: Entity[];
  tables: Table[];
  images: ExtractedImage[];
  signatures: Signature[];
  dates: DateEntity[];
  amounts: AmountEntity[];
  addresses: AddressEntity[];
  confidence_scores: Record<string, number>;
}

export interface Entity {
  id: string;
  type: string;
  value: string;
  confidence: number;
  bounding_box?: BoundingBox;
  page_number?: number;
}

export interface Table {
  id: string;
  headers: string[];
  rows: string[][];
  bounding_box: BoundingBox;
  page_number: number;
  confidence: number;
}

export interface ExtractedImage {
  id: string;
  type: 'chart' | 'diagram' | 'photo' | 'logo' | 'signature' | 'other';
  bounding_box: BoundingBox;
  page_number: number;
  description?: string;
  confidence: number;
}

export interface Signature {
  id: string;
  signer_name?: string;
  bounding_box: BoundingBox;
  page_number: number;
  confidence: number;
  is_digital: boolean;
}

export interface DateEntity {
  id: string;
  value: string;
  type: 'creation' | 'modification' | 'due' | 'effective' | 'expiration' | 'other';
  confidence: number;
  bounding_box?: BoundingBox;
  page_number?: number;
}

export interface AmountEntity {
  id: string;
  value: number;
  currency: string;
  type: 'total' | 'subtotal' | 'tax' | 'discount' | 'other';
  confidence: number;
  bounding_box?: BoundingBox;
  page_number?: number;
}

export interface AddressEntity {
  id: string;
  type: 'sender' | 'recipient' | 'billing' | 'shipping' | 'other';
  street?: string;
  city?: string;
  state?: string;
  zip_code?: string;
  country?: string;
  confidence: number;
  bounding_box?: BoundingBox;
  page_number?: number;
}

export interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface ProcessingResults {
  ocr_results: OCRResults;
  nlp_results: NLPResults;
  classification_results: ClassificationResults;
  extraction_results: ExtractionResults;
  quality_metrics: QualityMetrics;
  processing_time: number;
  ai_model_used: string;
  model_version: string;
}

export interface OCRResults {
  text_confidence: number;
  layout_confidence: number;
  language_detected: string;
  text_blocks: TextBlock[];
  processing_time: number;
}

export interface TextBlock {
  id: string;
  text: string;
  confidence: number;
  bounding_box: BoundingBox;
  page_number: number;
  font_info?: FontInfo;
}

export interface FontInfo {
  family: string;
  size: number;
  weight: string;
  style: string;
  color: string;
}

export interface NLPResults {
  entities: NLPEntity[];
  sentiment: SentimentAnalysis;
  topics: Topic[];
  key_phrases: string[];
  language: string;
  processing_time: number;
}

export interface NLPEntity {
  text: string;
  type: string;
  confidence: number;
  metadata?: Record<string, any>;
}

export interface SentimentAnalysis {
  overall: 'positive' | 'negative' | 'neutral';
  score: number;
  details: Record<string, number>;
}

export interface Topic {
  name: string;
  confidence: number;
  keywords: string[];
}

export interface ClassificationResults {
  document_type: DocumentType;
  confidence: number;
  alternative_types: Array<{
    type: DocumentType;
    confidence: number;
  }>;
  category: string;
  subcategory?: string;
  processing_time: number;
}

export interface ExtractionResults {
  fields: ExtractedField[];
  tables: ExtractedTable[];
  forms: ExtractedForm[];
  processing_time: number;
}

export interface ExtractedField {
  name: string;
  value: string;
  confidence: number;
  bounding_box?: BoundingBox;
  page_number?: number;
  field_type: string;
}

export interface ExtractedTable {
  id: string;
  name?: string;
  headers: string[];
  rows: ExtractedTableRow[];
  bounding_box: BoundingBox;
  page_number: number;
  confidence: number;
}

export interface ExtractedTableRow {
  id: string;
  cells: ExtractedTableCell[];
}

export interface ExtractedTableCell {
  value: string;
  confidence: number;
  bounding_box: BoundingBox;
}

export interface ExtractedForm {
  id: string;
  name: string;
  fields: ExtractedField[];
  bounding_box: BoundingBox;
  page_number: number;
  confidence: number;
}

export interface QualityMetrics {
  overall_quality: number;
  text_quality: number;
  image_quality: number;
  layout_quality: number;
  confidence_threshold: number;
  quality_issues: QualityIssue[];
}

export interface QualityIssue {
  type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  suggestion?: string;
}

export interface AIInsights {
  summary: string;
  key_points: string[];
  action_items: ActionItem[];
  risk_assessment?: RiskAssessment;
  compliance_check?: ComplianceCheck;
  processing_time: number;
}

export interface ActionItem {
  id: string;
  description: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  due_date?: string;
  assigned_to?: string;
  status: 'pending' | 'in_progress' | 'completed';
}

export interface RiskAssessment {
  overall_risk: 'low' | 'medium' | 'high';
  risk_score: number;
  risk_factors: RiskFactor[];
  recommendations: string[];
}

export interface RiskFactor {
  factor: string;
  risk_level: 'low' | 'medium' | 'high';
  description: string;
  impact: string;
}

export interface ComplianceCheck {
  compliant: boolean;
  compliance_score: number;
  violations: ComplianceViolation[];
  recommendations: string[];
}

export interface ComplianceViolation {
  rule: string;
  severity: 'low' | 'medium' | 'high';
  description: string;
  impact: string;
}

export interface DocumentUploadRequest {
  file: File;
  metadata?: Partial<DocumentMetadata>;
  tags?: string[];
  category?: string;
  priority?: 'low' | 'medium' | 'high';
}

export interface DocumentUpdateRequest {
  filename?: string;
  tags?: string[];
  category?: string;
  metadata?: Partial<DocumentMetadata>;
}

export interface DocumentFilter {
  status?: DocumentStatus[];
  type?: DocumentType[];
  category?: string[];
  tags?: string[];
  date_range?: {
    start: string;
    end: string;
  };
  file_size?: {
    min: number;
    max: number;
  };
  confidence_score?: {
    min: number;
    max: number;
  };
}

export interface DocumentSearchParams {
  query: string;
  filters?: DocumentFilter;
  page?: number;
  limit?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface DocumentStats {
  total_documents: number;
  documents_by_status: Record<DocumentStatus, number>;
  documents_by_type: Record<DocumentType, number>;
  total_file_size: number;
  average_processing_time: number;
  average_confidence_score: number;
  processing_success_rate: number;
}
