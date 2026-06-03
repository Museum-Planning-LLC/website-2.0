# SEO Dashboard — setup

Internal dashboard: [`seo-dashboard.html`](./seo-dashboard.html) · data: [`rankings.json`](./rankings.json)

## What is automated vs manual

| Column | Source | Cost |
|--------|--------|------|
| **Your ranks** | Google Search Console API | Free |
| **Impressions / clicks / MoM** | GSC (28-day windows) | Free |
| **Competitor ranks** | Manual SERP quarterly (CSE API blocked for new Google projects) | Free |

No Semrush or Ahrefs subscription required.

---

## Custom Search API — competitor ranks

Google **disabled “Search the entire web”** for new Programmable Search Engines (Jan 2026). It will be grayed out on new engines — that is expected, not a bug.

**Workaround (free):** add your site **and each competitor domain** to “Sites to search” (up to 50 domains). The API then returns results ranked across that set — good for **relative** competitor comparison, not identical to a full Google SERP.

### Step 1 — Add domains in Programmable Search Engine

[Open your engine](https://programmablesearchengine.google.com/controlpanel/all) → **Search features** → **Sites to search** → add:

```
*.museumplanning.com/*
*.mgmp.us/*
*.vernerjohnson.com/*
*.museumgroup.com/*
*.metstrategies.com/*
```

Save. You do **not** need “Search the entire web” for this approach.

**Search engine ID (`cx`):** from embed code `cx=…` or control panel — e.g. `f5dc8478f87564050`

### Step 2 — API key

Google Cloud → **Credentials** → **Show key** on `Google Search API` (restricted to Custom Search API).

### Step 3 — Local env file

```bash
cd /Users/markwalhimer/Documents/GitHub/museum-planning-llc-website-2.0
cp tools/launch.env.example tools/launch.env
```

Edit `tools/launch.env`:

```
GOOGLE_CSE_API_KEY=your-key-from-show-key
GOOGLE_CSE_CX=f5dc8478f87564050
```

### Step 4 — Test and run

```bash
set -a && source tools/launch.env && set +a
python3 tools/fetch_gsc_rankings.py --test-cse
python3 tools/fetch_gsc_rankings.py
open docs/seo-dashboard.html
```

**If you get `403 PERMISSION_DENIED` / “does not have access to Custom Search JSON API”:**  
Google closed this API to **new customers** (2025–2026). There is no fix — skip CSE entirely. Use **GSC for your ranks** + **manual competitor SERP** (below). Your dashboard still works.

### What the numbers mean (multi-domain mode)

| Reading | Meaning |
|---------|---------|
| Position 3 among results | Best-matching page from that domain vs your tracked cohort |
| **Not** position 3 on Google | Other sites (Wikipedia, AAM, etc.) are not in the engine |

Spot-check one keyword in incognito Google quarterly to validate.

## Manual competitor update (if CSE unavailable or for spot-checks)

Five Tier 1 keywords × four competitors = **20 incognito Google lookups**, ~15 minutes per quarter.

1. Search each Tier 1 phrase in incognito Google
2. Record each competitor’s position (or `NR`) in `docs/seo-dashboard-config.json` → `competitorRanks`
3. Update `competitorRanksAsOf` to today’s date
4. Run `python3 tools/fetch_gsc_rankings.py --dry-run`

---

## Google Search Console — your ranks

**Full walkthrough:** [`GSC-SETUP.md`](./GSC-SETUP.md)

Quick test after adding `GSC_CREDENTIALS_FILE` to `tools/launch.env`:

```bash
set -a && source tools/launch.env && set +a
python3 tools/fetch_gsc_rankings.py --test-gsc
python3 tools/fetch_gsc_rankings.py
open docs/seo-dashboard.html
```

---

## Run commands

```bash
# Load secrets (local)
set -a && source tools/launch.env && set +a

# Test Custom Search only
python3 tools/fetch_gsc_rankings.py --test-cse

# Full fetch (CSE + GSC when credentials present)
python3 tools/fetch_gsc_rankings.py

# Config only, no API calls
python3 tools/fetch_gsc_rankings.py --dry-run
```

---

## View the dashboard

```bash
python3 tools/fetch_gsc_rankings.py
open docs/seo-dashboard.html
```

Run the fetch script first — it writes `rankings.json` and `rankings.embed.js`. Opening the HTML directly uses the embed file (browsers block `fetch()` on `file://` URLs).

---

## Files

| File | Role |
|------|------|
| `seo-dashboard-config.json` | Keyword list, competitor domains, opportunities |
| `rankings.json` | Generated output — dashboard reads this |
| `tools/fetch_gsc_rankings.py` | GSC + Custom Search fetch |
| `tools/launch.env.example` | Template for local secrets (copy → `launch.env`) |
