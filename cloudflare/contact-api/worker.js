/**
 * Museum Planning LLC — contact form → Postmark
 * Route: museumplanning.com/api/contact
 * Secret: POSTMARK_SERVER_TOKEN
 */
const ALLOWED_ORIGINS = new Set([
  "https://museumplanning.com",
  "https://www.museumplanning.com",
]);

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const cors = corsHeaders(origin);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }

    if (request.method !== "POST") {
      return json({ ok: false, error: "Method not allowed" }, 405, cors);
    }

    if (origin && !ALLOWED_ORIGINS.has(origin)) {
      return json({ ok: false, error: "Forbidden" }, 403, cors);
    }

    let payload;
    try {
      payload = await request.json();
    } catch {
      return json({ ok: false, error: "Invalid JSON" }, 400, cors);
    }

    if (payload.company) {
      return json({ ok: true }, 200, cors);
    }

    const name = trim(payload.name);
    const email = trim(payload.email);
    const interest = trim(payload.interest);
    const subject = trim(payload.subject);
    const message = trim(payload.message);

    if (!name || !email || !message) {
      return json({ ok: false, error: "Missing required fields" }, 400, cors);
    }
    if (!isEmail(email)) {
      return json({ ok: false, error: "Invalid email" }, 400, cors);
    }

    const token = env.POSTMARK_SERVER_TOKEN;
    if (!token) {
      return json({ ok: false, error: "Server not configured" }, 500, cors);
    }

    const fromEmail = env.FROM_EMAIL || "contact@museumplanning.com";
    const fromName = env.FROM_NAME || "Museum Planning LLC";
    const toEmail = env.TO_EMAIL || "mark@museumplanning.com";
    const subj = subject || "Inquiry — Museum Planning LLC";

    const textBody = [
      `Name: ${name}`,
      `Email: ${email}`,
      interest ? `Exploring: ${interest}` : "",
      "",
      message,
      "",
      "---",
      "",
      "Typical rates (Museum Planning LLC):",
      "- Museum Assessment: $18,000 + travel (min. retainer)",
      "- Strategic Planning: $45k – $75k + travel",
      "- Feasibility Studies: $40k – $70k + travel",
      "- Master Planning: $100k+ + travel",
      "- Exhibition Design: $60k – $200k + travel",
      "- Owners Rep / PM: Variable — per scope",
    ]
      .filter((line, i, arr) => line !== "" || (i > 0 && arr[i - 1] !== ""))
      .join("\n");

    const postmarkRes = await fetch("https://api.postmarkapp.com/email", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-Postmark-Server-Token": token,
      },
      body: JSON.stringify({
        From: `${fromName} <${fromEmail}>`,
        To: toEmail,
        ReplyTo: email,
        Subject: subj,
        TextBody: textBody,
        MessageStream: "outbound",
      }),
    });

    if (!postmarkRes.ok) {
      const detail = await postmarkRes.text();
      console.error("Postmark error", postmarkRes.status, detail);
      return json({ ok: false, error: "Send failed" }, 502, cors);
    }

    return json({ ok: true }, 200, cors);
  },
};

function trim(value) {
  return typeof value === "string" ? value.trim() : "";
}

function isEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function corsHeaders(origin) {
  const headers = {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    Vary: "Origin",
  };
  if (origin && ALLOWED_ORIGINS.has(origin)) {
    headers["Access-Control-Allow-Origin"] = origin;
  }
  return headers;
}

function json(data, status, cors) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...cors,
    },
  });
}
