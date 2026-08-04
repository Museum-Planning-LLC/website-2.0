# GTM — `contact_click` event (mailto)

Site code (`assets/analytics.js`) pushes this to `dataLayer` when a visitor clicks mailto for `mark@museumplanning.com` or `mark@walhimer.com`:

```javascript
{
  event: "contact_click",
  link_url: "mailto:mark@museumplanning.com",
  link_text: "Start a Conversation",
  page_path: "/"
}
```

Configure once in **Google Tag Manager** (`GTM-PGG4KV35`):

## 1. Data Layer Variables (optional)

| Name | Data Layer Variable Name |
|------|--------------------------|
| DLV - link_text | `link_text` |
| DLV - page_path | `page_path` |

## 2. Trigger

| Name | Type | Event name |
|------|------|------------|
| CE - contact_click | Custom Event | `contact_click` |

## 3. GA4 Event tag

| Field | Value |
|-------|--------|
| Tag type | Google Analytics: GA4 Event |
| Configuration tag | *(existing GA4 config tag)* |
| Event name | `contact_click` |
| Parameters | `link_text`, `page_path` |
| Trigger | CE - contact_click |

## 4. Key event (optional)

GA4 → Admin → Events → mark `contact_click` as a key event.

## 5. Test

GTM Preview → click **Start a Conversation** on `/` → confirm event before publish.

Until the GTM tag is published, events sit in `dataLayer` (Preview only).
