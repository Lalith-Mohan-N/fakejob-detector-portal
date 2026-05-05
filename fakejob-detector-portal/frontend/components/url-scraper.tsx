"use client";

import { useState } from "react";
import { predictUrl } from "@/lib/api";
import { PredictionResult } from "@/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2, Globe } from "lucide-react";

export function UrlScraper({ onResult }: { onResult: (r: PredictionResult) => void }) {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!url) return;
    setLoading(true);
    try {
      const data = await predictUrl(url);
      onResult(data.prediction);
    } catch (err: any) {
      alert(err.response?.data?.detail || "Scraping failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="flex items-center gap-2">
        <Globe className="h-5 w-5 text-muted-foreground" />
        <Input
          type="url"
          placeholder="https://example.com/job-posting"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
        />
        <Button type="submit" disabled={loading}>
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Scrape & Analyze"}
        </Button>
      </div>
      <p className="text-xs text-muted-foreground">
        Enter a real public job posting URL. We will scrape and analyze it using our ML models.
      </p>
    </form>
  );
}
