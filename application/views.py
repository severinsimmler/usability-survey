import json
from pathlib import Path

import flask


web = flask.Flask("usability-survey",
                  template_folder=Path("application", "templates"),
                  static_folder=Path("application", "static"))


def dump(path, forms):
    with path.open("w", encoding="utf-8") as textfile:
        textfile.write(json.dumps(forms, ensure_ascii=False, indent=4))


@web.route("/")
def index():
    return flask.render_template("index.html",
                                 view="index")

@web.route("/privacy")
def privacy():
    return flask.render_template("privacy.html",
                                 view="privacy")

@web.route("/demographic")
def demographic():
    return flask.render_template("demographic.html")

@web.route("/quesi", methods=["POST"])
def quesi():
    path = Path("fragebogen-demographic.json")
    dump(path, flask.request.form)
    return flask.render_template("quesi.html")

@web.route("/nasa", methods=["POST"])
def nasa():
    path = Path("fragebogen-quesi.json")
    dump(path, flask.request.form)
    return flask.render_template("nasa.html")

@web.route("/thankyou", methods=["POST"])
def thankyou():
    path = Path("fragebogen-nasa.json")
    dump(path, flask.request.form)
    return flask.render_template("thankyou.html",
                                 view="thankyou")
