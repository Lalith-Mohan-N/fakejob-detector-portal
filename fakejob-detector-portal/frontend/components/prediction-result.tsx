"use client";

import { PredictionResult } from "@/types";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { AlertTriangle, CheckCircle, Shield } from "lucide-react";

export function PredictionResultCard({ result }: { result: PredictionResult }) {
  const isSafe = !result.is_fraudulent;
  const risk = result.risk_percentage;

  return (
    <Card className="mt-6">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          {isSafe ? (
            <CheckCircle className="h-6 w-6 text-green-500" />
          ) : (
            <AlertTriangle className="h-6 w-6 text-red-500" />
          )}
          {isSafe ? "Likely Legitimate" : "Potential Fake Job"}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center gap-4">
          <Shield className="h-10 w-10 text-primary" />
          <div>
            <p className="text-2xl font-bold">{risk.toFixed(1)}%</p>
            <p className="text-sm text-muted-foreground">Risk Score</p>
          </div>
          <div className="ml-auto text-right">
            <p className="text-sm font-medium">{result.model_used}</p>
            <p className="text-xs text-muted-foreground">
              Confidence: {(result.confidence_score * 100).toFixed(1)}%
            </p>
          </div>
        </div>

        <div className="h-3 w-full rounded-full bg-muted overflow-hidden">
          <div
            className={`h-full rounded-full transition-all ${
              risk > 70 ? "bg-red-500" : risk > 40 ? "bg-yellow-500" : "bg-green-500"
            }`}
            style={{ width: `${risk}%` }}
          />
        </div>

        {result.suspicious_phrases.length > 0 && (
          <div>
            <h4 className="mb-2 font-semibold text-sm">Suspicious Phrases Detected</h4>
            <div className="flex flex-wrap gap-2">
              {result.suspicious_phrases.map((sp, i) => (
                <span
                  key={i}
                  className="inline-flex items-center rounded-full bg-destructive/10 px-2.5 py-0.5 text-xs font-medium text-destructive"
                >
                  {sp.phrase}
                </span>
              ))}
            </div>
          </div>
        )}

        {result.explanation && (
          <div>
            <h4 className="mb-2 font-semibold text-sm">Top Driving Features</h4>
            <ul className="space-y-1 text-sm text-muted-foreground">
              {result.explanation.feature_importance.slice(0, 5).map((f, i) => (
                <li key={i} className="flex justify-between">
                  <span>{f.feature}</span>
                  <span className={f.importance > 0 ? "text-red-500" : "text-green-500"}>
                    {f.importance > 0 ? "+" : ""}
                    {f.importance.toFixed(3)}
                  </span>
                </li>
              ))}
            </ul>
            <p className="mt-2 text-xs text-muted-foreground">{result.explanation.shap_summary}</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
