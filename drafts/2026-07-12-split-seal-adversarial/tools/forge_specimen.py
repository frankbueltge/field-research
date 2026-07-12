#!/usr/bin/env python3
"""How the two constructed specimens were made — transparency of method, not an exploit.

Read this first: there is no vulnerability here to reproduce. Embedding a C2PA manifest with
your own certificate is ordinary, documented use of the provenance SDK. The ONLY thing that
makes the forged specimen a "forge" is that its manifest asserts a hardware camera capture over
pixels that are not a camera capture — and the ONLY reason it is harmless is that it is signed by
a certificate that chains to no public trust list, so it self-discloses as
`signingCredential.untrusted` to any verifier that checks the trust chain. This script cannot and
does not produce a manifest that a trust-checking verifier would accept as authoritative; that
would require a production signing credential, which the collective does not have and would not
use. The construction is documented so the round can be disputed, per the collective's charter.

The committed specimens under ../specimens are frozen by sha256 (see data/specimens.json). ECDSA
signing uses a fresh random nonce, so re-running this script yields a byte-different but
equivalent specimen; verification of the committed round is done by re-running run_layer1.py
against the pinned bytes, not by re-deriving identical bytes here.

The test CA is NOT committed as a private key (only the public certs live under ../test-ca). To
re-construct a specimen, generate your own openly-labelled non-production test root, e.g.:

    openssl ecparam -name prime256v1 -genkey -noout -out ca_key.pem
    openssl req -new -x509 -key ca_key.pem -out ca_cert.pem -days 3650 \
        -subj "/CN=Split Seal Test Root CA/O=field-research" \
        -addext "basicConstraints=critical,CA:TRUE" -addext "keyUsage=critical,keyCertSign"
    openssl ecparam -name prime256v1 -genkey -noout -out ee_key.pem
    openssl req -new -key ee_key.pem -out ee.csr -subj "/CN=Split Seal Adversarial Signer/O=field-research"
    # end-entity extensions: CA:FALSE, keyUsage=digitalSignature, EKU=documentSigning (1.3.6.1.5.5.7.3.36)
    openssl x509 -req -in ee.csr -CA ca_cert.pem -CAkey ca_key.pem -CAcreateserial -out ee_cert.pem -days 3650 -extfile ee_ext.cnf
    openssl pkcs8 -topk8 -nocrypt -in ee_key.pem -out ee_key_pkcs8.pem
    cat ee_cert.pem ca_cert.pem > chain.pem

Usage:
    python forge_specimen.py BASE.png OUT_FORGE.png OUT_STRIPPED.png chain.pem ee_key_pkcs8.pem

BASE.png is a wild AI specimen carrying a genuine manifest (this round used the shipped w03).
The provenance library's own local signer could not use an openssl EC key in this environment
("empty string"); the callback path (signing ES256/DER with the `cryptography` library) works and
is used below.
"""
import sys

import c2pa
from PIL import Image
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

FORGE_MANIFEST = {
    "claim_generator": "SplitSealAdversarial_TestForge/1.0",
    "title": "adversarial-forged-capture (SPECIMEN, non-trusted test root)",
    "assertions": [
        {"label": "c2pa.actions", "data": {"actions": [
            {"action": "c2pa.created",
             "digitalSourceType": "http://cv.iptc.org/newscodes/digitalsourcetype/digitalCapture"}
        ]}}
    ],
}


def strip(base_png: str, out_png: str) -> None:
    """Lossless PNG re-save drops the C2PA chunk; decoded pixels are preserved exactly."""
    Image.open(base_png).convert("RGBA").save(out_png, format="PNG", optimize=False)


def forge(stripped_png: str, out_png: str, chain_pem: str, key_pkcs8_pem: str) -> None:
    key = serialization.load_pem_private_key(open(key_pkcs8_pem, "rb").read(), password=None)
    certs = open(chain_pem).read()
    signer = c2pa.Signer.from_callback(
        lambda data: key.sign(data, ec.ECDSA(hashes.SHA256())),
        c2pa.C2paSigningAlg.ES256, certs, None)
    c2pa.Builder(FORGE_MANIFEST).sign_file(stripped_png, out_png, signer)


def main() -> None:
    base, out_forge, out_stripped, chain_pem, key_pem = sys.argv[1:6]
    strip(base, out_stripped)
    forge(out_stripped, out_forge, chain_pem, key_pem)
    print("stripped ->", out_stripped)
    print("forged   ->", out_forge)


if __name__ == "__main__":
    main()
