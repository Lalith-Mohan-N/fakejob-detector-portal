"use client";

import { ApiJob } from "@/types";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ExternalLink, MapPin, Building } from "lucide-react";
import { useState } from "react";

export function JobCard({ job }: { job: ApiJob }) {
  const [risk, setRisk] = useState<number | null>(null);
  const [analyzing, setAnalyzing] = useState(false);

  async function analyze() {
    setAnalyzing(true);
    try {
      const res = await fetch("/api/backend/predict/structured", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: job.title,
          description: job.description,
          location: job.location,
          telecommuting: false,
          has_company_logo: false,
          has_questions: false,
        }),
      });
      const data = await res.json();
      setRisk(data.risk_percentage ?? 0);
    } catch {
      setRisk(null);
    } finally {
      setAnalyzing(false);
    }
  }

  const riskColor =
    risk === null
      ? "bg-muted text-muted-foreground"
      : risk > 70
      ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400"
      : risk > 40
      ? "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400"
      : "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400";

  return (
    <Card className="flex flex-col">
      <CardHeader className="pb-2">
        <CardTitle className="text-base leading-tight">{job.title}</CardTitle>
        <div className="flex items-center gap-3 text-xs text-muted-foreground">
          <span className="flex items-center gap-1">
            <Building className="h-3 w-3" />
            {job.company}
          </span>
          <span className="flex items-center gap-1">
            <MapPin className="h-3 w-3" />
            {job.location}
          </span>
        </div>
      </CardHeader>
      <CardContent className="flex-1">
        <p className="mb-4 line-clamp-4 text-sm text-muted-foreground">{job.description}</p>
        <div className="flex items-center justify-between">
          <a
            href={job.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-xs font-medium text-primary hover:underline"
          >
            <ExternalLink className="h-3 w-3" />
            View Posting
          </a>
          <button
            onClick={analyze}
            disabled={analyzing}
            className={`rounded-full px-3 py-1 text-xs font-semibold transition-colors ${riskColor}`}
          >
            {analyzing
              ? "Analyzing..."
              : risk !== null
              ? `${risk.toFixed(0)}% Risk`
              : "Analyze"}
          </button>
        </div>
      </CardContent>
    </Card>
  );
}
