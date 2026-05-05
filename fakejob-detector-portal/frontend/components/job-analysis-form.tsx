"use client";

import { useState } from "react";
import { predictStructured } from "@/lib/api";
import { JobPost, PredictionResult } from "@/types";
import { PredictionResultCard } from "./prediction-result";
import { UrlScraper } from "./url-scraper";
import { ImageUploader } from "./image-uploader";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Loader2 } from "lucide-react";

export function JobAnalysisForm() {
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    const fd = new FormData(e.currentTarget);
    const job: JobPost = {
      title: fd.get("title") as string,
      description: fd.get("description") as string,
      location: (fd.get("location") as string) || undefined,
      department: (fd.get("department") as string) || undefined,
      company_profile: (fd.get("company_profile") as string) || undefined,
      requirements: (fd.get("requirements") as string) || undefined,
      benefits: (fd.get("benefits") as string) || undefined,
      employment_type: (fd.get("employment_type") as string) || undefined,
      required_experience: (fd.get("required_experience") as string) || undefined,
      required_education: (fd.get("required_education") as string) || undefined,
      industry: (fd.get("industry") as string) || undefined,
      function: (fd.get("function") as string) || undefined,
      telecommuting: fd.get("telecommuting") === "on",
      has_company_logo: fd.get("has_company_logo") === "on",
      has_questions: fd.get("has_questions") === "on",
    };
    try {
      const prediction = await predictStructured(job);
      setResult(prediction);
    } catch (err: any) {
      alert(err.response?.data?.detail || "Prediction failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8">
      <Tabs defaultValue="form">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="form">Manual Entry</TabsTrigger>
          <TabsTrigger value="url">Job URL</TabsTrigger>
          <TabsTrigger value="image">Screenshot OCR</TabsTrigger>
        </TabsList>

        <TabsContent value="form">
          <form onSubmit={handleSubmit} className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="title">Job Title *</Label>
              <Input id="title" name="title" required placeholder="e.g. Software Engineer" />
            </div>
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="description">Description *</Label>
              <Textarea id="description" name="description" required rows={4} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="location">Location</Label>
              <Input id="location" name="location" placeholder="City, Country or Remote" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="department">Department</Label>
              <Input id="department" name="department" />
            </div>
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="company_profile">Company Profile</Label>
              <Textarea id="company_profile" name="company_profile" rows={2} />
            </div>
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="requirements">Requirements</Label>
              <Textarea id="requirements" name="requirements" rows={2} />
            </div>
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="benefits">Benefits</Label>
              <Textarea id="benefits" name="benefits" rows={2} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="employment_type">Employment Type</Label>
              <Input id="employment_type" name="employment_type" placeholder="Full-time, Part-time, Contract" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="required_experience">Required Experience</Label>
              <Input id="required_experience" name="required_experience" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="required_education">Required Education</Label>
              <Input id="required_education" name="required_education" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="industry">Industry</Label>
              <Input id="industry" name="industry" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="function">Function</Label>
              <Input id="function" name="function" />
            </div>
            <div className="flex gap-4 md:col-span-2">
              <label className="flex items-center gap-2 text-sm">
                <input type="checkbox" name="telecommuting" className="h-4 w-4" />
                Telecommuting
              </label>
              <label className="flex items-center gap-2 text-sm">
                <input type="checkbox" name="has_company_logo" className="h-4 w-4" />
                Has Company Logo
              </label>
              <label className="flex items-center gap-2 text-sm">
                <input type="checkbox" name="has_questions" className="h-4 w-4" />
                Has Screening Questions
              </label>
            </div>
            <div className="md:col-span-2">
              <Button type="submit" disabled={loading} className="w-full">
                {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
                Analyze Job
              </Button>
            </div>
          </form>
        </TabsContent>

        <TabsContent value="url">
          <UrlScraper onResult={setResult} />
        </TabsContent>

        <TabsContent value="image">
          <ImageUploader onResult={setResult} />
        </TabsContent>
      </Tabs>

      {result && <PredictionResultCard result={result} />}
    </div>
  );
}
