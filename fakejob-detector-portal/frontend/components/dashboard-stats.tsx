"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ShieldCheck, AlertTriangle, BarChart3, Activity } from "lucide-react";

export function DashboardStats() {
  const [stats, setStats] = useState({ total: 0, safe: 0, risky: 0, avgRisk: 0 });

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch("/api/backend/jobs/");
        const jobs = await res.json();
        const total = jobs.length;
        const safe = jobs.filter((j: any) => !j.fraudulent).length;
        const risky = jobs.filter((j: any) => j.fraudulent).length;
        const avgRisk = total ? ((risky / total) * 100) : 0;
        setStats({ total, safe, risky, avgRisk });
      } catch {
        setStats({ total: 0, safe: 0, risky: 0, avgRisk: 0 });
      }
    }
    load();
  }, []);

  const items = [
    { label: "Total Checked", value: stats.total, icon: BarChart3 },
    { label: "Safe", value: stats.safe, icon: ShieldCheck, color: "text-green-500" },
    { label: "Risky", value: stats.risky, icon: AlertTriangle, color: "text-red-500" },
    { label: "Avg Risk %", value: stats.avgRisk.toFixed(1), icon: Activity, color: "text-yellow-500" },
  ];

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {items.map((item) => {
        const Icon = item.icon;
        return (
          <Card key={item.label}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">{item.label}</CardTitle>
              <Icon className={`h-4 w-4 ${item.color || "text-muted-foreground"}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{item.value}</div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
