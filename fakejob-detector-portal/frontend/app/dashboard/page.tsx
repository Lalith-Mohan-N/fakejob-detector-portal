import { DashboardStats } from "@/components/dashboard-stats";
import { HistoryTable } from "@/components/history-table";

export default function DashboardPage() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <h1 className="mb-2 text-3xl font-bold">Dashboard</h1>
      <p className="mb-8 text-muted-foreground">
        Overview of your analysis activity and historical checks on real job data.
      </p>
      <DashboardStats />
      <div className="mt-8">
        <HistoryTable />
      </div>
    </div>
  );
}
