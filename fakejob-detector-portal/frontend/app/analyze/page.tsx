import { JobAnalysisForm } from "@/components/job-analysis-form";

export default function AnalyzePage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <h1 className="mb-2 text-3xl font-bold">Analyze a Job Posting</h1>
      <p className="mb-8 text-muted-foreground">
        Paste a job description, URL, or screenshot to detect potential fraud using our ML models trained on real data.
      </p>
      <JobAnalysisForm />
    </div>
  );
}
