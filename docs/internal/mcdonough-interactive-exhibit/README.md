# McDonough interactive exhibit system

**Status:** Concept / test-launch planning · started 2026-11-25
**Client:** City of McDonough, Georgia
**Owner:** Mark Walhimer, Museum Planning LLC
**Type:** Consulting work (separate from the artwork repo)

Working notes for a small, self-run interactive exhibit system. Nothing here is a commitment to the client.

---

## The idea

1. **Kids' post office game** on a touchscreen exhibit.
2. **Own museum photo database** that can also feed a website, a touch table, and a media server.
3. **One system for several museums**, with remote checks on each client's screens and computers.

The game is a single deliverable. The system around it (screen, local computer, network, dashboard, updates) is what makes it repeatable across clients.

## Proposed hardware (first test)

| Item | Note |
|------|------|
| 55" display | Public-facing screen |
| Touch overlay | **Test on macOS before buying more.** Mac support for multi-touch is limited; single-touch tap and drag is expected to be fine. Not yet tested. |
| Protective glass (Gorilla Glass) | Over the screen |
| Mac mini x 2-3 | One development machine, the rest run exhibits |

Mac mini is one way to move forward, not a final decision.

## Build approach

- Software: Python, Three.js, or HTML. Not decided.
- Kiosk should run **offline**. Network is for updates and the dashboard, not for the visitor experience.
- Dashboard: keep it small. Last check-in per machine and a way to restart the exhibit app.
- Remote access: Tailscale plus SSH or Screen Sharing. Do not open ports at the client site.
- Updates: built into the exhibit. Plan a **three-year cycle** where the computer is replaced and the exhibit is rebuilt together.

## Decisions still open

- [ ] Build the game first, or the photo database first?
- [ ] Software stack for the game (Python / Three.js / HTML)
- [ ] Does the touch overlay behave acceptably on macOS?
- [ ] Which museum photos exist, and who owns the rights?
- [ ] Who pays for the year-three rebuild? Put it in the agreement.
- [ ] macOS update policy between refreshes (hold back and test on the dev Mac, or allow)
- [ ] What the City of McDonough requires (insurance, contract, maintenance plan)
- [ ] What "test launch" means: duration and success measures

## Test launch (draft)

1. Buy one Mac mini and one touch overlay. Test them together.
2. Build a small version of the photo data (a folder of images plus a JSON file).
3. Build the post office game against that data.
4. Build the small dashboard.
5. Save a restore image of the exhibit Mac.
6. Run it for an agreed period and review.

## Risks and notes

- **Children's data:** if the exhibit collects anything, keep it anonymous (counts, time spent, levels played). No photos, voice, or identifiers. Check COPPA before collecting anything beyond that.
- **Self-learning / AI:** collect anonymous usage data, review it by hand, and ship changes as scheduled updates. Do not let the exhibit change its own behavior in front of children.
- **Blockchain / smart contract:** not needed for kiosk monitoring or updates. A database with signed update files covers that. Possible later for photo provenance and rights, decided separately.
- **Single person support:** write a short handoff document so someone else can restart a screen.
- **Photo rights:** showing an image in a gallery and publishing it on a website are different permissions.

## Related

- [landscape.md](./landscape.md) — who else does managed exhibit systems, collections platforms, and post office exhibits
- `digital-exhibits/` — existing Digital Exhibits delivery proofs on museumplanning.com
- `Museum-Planning-LLC/museum-database` — 2018 IMLS museums database (museums, not photos)

## Visibility

This repo is published on GitHub Pages, so files here are reachable by URL. Keep client-specific fees, contract terms, and personal details out of this folder.
