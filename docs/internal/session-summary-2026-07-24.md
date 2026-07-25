# Session summary — 2026-07-24

**Internal only.** Captures one working session: contact form shipping, stack clarity, and Convergence / square-museum POC direction.

---

## 1. Contact form — completed tonight

### Problem (since ~May 20 WordPress → GitHub migration)

- Contact forms used **`mailto:`** — opened the visitor’s Mail app; Mark only received mail if they pressed Send.
- Zero inbox submissions aligned with migration, not primarily SEO.

### Postmark (domain + sending)

| Step | Status |
|------|--------|
| DKIM TXT on `20260724182822pm._domainkey` | Verified |
| Return-Path CNAME `pm-bounces` → `pm.mtasv.net` | Verified |
| Sender signature `contact@museumplanning.com` | Created |
| Server API token | In Cloudflare Worker secret |

**Note:** Postmark UI font makes DKIM characters look like `00` / `I` — copy **from Postmark’s Copy button**, character-for-character. Cloudflare quoting TXT values in `"..."` is normal.

### Cloudflare Worker

- **Worker:** `museumplanning-contact-api`
- **Route:** `museumplanning.com/api/contact` (zone Workers Routes — **not** root custom domain on the worker)
- **Secret:** `POSTMARK_SERVER_TOKEN`
- **Failure mode on route:** Fail closed
- **From / Reply-To:** `contact@museumplanning.com` → `mark@museumplanning.com`, Reply-To = visitor email

### Site changes (GitHub `website-2.0`)

| Commit | What |
|--------|------|
| `c8aacbc` | Contact page `fetch("/api/contact")`, privacy page, `cloudflare/contact-api/` |
| `60ea89b` | Email body: **message on top**, typical rates after `---` |

**Repo paths:**

- `museum-planning-contact.html`
- `museum-planning-privacy.html`
- `cloudflare/contact-api/worker.js` (+ README, wrangler.toml)

**Live Worker code** is pasted/deployed in Cloudflare dashboard; keep repo `worker.js` in sync when editing.

### Cost (rough)

- **Cloudflare Worker:** free tier sufficient for contact volume
- **Postmark:** free/dev tier ~100 emails/month; low cost at consulting-site volume

### Still open (website ops)

- Newsletter signup still **`mailto:`** on some pages — separate from Postmark (transactional)
- Mailchimp or lighter alternative — not integrated yet
- Other service pages with `mailto:` submit (master planning, feasibility, immersive, steam) — can share same Worker later
- Portfolio-home experiment review by **2026-07-31**
- GSC: request indexing for `/`

---

## 2. Stack map — what belongs where

Professional layout for **museumplanning.com** (not artwork, not Surrender installs):

```
Visitor → Cloudflare (DNS, CDN, Workers) → GitHub Pages (static HTML)
                ↓
         Postmark (transactional contact)
                ↓
         GA4 / GTM (analytics)
```

| Tool | Role | This site? |
|------|------|------------|
| **Cloudflare** | DNS, CDN, Worker API layer | Yes |
| **GitHub Pages** | Static site host | Yes |
| **Postmark** | One-to-one transactional mail | Yes — contact |
| **Mailchimp / Buttondown / etc.** | Marketing list + newsletter | Not yet |
| **LLM API** (via Worker) | Smart search, routing — no chat UI | Future pilot |
| **Supabase** | Postgres — apps, genomes, long-lived data | Art/install track, not marketing site |
| **Firebase** | Realtime phone → bridge → OSC | Art/install track, not marketing site |

**Firebase vs Supabase (artwork):** use **both** — Firebase for live operator/phone path; Supabase for genome/scars/persistence. Do not consolidate everything on one.

---

## 3. AI on the site — direction (not built)

- **Not** a chatbot on a consulting homepage.
- **Yes:** reactive patterns — smart search, interest-based routing, related projects, optional dynamic intro blocks.
- **Pattern:** static HTML → Cloudflare Worker (secret API key) → LLM + optional markdown corpus / page index.
- **v1 pilot idea:** Field Notes / Museum School search — question in, links + short excerpt out.
- **When it gets heavier:** embeddings + vector index across 200+ pages (still same Worker pattern).

---

## 4. Mailchimp — next optional lane

- **Postmark ≠ Mailchimp.** Contact is done; newsletter is a separate integration.
- Newsletter forms on site still use mailto in places (e.g. resiliency home band).
- Mailchimp OK if account/lists already exist; **Buttondown** etc. worth considering for simpler B2B newsletter if starting fresh.

---

## 5. Convergence / square-museum POC — strategic thread

### Core line (for mayors / city managers)

