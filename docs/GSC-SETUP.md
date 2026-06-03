# Google Search Console — connect real “Your ranks” data

~15 minutes, one time. Free.

After this, `python3 tools/fetch_gsc_rankings.py` pulls **your** average positions, impressions, clicks, and MoM from GSC. Competitor columns stay manual (quarterly SERP).

Use the same Google Cloud project as before (`museumplanning Google Search` is fine).

---

## Step 1 — Enable the Search Console API

1. Open [Google Cloud Console → APIs & Services → Library](https://console.cloud.google.com/apis/library)
2. Search **Google Search Console API** (not Custom Search)
3. Click **Enable**

---

## Step 2 — Create a service account

1. [APIs & Services → Credentials](https://console.cloud.google.com/apis/credentials)
2. **Create credentials** → **Service account**
3. Name: `seo-dashboard-gsc` (any name works)
4. Skip optional role grants → **Done**
5. Click the new service account → **Keys** tab → **Add key** → **Create new key** → **JSON** → **Create**

A `.json` file downloads. **Keep it private** — do not commit to git.

Note the **service account email**, e.g.:

```
seo-dashboard-gsc@museumplanning-google-search.iam.gserviceaccount.com
```

---

## Step 3 — Add the service account to Search Console

1. Open [Google Search Console](https://search.google.com/search-console)
2. Select **museumplanning.com** (domain or URL-prefix property)
3. **Settings** (gear) → **Users and permissions**
4. **Add user**
5. Paste the **service account email**
6. Permission: **Full** (or Restricted with read access — Full is simplest)
7. **Add**

Without this step, the API returns no data even with a valid key.

---

## Step 4 — Put the JSON key path in launch.env

Move the downloaded JSON somewhere safe, e.g.:

```
~/Documents/GitHub/museum-planning-llc-website-2.0/tools/gsc-service-account.json
```

Edit `tools/launch.env`:

```
CSE_DISABLED=1

GSC_CREDENTIALS_FILE=/Users/markwalhimer/Documents/GitHub/museum-planning-llc-website-2.0/tools/gsc-service-account.json
```

Use your **actual path** to the JSON file.

---

## Step 5 — Test the connection

```bash
cd /Users/markwalhimer/Documents/GitHub/museum-planning-llc-website-2.0
pip install -r tools/requirements-gsc.txt
set -a && source tools/launch.env && set +a
python3 tools/fetch_gsc_rankings.py --test-gsc
```

**Success looks like:**

```
GSC connected. Properties this service account can access:
  sc-domain:museumplanning.com (siteFullUser) ← configured

Sample query 'museum planning' (2026-05-… – 2026-05-…):
  avg position: 4.2
  impressions:  120
  clicks:       8

GSC OK — run: python3 tools/fetch_gsc_rankings.py
```

---

## Step 6 — Refresh the dashboard

```bash
set -a && source tools/launch.env && set +a
python3 tools/fetch_gsc_rankings.py
open docs/seo-dashboard.html
```

Footer should say **Your ranks: Google Search Console (…)** instead of “seed”.

---

## Troubleshooting

### Property not in list

Search Console may use **URL prefix** instead of **domain**:

- Domain: `sc-domain:museumplanning.com` (default in config)
- URL prefix: `https://museumplanning.com/`

Run `--test-gsc` to see which properties appear. If you only see the URL-prefix form, add to `launch.env`:

```
GSC_SITE_URL=https://museumplanning.com/
```

### 403 or “User does not have sufficient permission”

- Service account email not added in Search Console → Users
- Wrong Google account / wrong property selected in GSC when adding user

### Query shows no impressions

Normal if the phrase had zero impressions in the last 28 days. Other Tier 1 keywords may still have data. Check GSC UI → Performance → same date range.

### Rank differs from incognito Google

GSC reports **average position** over 28 days, not today’s exact SERP rank. Close enough for trends; spot-check competitors manually.

---

## Optional — monthly auto-refresh on GitHub

Repo → **Settings → Secrets → Actions**:

| Secret | Value |
|--------|--------|
| `GSC_CREDENTIALS_JSON` | Entire contents of the service account JSON file |

Workflow [`.github/workflows/seo-rankings.yml`](../.github/workflows/seo-rankings.yml) runs on the 1st of each month.

---

## What becomes real vs still manual

| After GSC setup | Source |
|-----------------|--------|
| Your rank column | GSC average position |
| Impressions / clicks under each keyword | GSC |
| MoM column | GSC (28-day vs prior 28-day) |
| Competitor columns | Still manual — update `seo-dashboard-config.json` quarterly |
