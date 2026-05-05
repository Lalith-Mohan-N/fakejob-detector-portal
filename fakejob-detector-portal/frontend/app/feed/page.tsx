import { JobFeed } from "@/components/job-feed";

export default function FeedPage() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <h1 className="mb-2 text-3xl font-bold">Live Job Feed</h1>
      <p className="mb-8 text-muted-foreground">
        Real job listings from public APIs with built-in fraud scoring. Every posting is analyzed using our EMSCAD-trained models.
      </p>
      <JobFeed />
    </div>
  );
}
