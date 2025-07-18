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

## Hinweise

* Das Tool verarbeitet aktuell nur `.mp4`-Dateien.
* Bei sehr langen Videos kann der Fortschrittsbalken etwas verzögert reagieren.
* CRF-Werte über 30 führen zu starker Komprimierung und Qualitätsverlust.

---

## Feedback oder Beiträge?

Pull Requests, Bug Reports oder Verbesserungsvorschläge sind willkommen!