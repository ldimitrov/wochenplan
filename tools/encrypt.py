"""Verschlüsselt eine HTML-Seite mit Passwort für GitHub Pages.

Aufruf: python3 encrypt.py <eingabe.html> <ausgabe.html> <passwort>
Die Eingabe ist der Seiteninhalt ohne <html>/<head>-Gerüst (wie für das Claude-Artifact).
"""
import base64, os, sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERATIONS = 600_000
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gate.html")

src, out, password = sys.argv[1], sys.argv[2], sys.argv[3]
inner = open(src, encoding="utf-8").read()
page = ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
        '</head><body>' + inner + '</body></html>')

salt, iv = os.urandom(16), os.urandom(12)
key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS).derive(password.encode())
cipher = AESGCM(key).encrypt(iv, page.encode("utf-8"), None)

b64 = lambda b: base64.b64encode(b).decode()
html = (open(TEMPLATE, encoding="utf-8").read()
        .replace("__SALT__", b64(salt)).replace("__IV__", b64(iv))
        .replace("__ITER__", str(ITERATIONS)).replace("__DATA__", b64(cipher)))
open(out, "w", encoding="utf-8").write(html)
print(f"{out}: {len(html)} Bytes")
