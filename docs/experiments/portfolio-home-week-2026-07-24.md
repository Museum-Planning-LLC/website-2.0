# Portfolio as homepage — one-week experiment

**Started:** 2026-07-24  
**Review / revert by:** 2026-07-31  

## What changed

- `/` (`index.html`) now serves the full project portfolio (formerly `museum-planning-projects.html`).
- Previous resiliency homepage saved as `index-resiliency-home.html`.
- `museum-planning-projects.html` redirects to `/` so existing links still work.

## What to watch (GA4)

- Sessions on `/` vs prior week
- Clicks on **Start a Conversation** / mailto
- Contact form submissions on `museum-planning-contact.html`
- Any inbound email volume

## Revert (after review)

```bash
cd museum-planning-llc-website-2.0
git checkout museum-planning-projects.html
mv index-resiliency-home.html index.html
# optional: remove index-resiliency-home.html after confirming restore
git add index.html museum-planning-projects.html
git commit -m "Revert portfolio-as-homepage experiment."
git push
```

## Keep experiment

If portfolio-home is working, restore resiliency messaging elsewhere (e.g. link from Services / For Cities) rather than deleting `index-resiliency-home.html` until merged intentionally.
