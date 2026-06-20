# Agent context — Museum Planning LLC website

**Repo:** `website-2.0` → [museumplanning.com](https://museumplanning.com)

## Start here

1. [`docs/BUSINESS-AND-SEO-PLAYBOOK.md`](docs/BUSINESS-AND-SEO-PLAYBOOK.md) — business intent, Tier 1 keywords, new-page pushback rules, what’s already done
2. [`docs/NAVIGATION.md`](docs/NAVIGATION.md) — global nav order, Field Notes hub, `sync_site_nav.py`, exceptions
3. [`docs/seo-keyword-strategy.md`](docs/seo-keyword-strategy.md) — keyword ↔ URL map
4. [`STYLE-GUIDE.md`](STYLE-GUIDE.md) — design, voice, SEO checklist

## Non-negotiables

- **Five Tier 1 money keywords** — one URL each; don’t create competing pages
- **Push back** on vague new pages (“museum cost”, etc.) — expand Tier 1 FAQs or Tier 3 School instead
- **We** voice on commercial pages
- **Cloudflare 301s** for legacy WordPress paths — see [`redirects/README.md`](redirects/README.md)
- **Nav** — do not add top-bar items without strategy approval; thought leadership → **Field Notes** (`thought-leadership.html`) only; run `python3 tools/sync_site_nav.py` after nav edits

Cursor rules in [`.cursor/rules/`](.cursor/rules/) enforce Tier 1 discipline when this repo is open.
