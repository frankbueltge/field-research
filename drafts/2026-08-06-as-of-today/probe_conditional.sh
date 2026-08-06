#!/bin/sh
# Post-hoc mechanism probe (not a pre-registered prediction): does a conditional request
# on an unchanged page get 304 Not Modified, or is the validator invalidated every render?
U="https://digital-strategy.ec.europa.eu/en/policies/ai-act-standardisation"
UA="Mozilla/5.0 (compatible; field-research/1.0; public-interest measurement)"
BASE_LM=$(curl -sS -A "$UA" -D - -o /dev/null --max-time 60 "$U" | awk 'BEGIN{IGNORECASE=1}/^last-modified:/{sub(/^[^:]*: /,"");print;exit}' | tr -d '\r')
BASE_ET=$(curl -sS -A "$UA" -D - -o /dev/null --max-time 60 "$U" | awk 'BEGIN{IGNORECASE=1}/^etag:/{sub(/^[^:]*: /,"");print;exit}' | tr -d '\r')
echo "baseline last-modified: $BASE_LM"
echo "baseline etag: $BASE_ET"
i=0
while [ $i -lt 7 ]; do
  OUT=$(curl -sS -A "$UA" -H "If-Modified-Since: $BASE_LM" -H "If-None-Match: $BASE_ET" -D - -o /dev/null --max-time 60 -w "%{http_code}" "$U")
  CODE=$(printf '%s' "$OUT" | tail -c 3)
  NEWLM=$(printf '%s' "$OUT" | awk 'BEGIN{IGNORECASE=1}/^last-modified:/{sub(/^[^:]*: /,"");print;exit}' | tr -d '\r')
  echo "$(date -u +%FT%TZ) status=$CODE last-modified=$NEWLM"
  i=$((i+1))
  [ $i -lt 7 ] && sleep 120
done
