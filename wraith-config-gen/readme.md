# Wraith Config Gen


## Installation

Wraith wurde in Ruby implementiert und nutzt ImageMagick: [Wraith Requirements](https://bbc-news.github.io/wraith/os-install.html)

Informationen zur Installation von Wraith: [Wraith documentation](http://bbc-news.github.io/wraith/index.html).

Für das Tool müssen nur die Python Pakete installiert werden:

> pip install -r requirements.txt

In der jetzigen Form wird nur Chrome unterstützt, sowohl vom Wraith als auch vom Python-Skript. Die neuste Version des Chromedrivers wird automatisch innerhalb der venv installiert.

## Nutzung

      usage: extractor.py [-h] [-f] [-v] url

      positional arguments:
        url            url of the reveal.js presentation

      optional arguments:
        -h, --help     show this help message and exit
        -f, --file     save urls to file
        -v, --verbose  toogle off headless mode

Referenzscreenshots erstellen:

> wraith history configs/history.yaml

Aktuelle Version vergleichen:

> wraith latest configs/history.yaml                       

## Änderung der Standardkonfiguration

Das Tool nutzt die Dateien im Ordner Templates als Vorlage für die erzeugten Konfigurationsdateien.
