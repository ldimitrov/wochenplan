"""Legt die Arbeitsdaten des Wochenplans verschlüsselt im Repo ab (daten.enc) und holt sie wieder heraus.

    python3 tools/daten.py packen   <ordner> <passwort-datei>   # Ordner -> daten.enc
    python3 tools/daten.py auspacken <ordner> <passwort-datei>  # daten.enc -> Ordner

Verschlüsselt wird wie die Seite: AES-GCM, Schlüssel per PBKDF2 aus dem Passwort.
Generierte Dateien (HTML, PDF), die Passwortdatei und Caches kommen nicht mit.
"""
import io
import os
import sys
import tarfile

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERATIONS = 600_000
ZIEL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "daten.enc")
AUSGESCHLOSSEN = {"passwort.txt", "__pycache__"}
ENDUNGEN_AUSGESCHLOSSEN = (".html", ".pdf", ".pyc")


def key(password, salt):
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS).derive(password.encode())


def mitnehmen(info):
    name = os.path.basename(info.name)
    if name in AUSGESCHLOSSEN or (info.isfile() and name.endswith(ENDUNGEN_AUSGESCHLOSSEN)):
        return None
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    return info


def packen(ordner, password):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for name in sorted(os.listdir(ordner)):
            tar.add(os.path.join(ordner, name), arcname=name, filter=mitnehmen)
    salt, iv = os.urandom(16), os.urandom(12)
    open(ZIEL, "wb").write(salt + iv + AESGCM(key(password, salt)).encrypt(iv, buf.getvalue(), None))
    with tarfile.open(fileobj=io.BytesIO(buf.getvalue())) as tar:
        print("\n".join(tar.getnames()))
    print(f"{ZIEL}: {os.path.getsize(ZIEL)} Bytes")


def auspacken(ordner, password):
    data = open(ZIEL, "rb").read()
    salt, iv, cipher = data[:16], data[16:28], data[28:]
    plain = AESGCM(key(password, salt)).decrypt(iv, cipher, None)
    with tarfile.open(fileobj=io.BytesIO(plain)) as tar:
        tar.extractall(ordner, filter="data")
        print("\n".join(tar.getnames()))


if __name__ == "__main__":
    befehl, ordner, passwort_datei = sys.argv[1:4]
    password = open(passwort_datei, encoding="utf-8").read().strip()
    {"packen": packen, "auspacken": auspacken}[befehl](ordner, password)
