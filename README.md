# FFMPEG GUI – Einfach Videos komprimieren

Ein einfaches GUI-Tool zur Video-Komprimierung mit [FFmpeg](https://ffmpeg.org/) – ideal für mehrere Dateien gleichzeitig.

## Features

*  Mehrfachauswahl von Videodateien (`.mp4`)
*  Warteschlange: Dateien werden nacheinander verarbeitet
*  Fortschrittsanzeige für die aktuelle Datei
*  Visuelles Feedback: Verarbeitete Dateien werden grün markiert
*  Ausgabedateien erhalten den Suffix `_komprimiert`
*  Auswahl des CRF-Werts (Qualitäts-/Komprimierungsstufe)

---

## Funktionsweise:

1. **Dateien auswählen:** Klicke auf „Dateien auswählen“ und wähle ein oder mehrere `.mp4`-Videos.
2. **CRF-Wert wählen:** Je niedriger der CRF-Wert, desto besser die Qualität (Standardbereich: 20–30).
3. **Starten:** Die Videos werden nacheinander mit `ffmpeg` verarbeitet.
4. **Ausgabe:** Die komprimierten Dateien landen im selben Ordner und heißen z. B. `video_komprimiert.mp4`.

---

## Voraussetzungen & Build

Falls du das Projekt selbst ausführen oder bauen willst:

### Benötigte Dateien

* `ffmpeg.exe`
* `ffprobe.exe`

Download unter: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

Lade die Dateien herunter und platziere sie im selben Verzeichnis wie das Python-Skript.

### Build-Anleitung mit `pyinstaller`:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --add-binary="ffmpeg.exe;." --add-binary="ffprobe.exe;." dein_scriptname.py
```

Die ausführbare Datei findest du dann im Ordner `dist/`.

---

## Abhängigkeiten

Installiere die benötigten Python-Pakete mit:

```bash
pip install customtkinter
pip install CustomTkinterMessagebox
```

> Das Tool verwendet `customtkinter` für modernes UI-Design.

---

## Ordnerstruktur

```
projekt/
├── ffmpeg.exe
├── ffprobe.exe
├── dein_script.py
├── README.md
```

---

## Hinweise

* Das Tool verarbeitet aktuell nur `.mp4`-Dateien.
* Bei sehr langen Videos kann der Fortschrittsbalken etwas verzögert reagieren.
* CRF-Werte über 30 führen zu starker Komprimierung und Qualitätsverlust.

---

## Feedback oder Beiträge?

Pull Requests, Bug Reports oder Verbesserungsvorschläge sind willkommen!