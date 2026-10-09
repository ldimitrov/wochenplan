# Wochenplan

Passwortgeschützter Essensplan der Woche: https://ldimitrov.github.io/wochenplan/

`index.html` enthält den Plan nur verschlüsselt (AES-GCM, Schlüssel per PBKDF2 aus dem Passwort). Entschlüsselt wird im Browser.

Neue Woche veröffentlichen:

```sh
python3 tools/encrypt.py wochenplan.html index.html '<passwort>'
```

Benötigt `pip install cryptography`. Die unverschlüsselte Seite gehört nicht ins Repo.

## Arbeitsdaten

Plan, Rezepte, Einkaufslisten, Bring!-Abgleich und die Build-Skripte liegen verschlüsselt in `daten.enc` (gleiches Passwort wie die Seite):

```sh
python3 tools/daten.py auspacken <ordner> <passwort-datei>   # zum Lesen/Bearbeiten
python3 tools/daten.py packen    <ordner> <passwort-datei>   # nach Änderungen
```

Bring!-Zugangsdaten kommen aus den Umgebungsvariablen `BRING_EMAIL` und `BRING_PASSWORD` und liegen nie im Repo.
