# museumplanner.org → museumplanning.com (sunset redirects)

**Status:** Content migration in progress on museumplanning.com. Apply these redirects when museumplanner.org DNS is pointed at a host that can serve 301 rules (Cloudflare, GitHub Pages `_redirects`, or similar).

**Policy:** museumplanning.com is the single consulting domain. museumplanner.org educational content moves to **Museum School** (Tier 3). Do not create competing Tier 1 URLs for exhibition design.

## Exhibition Design series (live on museumplanning.com)

| Legacy URL (museumplanner.org) | New URL (museumplanning.com) |
|--------------------------------|------------------------------|
| `/museum-exhibition-design-2/` | `/museum-school/museum-exhibition-design/` |
| `/museum-exhibition-design-part-i/` | `/museum-school/museum-exhibition-design/exhibition-design-part-i.html` |
| `/museum-exhibition-design-part-ii/` | `/museum-school/museum-exhibition-design/exhibition-design-part-ii.html` |
| `/museum-exhibition-design-part-iii/` | `/museum-school/museum-exhibition-design/exhibition-design-part-iii.html` |
| `/museum-exhibition-design-part-4/` | `/museum-school/museum-exhibition-design/exhibition-design-part-iv.html` |
| `/museum-exhibition-design-v/` | `/museum-school/museum-exhibition-design/exhibition-design-part-v.html` |
| `/frequently-asked-museum-questions/` (FAQ hub) | `/museum-school/museum-exhibition-design/` (interim; migrate FAQ content separately if needed) |

## Still to migrate (backlog)

| Content | Suggested destination |
|---------|----------------------|
| Starting a museum (10 steps) | Already covered by `museum-school/how-to-start-a-museum.html` — redirect legacy `/starting-a-museum/` there |
| Starting a science center | New Tier 3 page or section on `how-to-start-a-museum.html`; fix museumplanning.com `/starting-a-science-center` → that page (not Museum School index) |
| Remaining blog posts / FAQ | Museum School or retire with 301 to closest guide |

## Rebuild exhibition series pages

Source of truth for HTML body: `museum-planner-2.0/exhibition-design/`. Regenerate on museumplanning.com:

```bash
python3 tools/build_exhibition_design_series.py
```

## Close checklist

1. All high-traffic museumplanner.org URLs have 301 targets on museumplanning.com.
2. Google Search Console: change-of-address or URL removal for museumplanner.org after 301s live.
3. Bing Webmaster Tools: same.
4. Remove `museumplanner.org` links from museumplanning.com footers once sunset is complete (optional — or point to Museum School index).
5. Confirm museumplanner.org GitHub Pages / WordPress is decommissioned so nothing serves duplicate content.
