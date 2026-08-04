# Portfolio as homepage — kept (2026-08-04)

**Started:** 2026-07-24  
**Reviewed:** 2026-08-04  
**Decision:** **Keep** portfolio at `/`

## What changed

- `/` (`index.html`) serves the full project portfolio (formerly `museum-planning-projects.html`).
- Previous resiliency homepage preserved as `index-resiliency-home.html`.
- `museum-planning-projects.html` redirects to `/`.

## North star (30 days from 2026-08-04)

Track **inbound email frequency and fit**, not raw GA sessions.

| Target | Signal |
|--------|--------|
| **~1 email / day or every other day** | Consultant-grade inbound (institution, city, university) |
| **Quality holds** | Tagged rows in [`docs/internal/inbound-inquiry-log.md`](../internal/inbound-inquiry-log.md) skew `consultant` / `city` / `university`, not `wrong-fit` |
| **Next review** | **2026-09-03** — GA + GSC + inquiry log |

## Review summary (2026-08-04)

| Signal | Before (Jul 17–23) | After (Jul 24–Aug 3) |
|--------|-------------------:|---------------------:|
| GA active users / day | ~71 | ~74 |
| GA contact views / day | 1.4 | 1.6 |
| GSC impressions / day | 417 | 451 |
| Inbound email | months of silence | ~daily / every other day |
| Notable | — | NYBG (Jul 27; wrong-fit on remote, right-fit on credibility) |

**Takeaway:** Volume metrics flat or slightly mixed; **fidelity up** — fewer clicks, better inquiries.

## Shipped with keep decision

- Homepage title/H1: **museum planning consultants** + proof grid (`index.html`)
- `assets/analytics.js`: `contact_click` on mailto → `dataLayer`
- GTM tag steps: [`docs/analytics/gtm-contact-click-setup.md`](../analytics/gtm-contact-click-setup.md)

## Revert (only if needed)

```bash
cd museum-planning-llc-website-2.0
git checkout museum-planning-projects.html
mv index-resiliency-home.html index.html
git add index.html museum-planning-projects.html
git commit -m "Revert portfolio-as-homepage."
git push
```

Resiliency messaging stays on dedicated pages and in `index-resiliency-home.html` until merged elsewhere.
