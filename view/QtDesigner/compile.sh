#!/bin/bash

# Gehe durch alle .ui Dateien im aktuellen Verzeichnis
for file in *.ui; do
    # Extrahiere den Dateinamen ohne Endung
    filename="${file%.ui}"
    
    # Führe pyuic5 aus
    # -x erzeugt direkt ausführbaren Test-Code am Ende der Datei
    # -o definiert die Output-Datei
    pyuic5 -x "$file" -o "output/${filename}_ui.py"
    
    echo "Umgewandelt: $file -> ${filename}_ui.py"
done
