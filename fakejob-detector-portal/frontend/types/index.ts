export interface PredictionResult {
  is_fraudulent: boolean;
  confidence_score: number;
  risk_percentage: number;
  model_used: string;
  suspicious_phrases: Array<{ phrase: string; severity: string }>;
  explanation?: {
    feature_importance: Array<{ feature: string; importance: number }>;
    shap_summary: string;
  };
}

export interface JobPost {
  title: string;
  location?: string;
  department?: string;
  company_profile?: string;
  description: string;
  requirements?: string;
  benefits?: string;
  telecommuting: boolean;
  has_company_logo: boolean;
  has_questions: boolean;
  employment_type?: string;
  required_experience?: string;
  required_education?: string;
  industry?: string;
  function?: string;
}

export interface ApiJob {
  id: string;
  title: string;
  company: string;
  location: string;
  description: string;
  url: string;
  posted_at: string;
  source: string;
}

export interface PredictionLog {
  id: number;
  is_fraudulent: boolean;
  confidence_score: number;
  risk_percentage: number;
  model_used: string;
  suspicious_phrases: Array<{ phrase: string; severity: string }>;
  created_at: string;
}
