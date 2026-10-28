#!/bin/sh
# Session 237: fetch FEWS NET warehouse market prices per country into $1 (not committed).
for cc in AF PK BI ET KE RW SO SS SD TZ UG SV GT HT HN NI VE PS IR IQ LB SY UA YE AO CD LS MG MW MZ ZM ZW BF CM CF TD ML MR NE NG SN TG; do
  curl -sS --max-time 600 -A "field-research (Meridian; research)" "https://fdw.fews.net/api/marketpricefacts/?format=json&country_code=$cc&start_date=2024-01-01&end_date=2026-10-28" -o "$1/$cc.json"
  echo "$cc $(wc -c < "$1/$cc.json")"
done
