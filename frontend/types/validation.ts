export interface ValidationTask {
  id: string;
  document: {
    id: string;
    filename: string;
    document_type: string;
    file_size: number;
    uploaded_at: string;
  };
  field_name: string;
  extracted_value: string;
  ai_confidence: number;
  status: ValidationStatus;
  assigned_to?: string;
  assigned_at: string;
  completed_at?: string;
  validation_result?: ValidationResult;
  notes?: string;
  priority: "low" | "medium" | "high";
  created_at: string;
  updated_at: string;
}

export type ValidationStatus = "pending" | "in_progress" | "completed" | "rejected";

export interface ValidationResult {
  validation_result: "correct" | "incorrect" | "partially_correct";
  confidence_level: "high" | "medium" | "low";
  corrected_value?: string;
  notes?: string;
  submitted_at: string;
  submitted_by: string;
}

export interface ValidationQueue {
  tasks: ValidationTask[];
  total_count: number;
  pending_count: number;
  in_progress_count: number;
  completed_count: number;
  rejected_count: number;
}

export interface ValidationStats {
  total_tasks: number;
  completed_tasks: number;
  accuracy_rate: number;
  average_processing_time: number;
  tasks_by_status: Record<ValidationStatus, number>;
  tasks_by_priority: Record<string, number>;
}

export interface ValidationAssignmentRequest {
  task_id: string;
  assigned_to: string;
}

export interface ValidationSubmissionRequest {
  validation_result: "correct" | "incorrect" | "partially_correct";
  confidence_level: "high" | "medium" | "low";
  corrected_value?: string;
  notes?: string;
}

export interface ValidationFilter {
  status?: ValidationStatus[];
  priority?: string[];
  document_type?: string[];
  assigned_to?: string;
  date_range?: string;
  field_name?: string;
}

export interface ValidationSearchParams {
  query?: string;
  filters?: ValidationFilter;
  limit?: number;
  offset?: number;
  sort_by?: string;
  sort_order?: "asc" | "desc";
}
