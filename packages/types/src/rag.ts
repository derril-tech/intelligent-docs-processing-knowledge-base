// RAG Pipeline Types

export interface DocumentChunk {
  id: number;
  documentId: number;
  chunkType: 'text' | 'table' | 'image' | 'header' | 'footer';
  content: string;
  contentHash: string;
  pageNumber?: number;
  startPosition?: number;
  endPosition?: number;
  embeddingModel: string;
  embedding?: number[];
  metadata?: Record<string, any>;
  tags?: string[];
  confidenceScore?: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface Citation {
  id: number;
  sourceChunkId: number;
  sourceDocumentId: number;
  answerId: number;
  spanStart?: number;
  spanEnd?: number;
  confidenceScore: number;
  citationType: 'direct' | 'indirect' | 'reference';
  createdAt: Date;
}

export interface Answer {
  id: number;
  question: string;
  answerText: string;
  answerHash: string;
  modelUsed: string;
  promptTemplate?: string;
  contextChunksUsed?: number[];
  confidenceScore?: number;
  factualityScore?: number;
  citationCount: number;
  userId: number;
  sessionId?: string;
  createdAt: Date;
  citations?: Citation[];
}

export interface QuestionRequest {
  question: string;
  context?: string;
  maxCitations?: number;
}

export interface AnswerResponse {
  answer: string;
  citations: CitationResponse[];
  confidenceScore: number;
  answerId: number;
  modelUsed: string;
  processingTimeMs?: number;
  createdAt?: Date;
}

export interface CitationResponse {
  chunkId: number;
  documentId: number;
  spanStart?: number;
  spanEnd?: number;
  confidence: number;
  contentPreview?: string;
}

export interface ChunkSearchRequest {
  query: string;
  limit?: number;
  scoreThreshold?: number;
  filters?: Record<string, any>;
}

export interface ChunkSearchResponse {
  content: string;
  metadata: Record<string, any>;
  score: number;
  documentId: number;
  chunkId: number;
}

export interface DocumentProcessingRequest {
  documentId: number;
  chunkSize?: number;
  chunkOverlap?: number;
  embeddingModel?: string;
}

export interface DocumentProcessingResponse {
  message: string;
  chunksCreated: number;
  documentId: number;
  processingTimeMs?: number;
  embeddingModel: string;
}

export interface RAGStatsResponse {
  totalChunks: number;
  totalAnswers: number;
  totalCitations: number;
  avgConfidenceScore: number;
  mostUsedEmbeddingModel: string;
  mostUsedLlmModel: string;
}
