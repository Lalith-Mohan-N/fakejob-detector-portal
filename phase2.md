Continue the project. Build Phase 2: Modern Frontend + Advanced Features. **Strictly use real data only** — no mock data, no random jobs, no placeholders.

Use Next.js 15 (App Router) + TypeScript + Tailwind CSS + shadcn/ui.

Key Requirements (Real Data Only):
1. Connect seamlessly to the Phase 1 FastAPI backend.
2. Job Analysis Page:
   - Form fields matching the real EMSCAD dataset columns.
   - Paste real job URL support (call backend scraper).
   - Image upload with OCR support (for real job screenshots).
3. Display predictions using real examples from the EMSCAD dataset for demo purposes (load a few real legitimate and real fraudulent job samples).
4. Live Job Feed: Pull and display only real job listings (use public job APIs like USAJOBS, Adzuna free tier, or scrape reputable boards ethically with proper headers and rate limiting — never fake data).
5. All demo content, history, and example cards must use actual job postings from the dataset or real public sources.
6. Show Trust Score, risk breakdown, highlighted phrases, and explanations based on real model behavior on the dataset.
7. Implement user dashboard showing history of real checks.
8. Make UI modern, responsive, dark mode enabled.

Provide complete, production-ready code for all components and pages. Ensure every piece of displayed data comes from the real dataset or live real job sources.