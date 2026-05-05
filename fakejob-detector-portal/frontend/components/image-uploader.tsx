"use client";

import { useState, useCallback } from "react";
import { predictStructured } from "@/lib/api";
import { PredictionResult } from "@/types";
import { Button } from "@/components/ui/button";
import { Upload, Loader2, FileImage } from "lucide-react";
import Tesseract from "tesseract.js";

export function ImageUploader({ onResult }: { onResult: (r: PredictionResult) => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [ocrText, setOcrText] = useState("");

  const onDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const f = e.dataTransfer.files[0];
    if (f && f.type.startsWith("image/")) {
      setFile(f);
      setPreview(URL.createObjectURL(f));
    }
  }, []);

  async function handleAnalyze() {
    if (!file) return;
    setLoading(true);
    try {
      const { data: { text } } = await Tesseract.recognize(file, "eng");
      setOcrText(text);
      const prediction = await predictStructured({
        title: "Screenshot Analysis",
        description: text,
        telecommuting: false,
        has_company_logo: false,
        has_questions: false,
      });
      onResult(prediction);
    } catch (err: any) {
      alert("OCR or prediction failed: " + (err.message || "Unknown error"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <div
        onDrop={onDrop}
        onDragOver={(e) => e.preventDefault()}
        className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-muted-foreground/25 bg-muted/50 p-8 transition-colors hover:bg-muted"
      >
        {preview ? (
          <img src={preview} alt="Preview" className="max-h-64 rounded-md object-contain" />
        ) : (
          <>
            <FileImage className="mb-2 h-8 w-8 text-muted-foreground" />
            <p className="text-sm text-muted-foreground">
              Drag and drop a job posting screenshot, or click to select
            </p>
          </>
        )}
        <input
          type="file"
          accept="image/*"
          className="absolute inset-0 cursor-pointer opacity-0"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) {
              setFile(f);
              setPreview(URL.createObjectURL(f));
            }
          }}
        />
      </div>

      {ocrText && (
        <div className="rounded-md bg-muted p-3 text-xs text-muted-foreground">
          <strong>OCR Preview:</strong>
          <p className="mt-1 line-clamp-6">{ocrText}</p>
        </div>
      )}

      <Button onClick={handleAnalyze} disabled={!file || loading} className="w-full">
        {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Upload className="mr-2 h-4 w-4" />}
        Run OCR & Analyze
      </Button>
    </div>
  );
}
