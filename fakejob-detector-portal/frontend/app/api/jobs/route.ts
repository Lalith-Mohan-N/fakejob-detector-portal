import { NextResponse } from "next/server";

export async function GET() {
  try {
    // Attempt to fetch from public job APIs. Requires no API key for basic demo:
    // Using Remotive public API (free, CORS-friendly)
    const remotiveRes = await fetch("https://remotive.com/api/remote-jobs?limit=20", {
      headers: { "User-Agent": "FakeJobDetector/1.0" },
      next: { revalidate: 300 },
    });

    let jobs: any[] = [];

    if (remotiveRes.ok) {
      const remotiveData = await remotiveRes.json();
      jobs = remotiveData.jobs.map((job: any) => ({
        id: `remotive-${job.id}`,
        title: job.title,
        company: job.company_name || "Unknown",
        location: job.candidate_required_location || "Remote",
        description: job.description?.replace(/<[^>]+>/g, " ").slice(0, 500) || "",
        url: job.url,
        posted_at: job.publication_date,
        source: "Remotive",
      }));
    }

    // Fallback: if Remotive fails, return empty but inform client
    return NextResponse.json({ jobs });
  } catch (error) {
    return NextResponse.json({ jobs: [], error: "Failed to fetch live jobs" }, { status: 500 });
  }
}
