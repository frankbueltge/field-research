#!/bin/sh
# Reachability probe: one request per line of targets.txt (matter|name|url).
# Usage: sh probe.sh [user-agent] < targets.txt   (no argument = curl's default client string)
UA="$1"
while IFS='|' read -r matter name url; do
  [ -z "$url" ] && continue
  if [ -n "$UA" ]; then out=$(curl -sS -L -m 30 -o body.tmp -w "%{http_code}|%{content_type}|%{size_download}" -A "$UA" "$url" 2>&1 | tail -1)
  else out=$(curl -sS -L -m 30 -o body.tmp -w "%{http_code}|%{content_type}|%{size_download}" "$url" 2>&1 | tail -1); fi
  echo "$(date -u +%FT%TZ)|$matter|$name|$url|$out|$(sha256sum body.tmp | cut -c1-16)"
done
