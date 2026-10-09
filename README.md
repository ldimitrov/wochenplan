# Wochenplan

Passwortgeschützter Essensplan der Woche: https://ldimitrov.github.io/wochenplan/

`index.html` enthält den Plan nur verschlüsselt (AES-GCM, Schlüssel per PBKDF2 aus dem Passwort). Entschlüsselt wird im Browser.

Neue Woche veröffentlichen:

```sh
python3 tools/encrypt.py wochenplan.html index.html '<passwort>'
```

Benötigt `pip install cryptography`. Die unverschlüsselte Seite gehört nicht ins Repo.
