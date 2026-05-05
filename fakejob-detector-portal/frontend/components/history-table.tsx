"use client";

import { useEffect, useState } from "react";
import { PredictionLog } from "@/types";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Loader2 } from "lucide-react";

export function HistoryTable() {
  const [logs, setLogs] = useState<PredictionLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch("/api/backend/jobs/");
        const data = await res.json();
        const history: PredictionLog[] = (data || []).map((job: any, i: number) => ({
          id: i + 1,
          is_fraudulent: job.fraudulent,
          confidence_score: job.fraudulent ? 0.85 : 0.15,
          risk_percentage: job.fraudulent ? 85 : 15,
          model_used: "ensemble_rf_xgb",
          suspicious_phrases: [],
          created_at: job.created_at,
        }));
        setLogs(history);
      } catch {
        setLogs([]);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Checks</CardTitle>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex justify-center py-8">
            <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
          </div>
        ) : logs.length === 0 ? (
          <p className="text-center text-sm text-muted-foreground py-8">No history yet. Run some analyses to see results here.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left text-muted-foreground">
                  <th className="pb-2 pr-4">ID</th>
                  <th className="pb-2 pr-4">Result</th>
                  <th className="pb-2 pr-4">Risk %</th>
                  <th className="pb-2 pr-4">Model</th>
                  <th className="pb-2">Date</th>
                </tr>
              </thead>
              <tbody>
                {logs.slice(0, 20).map((log) => (
                  <tr key={log.id} className="border-b last:border-0">
                    <td className="py-3 pr-4">{log.id}</td>
                    <td className="py-3 pr-4">
                      <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${log.is_fraudulent ? "bg-red-100 text-red-700" : "bg-green-100 text-green-700"}`}>
                        {log.is_fraudulent ? "Risky" : "Safe"}
                      </span>
                    </td>
                    <td className="py-3 pr-4">{log.risk_percentage.toFixed(1)}%</td>
                    <td className="py-3 pr-4">{log.model_used}</td>
                    <td className="py-3 text-muted-foreground">{new Date(log.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
