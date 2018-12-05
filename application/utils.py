from pathlib import Path
import json
import sys

import flask


def init_app(name):
    if getattr(sys, "frozen", False):
        resources_root = Path(sys._MEIPASS)
    else:
        resources_root = Path("application")
    return flask.Flask(name,
                       template_folder=Path(resources_root, "templates"),
                       static_folder=Path(resources_root, "static"))


def dump(path, data):
    with path.open("w", encoding="utf-8") as textfile:
        print(f"Dumped data to '{path}'.")
        textfile.write(json.dumps(data, ensure_ascii=False, indent=4))
