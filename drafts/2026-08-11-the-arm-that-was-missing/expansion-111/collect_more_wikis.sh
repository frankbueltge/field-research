#!/bin/sh
# Session 111 corpus expansion: language editions NOT queried at session 109.
# Same instrument (collect_corpus.py), same query, same namespace. Sequential.
set -u
cd "$(dirname "$0")/.."
for w in cs.wikipedia.org da.wikipedia.org fi.wikipedia.org el.wikipedia.org \
         hu.wikipedia.org no.wikipedia.org ro.wikipedia.org bg.wikipedia.org \
         sr.wikipedia.org hr.wikipedia.org sk.wikipedia.org sl.wikipedia.org \
         lt.wikipedia.org lv.wikipedia.org et.wikipedia.org ca.wikipedia.org \
         eu.wikipedia.org gl.wikipedia.org hi.wikipedia.org bn.wikipedia.org \
         ta.wikipedia.org te.wikipedia.org ml.wikipedia.org mr.wikipedia.org \
         ur.wikipedia.org ms.wikipedia.org tl.wikipedia.org my.wikipedia.org \
         ne.wikipedia.org si.wikipedia.org ka.wikipedia.org hy.wikipedia.org \
         az.wikipedia.org kk.wikipedia.org uz.wikipedia.org mn.wikipedia.org \
         sw.wikipedia.org af.wikipedia.org is.wikipedia.org sq.wikipedia.org \
         mk.wikipedia.org bs.wikipedia.org be.wikipedia.org simple.wikipedia.org \
         nn.wikipedia.org ga.wikipedia.org cy.wikipedia.org la.wikipedia.org \
         ka.wikipedia.org ky.wikipedia.org ; do
  if [ -f "corpus-$w.json" ]; then echo "SKIP $w (session 109 already has it)"; continue; fi
  python3 collect_corpus.py "$w" 2>>expansion-111/collect-wiki-stderr.txt \
    || echo "{\"wiki\":\"$w\",\"ERROR\":true}"
  sleep 0.5
done
