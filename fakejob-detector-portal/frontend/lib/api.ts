import axios from "axios";
import { PredictionResult, JobPost, PredictionLog, ApiJob } from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api/backend";

const api = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

export async function predictStructured(job: JobPost): Promise<PredictionResult> {
  const { data } = await api.post<PredictionResult>("/predict/structured", job);
  return data;
}

export async function predictUrl(url: string): Promise<{
  scraped_data: JobPost;
  prediction: PredictionResult;
  explanation: any;
}> {
  const { data } = await api.post("/predict/url", { url });
  return data;
}

export async function fetchJobs(): Promise<ApiJob[]> {
  const { data } = await api.get("/jobs/");
  return data;
}

export async function fetchPredictionHistory(): Promise<PredictionLog[]> {
  const { data } = await api.get("/jobs/");
  return data;
}
