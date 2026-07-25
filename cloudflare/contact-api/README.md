# Contact API (Cloudflare Worker → Postmark)

Sends `museum-planning-contact.html` submissions to `mark@museumplanning.com` via Postmark.

## Deploy (Cloudflare dashboard — ~10 min)

1. **Workers & Pages** → **Create** → **Create Worker**
2. Name: `museumplanning-contact-api`
3. Replace default code with `worker.js` from this folder → **Deploy**
4. **Settings** → **Variables**:
   - **Secret:** `POSTMARK_SERVER_TOKEN` = your Postmark Server API token
   - Optional plain vars: `FROM_EMAIL`, `FROM_NAME`, `TO_EMAIL` (defaults in `worker.js`)
5. **Triggers** → **Add route**:
   - Route: `museumplanning.com/api/contact`
   - Zone: `museumplanning.com`

## Deploy (Wrangler CLI)

```bash
cd cloudflare/contact-api
npm create cloudflare@latest -- --no-install  # or: npm i -g wrangler
wrangler secret put POSTMARK_SERVER_TOKEN
wrangler deploy
```

## Test

```bash
curl -s -X POST https://museumplanning.com/api/contact \
  -H "Content-Type: application/json" \
  -H "Origin: https://museumplanning.com" \
  -d '{"name":"Test","email":"you@example.com","message":"Hello from curl"}'
```

Expect `{"ok":true}`. Check Postmark **Activity** and your inbox.

## Site

After the worker is live, push the updated `museum-planning-contact.html` (uses `fetch("/api/contact", …)`).
