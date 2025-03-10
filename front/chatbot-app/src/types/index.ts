// API Response Types
export interface ApiInfo {
  api_name: string;
  api_version: string;
  api_description: string;
  llm_provider: string;
  llm_model: string;
  db_engine: string;
  db_content: string;
}

export interface ChatSession {
  session_id: string;
  name: string;
  timestamp: string;
}

export interface ChatRequest {
  session_id: string;
  query: string;
  explanation_full: boolean;
  output_format: string;
  full_data: boolean;
}

export interface ChatResponse {
  user_query: string;
  sql_query: string;
  sql_explanation: string;
  business_explanation: string;
  download_link: string;
  query_time: string;
  response_time: string;
}

// UI State Types
export interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: string;
  metadata?: ChatResponse;
}

export interface ChatState {
  sessions: ChatSession[];
  activeSessionId: string | null;
  messages: Record<string, Message[]>;
  isLoading: boolean;
  error: string | null;
  apiInfo: ApiInfo | null;
}

export interface FormState {
  detailedAnswer: boolean;
  fileFormat: 'json' | 'csv';
  sampleData: boolean;
} 