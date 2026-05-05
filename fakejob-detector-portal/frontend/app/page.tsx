import Link from "next/link";
import { Shield, Search, Newspaper, BarChart3 } from "lucide-react";

export default function HomePage() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-16">
      <div className="text-center">
        <Shield className="mx-auto h-16 w-16 text-primary" />
        <h1 className="mt-6 text-4xl font-extrabold tracking-tight sm:text-5xl">
          Fake Job Detector Portal
        </h1>
        <p className="mt-4 text-lg text-muted-foreground">
          Real-time global job vacancy portal with intelligent fake job detection powered by ML.
        </p>
      </div>

      <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <FeatureCard
          href="/analyze"
          icon={<Search className="h-6 w-6" />}
          title="Analyze a Job"
          description="Paste a job posting, URL, or screenshot to instantly detect fraud using real ML models trained on the EMSCAD dataset."
        />
        <FeatureCard
          href="/feed"
          icon={<Newspaper className="h-6 w-6" />}
          title="Live Job Feed"
          description="Browse real job listings from public APIs with built-in fraud scoring on every post."
        />
        <FeatureCard
          href="/dashboard"
          icon={<BarChart3 className="h-6 w-6" />}
          title="Dashboard"
          description="View your analysis history, statistics, and trends on real job data."
        />
      </div>
    </div>
  );
}

function FeatureCard({
  href,
  icon,
  title,
  description,
}: {
  href: string;
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <Link
      href={href}
      className="group flex flex-col gap-3 rounded-xl border bg-card p-6 shadow-sm transition-colors hover:bg-accent"
    >
      <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
        {icon}
      </div>
      <h3 className="text-lg font-semibold">{title}</h3>
      <p className="text-sm text-muted-foreground">{description}</p>
    </Link>
  );
}
