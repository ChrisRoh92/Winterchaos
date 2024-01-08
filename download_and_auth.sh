#!/bin/bash

# URL des Tar-Archivs
tar_url="https://bierdurstmann.com/winterchaos/assets.tar"

# Verzeichnis, in dem das Tar-Archiv heruntergeladen und entpackt wird
target_directory="."

# Verzeichnis, in dem der Unterordner "assets" erstellt wird
game_directory="$target_directory/game1"

# Benutzername und Passwort abfragen
read -p "Benutzername: " username
read -s -p "Passwort: " password
echo

# Datei herunterladen und speichern
curl -u "$username:$password" -o "$target_directory/assets.tar" "$tar_url"

# Überprüfen, ob der Download erfolgreich war
if [ $? -eq 0 ]; then
    echo "Das Tar-Archiv wurde erfolgreich heruntergeladen."

    # Entpacke das Tar-Archiv in den Unterordner "assets"
    tar -xvf "$target_directory/assets.tar" -C "$game_directory/"

    echo "Das Tar-Archiv wurde erfolgreich entpackt."

    rm assets.tar
else
    echo "Ein Fehler ist aufgetreten. Das Tar-Archiv konnte nicht heruntergeladen werden."
fi
