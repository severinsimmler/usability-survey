import json
from pathlib import Path
import uuid

import flask


web = flask.Flask("usability-survey",
                  template_folder=Path("application", "templates"),
                  static_folder=Path("application", "static"))

@web.route("/")
def index():
    return flask.render_template("index.html",
                                 view="index")

@web.route("/error")
def error():
    return flask.render_template("error.html",
                                 view="error")

@web.route("/privacy")
def privacy():
    return flask.render_template("privacy.html",
                                 view="privacy")

@web.route("/survey")
def survey():
    return flask.render_template("survey.html",
                                 view="survey")

@web.route("/thankyou", methods=["POST"])
def thankyou():
    user = str(uuid.uuid4())
    forms = flask.request.form
    data = dict()

    data["user"] = user
    data["geschlecht"] = forms["geschlecht"]
    data["alter"] = forms["alter"]

    print(json.dumps(data))
    return flask.render_template("thankyou.html",
                                 view="thankyou")

