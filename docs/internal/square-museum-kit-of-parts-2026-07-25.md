# Square Museum — kit of parts (internal)

**Context:** Rust Belt · Deep South · shrinking downtown · **Main Street suffering** · civic recovery  
**Budget:** **$5–10 million total** (building + exhibits + digital — not a campaign museum)  
**Size:** **~10,000 ft²** (~5k public / ~5k back-of-house)  
**Framework:** C.O. Polk program spine + [Digital Exhibits](https://github.com/Museum-Planning-LLC/digital-exhibits) software templates + [Convergence Era](https://museumplanning.com/convergence-era.html) / digital twin logic  

**Rendering partner:** Rolando — see `rolando-brief-square-museum-2026-07-24.md`

---

## What this is not

At $5–10M and 10k ft², we are **not** quoting:

| Reference (aspirational only) | Why it’s out of budget |
|------------------------------|-------------------------|
| [British Museum Great Court](https://www.britishmuseum.org/about-us/british-museum-story/architecture/great-court) | Atrium engineering + heritage envelope — $100M+ class |
| [Guggenheim Bilbao](https://www.guggenheim-bilbao.eus/en/the-building/inside-the-museum) | Icon building + international art museum capital |
| Cloud Gate / monumental Kapoor | Single-sculpture budgets exceed whole project |
| Dateland / ticketed spectacle box | Wrong mission and opex for Main Street |

We **borrow the idea**, not the square footage or the invoice.

---

## What we extract from Mark’s reference links

From `Desktop/rolando/links.rtf`:

| # | Link | Extract for kit (scaled) |
|---|------|---------------------------|
| 1 | [Jeongok Prehistory Museum](https://jgpm.ggcf.kr/) · [XTU](https://www.xtuarchitects.com/muse-de-la-prhistoire-de-jeongok-jeongok-core-du-sud-2) | Landscape + building as one gesture; regional story on modest site; **not** the full Korean campus scale |
| 2 | [Guggenheim Bilbao interior](https://www.guggenheim-bilbao.eus/en/the-building/inside-the-museum) | **One** dramatic volume or stair — not the whole building |
| 3 | [Anish Kapoor](https://anishkapoor.com/110) | Mirror / void / infinity **at room scale** — polished chamber, not Chicago-scale public art |
| 4 | [ARoS James Turrell Skyspace](https://www.aros.dk/en/aros-collection/as-seen-below-the-dome-a-skyspace-by-james-turrell/) | Contemplative light room; aperture + bench; **skyspace-lite** module |
| 5 | British Museum Great Court | **Do not draw** — listed only as scale anchor |
| 6 | [Discovery Lab](https://www.discoverylab.org/exhibits) | Maker honesty, kid energy, repeatable exhibit cells |
| 7 | [Bruce Munro](https://www.brucemunro.co.uk/) | Fiber-optic / LED field on **eaves, garden path, or facade** — exterior evening identity |

---

## Core kit (every project — required)

These are non-optional for a credible square museum. Rolando plan should always show them.

| Part | ~Purpose | Notes |
|------|----------|--------|
| **A. Main Street front** | Downtown legibility | Storefront-scale welcome; reads from square; not a suburban bunker |
| **B. Entry + renewal desk** | Staff + “today’s activities” | Casual **renewal office** visible from lobby — where signage, events, and digital content get updated (Polk entry desk evolved) |
| **C. Local history gallery** | Objects + place | Cases, timeline, photography; **one** digital anchor (touch table or local-history wall) |
| **D. Changing / art bay** | Local artists + rotating shows | One quality wall; Smithsonian-minded cases optional at upper budget |
| **E. Theater / multi-use** | Schools, council, weekends | Storable chairs; projection; community contract |
| **F. Maker lab** | Discovery Lab tier | 3D print / scan / bench tools; summer camp; visible from corridor |
| **G. Back of house** | Operate for 30 years | Storage RH, prep, AV closet, loading, staff WC — **honest 5k BoH** |
| **H. Digital Exhibits slot** | Software kit | Pick **≥1** form factor: kiosk · full-wall · full-room ([repo](https://github.com/Museum-Planning-LLC/digital-exhibits)) |
| **I. Square connection** | Main Street recovery | Exterior shot: foot traffic, festival, parking reality (lot or shuttle) |

---

## Optional kit modules (pick 2–4 within budget)

Each module is a **catalog line item** — mayor chooses during feasibility, not during first coffee.

| ID | Module | What it feels like | Budget tier | Reference DNA |
|----|--------|-------------------|-------------|----------------|
| **M1** | **Infinity / mirror chamber** | Single small room; 2–6 people; reflective surfaces; local story projection optional | $$ | Kapoor infinity room **concept**, civic scale |
| **M2** | **Glass spheres / lenses (ceiling bay)** | One gallery bay: suspended glass, light play, objects below | $$ | Poetic ceiling — not Bilbao atrium |
| **M3** | **Skyspace-lite** | Dedicated room; aperture or oculus; bench; dawn/dusk program | $$–$$$ | Turrell / ARoS **logic**, not ARoS budget |
| **M4** | **Fiber optic eaves + garden** | Exterior path, facade soffit, or courtyard; evening Main Street beacon | $–$$ | Bruce Munro **field** scaled to garden |
| **M5** | **Exterior garden room** | Walled courtyard; programs spill out; seasonal events | $–$$ | Jeongok landscape ** gesture**, town scale |
| **M6** | **Full-room digital** | Shared Ground–class participatory room | $$–$$$ | McDonough; [Shared Ground proof](https://museumplanning.com/immersive-mexico/en/shared-ground.html) |
| **M7** | **Full-wall digital** | One architectural surface — timeline, place, or science sim | $$ | [Flow field grid proof](https://museumplanning.com/digital-exhibits/flow-field-grid.html) |
| **M8** | **Town-square interactive** | Floor or model of **their** square; projection optional | $$ | Polk Town Square interactive — parameterized |
| **M9** | **Monument / street signage** | LED monument at sidewalk; event push from renewal desk | $ | Polk street signs; Geranium Festival test case |

**Budget discipline:** At **$5M**, core **A–I** + **two** optional modules. At **$10M**, core + **four** modules + higher case/finish line.

---

## Software kit (pairs with physical modules)

Same pick-list logic — institution content swapped, engine reused.

| Software template | Physical hook | Repo entry |
|-------------------|---------------|------------|
| Kiosk | Entry, maker, kids | Digital Exhibits · kiosk |
| Full-wall | M7, theater, history bay | local-history · place / flow-field |
| Full-room | M6 | Shared Ground |
| Collections + signage CMS | B, I, renewal desk | Polk 2017 spec #1–4 |
| Federated collections API | C, digital layer | Museums Everywhere — no British Museum clone |

**Renewal office (B)** is the human face of constant museum refresh — staff rotate content to monument signs, wall screens, and website without reopening the building.

---

## Rust Belt / Deep South scenario defaults

| Input | Default for renderings |
|-------|------------------------|
| Population | 25k–60k (declining or flat) |
| Downtown | Main Street: empty storefronts **next to** revived block; museum as anchor |
| Building | Adaptive reuse of civic/commercial shell **or** new infill on square |
| Climate | Hot-humid south or four-season rust belt — show HVAC/screened porch logic where relevant |
| Parking | Tight — 20–40 spaces or shuttle from county lot |
| Story | Local history + industry memory + contemporary maker |

---

## Suggested Rolando hero composition ($7M mental model)

One rendering set that sells the kit without Bilbao pricing:

1. **Exterior — Main Street morning** — square, museum frontage, M4 fiber on eaves optional at dusk inset  
2. **Interior — history + M2 glass ceiling bay OR M7 wall** — daylight + objects  
3. **Interior — maker (F) + renewal desk (B)** — staff laptop, kids at bench  
4. **Optional chamber — M1 or M3** — quiet, contemplative counterpoint to maker energy  
5. **Plan** — core A–I labeled; dotted outlines for optional modules mayor could add  

---

## Links file (source)

Mark’s reference list: `~/Desktop/rolando/links.rtf`

---

*Internal · Museum Planning LLC · 2026-07-25*
