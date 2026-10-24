#!/bin/sh
# Downloads the study's one source (not committed: third-party data, 21 MB). Usage: sh fetch.sh <out.json>
curl -sS -o "$1" "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sbs_ovw_act?format=JSON&lang=en&time=2021"
sha256sum "$1"
# Digest of the copy this study analysed (2026-10-24): see data/results.json, source.sha256.
# Eurostat revises this table; a different digest means a different release, not a broken fetch.
