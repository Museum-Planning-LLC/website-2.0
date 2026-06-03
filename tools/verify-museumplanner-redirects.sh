#!/usr/bin/env bash
set -euo pipefail

CF_IP="${CF_IP:-104.21.65.35}"

echo "=== DNS (dig) ==="
dig +short museumplanner.org A
dig +short www.museumplanner.org A

echo ""
echo "=== macOS resolver cache ==="
dscacheutil -q host -a name museumplanner.org 2>/dev/null || echo "(no cache entry for museumplanner.org)"

echo ""
echo "=== curl www (system DNS) ==="
curl -4 -sI --connect-timeout 10 "https://www.museumplanner.org/" | grep -iE "^HTTP|^location|^server|^cf-ray" || true

echo ""
echo "=== curl apex (system DNS) ==="
if curl -4 -sI --connect-timeout 10 "https://museumplanner.org/" 2>/dev/null | grep -iE "^HTTP|^location|^server|^cf-ray"; then
  :
else
  echo "(apex failed — trying Cloudflare IP via --resolve)"
  curl -4 -sI --resolve "museumplanner.org:443:${CF_IP}" --connect-timeout 10 \
    "https://museumplanner.org/" | grep -iE "^HTTP|^location|^server|^cf-ray" || true
  echo ""
  echo "If --resolve works but system DNS fails, flush cache:"
  echo "  sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder"
fi

echo ""
echo "=== curl apex part-i (--resolve) ==="
curl -4 -sI --resolve "museumplanner.org:443:${CF_IP}" --connect-timeout 10 \
  "https://museumplanner.org/museum-exhibition-design-part-i/" \
  | grep -iE "^HTTP|^location" || true