> The future isn’t a building full of screens. It’s a museum whose physical plant, digital layer, and community role are planned as one system — at a price point and mission your city can sustain.

### Anti-pattern

- **Dateland-style** venues: spectacle, high ticket, ~20-minute visit, weak civic/stewardship story.
- **Partial credit:** infrastructure thinking; **wrong** for default civic local-history model.

### Modal client (matches ~30 city outreach emails)

- Small / mid population (~30k typical)
- **Historic building on the town square**
- Parking: knock-down, surface lot, or shuttle
- **McDonough is the proof case** — Polk opened, cultural plan, Shared Ground

### Logic chain (program sizing)

| City scale | Rough exhibit program |
|------------|-------------------------|
| ~30,000 | ~5,000 ft² front-of-house (+ back-of-house as site allows) |
| ~60k–100k | ~10,000 ft² (e.g. 5k exhibit / 5k back-of-house) |

**Same spine every time:** local history, local art/culture, changing exhibits, modest collection, maker/program room, weekend events, downtown traffic.

### Rolando (architect) — contacted 2026-07-24

- Did Howard renderings; fast, inexpensive, aligned taste.
- **Ask:** renderings for **generic** 10k ft² square-adjacent local history museum — Convergence proof, not Dateland.
- **Show in images:** natural light, objects, touchscreens where earned, maker, kids, art, weekend square energy, honest back-of-house; parking constraint visible.
- **Why:** committees decide on **pictures**; words alone lose.

### C.O. Polk 2017–2018 docs = already the kit

**Source files reviewed this session:**

- `CO-Polk-6-8-18 copy.pdf` — 47-sheet exhibit development (Project Overview EX-0.1, plans, interactives)
- `Polk-Museum-Empathy-Maps.pdf` — personas + stakeholders

**Polk already specified:**

1. Five zones: Entry, Main Gallery, Theater/Multi-use, Art Gallery, Kids  
2. System diagram: website/app/events/collections/games ↔ touch table, object table, signage, town square, 3D printer, **plus** storage RH, people counter, HVAC, alarm, lighting  
3. Cloud DB + personalized collections + Quizlet-like games + **digital signage push** (MLK, Geranium Festival, etc.)  
4. Software req **#5:** port database to **partner museums**  
5. Empathy personas: fundraiser (Frank), reunion family (Emily), AA community (Smiths), student (Darius), autism spectrum kid + 3D print (Dennis)

**Conclusion:** Convergence POC is not greenfield theory — it is **parameterized Polk** for cities that don’t have McDonough yet. Rolando draws the **typology**; Polk docs are the **logic**; LLM/twin/collections APIs are the **2026 update** to the 2017 software stack.

### Multi-museum platform (future business shape)

- 2–3 developers could operate **shared** CMS + schedule + collections hooks + site push for many small museums (GitHub/Cloudflare-style deploy).
- Separate from Museum Planning LLC marketing site and separate from Walhimer artwork.
- Governance/ethics on analytics (e.g. NEC demographic inference on displays) should be **platform policy**, not per-vendor default.

---

## 6. Three lanes — keep separate

| Lane | Purpose |
|------|---------|
| **Museum Planning LLC site** | Leads, portfolio, methodology, contact |
| **Walhimer artwork / installations** | Creative work; Firebase/Supabase/OSC |
| **Convergence / Culture Everywhere POC** | Kit + twin + federated collections + Rolando visuals + optional platform |

Do not merge artwork into consulting homepage; cross-link only when intentional.

---

## 7. Suggested next documents (pick one when ready)

| Document | Audience | Contents |
|----------|----------|----------|
| **Rolando brief (1–2 pages)** | Rolando | Shot list, square site, 5k/5k or Polk-scale, attach EX-0.1 + exhibit plan |
| **Square Museum Logic Chain** | Mayors, city managers | Population → ft² → rooms → staff → parking → digital scope; McDonough row filled in |
| **Mayor answer (1 page)** | Elected / city admin | Dateland contrast + convergence line + McDonough proof + rendering placeholder |
| **Polk kit manifest** | Internal / dev | Five zones as JSON/markdown modules; maps to 2017 sheet index |
| **Newsletter integration spec** | Internal | Mailchimp vs Buttondown, form embed, privacy update |

**New Cursor thread recommended for:** Rolando brief + Square Museum Logic Chain (keeps website ops separate from POC product work).

---

## 8. Reference links (live site)

- Contact: https://museumplanning.com/museum-planning-contact.html  
- Convergence Era: https://museumplanning.com/convergence-era.html  
- Polk project (site): portfolio / `projects/` entries for McDonough  

---

*Last updated: 2026-07-24 (session end).*
