import json
from pathlib import Path

import flask


web = flask.Flask("usability-survey",
                  template_folder=Path("application", "templates"),
                  static_folder=Path("application", "static"))

@web.route("/")
def index():
    return flask.render_template("index.html",
                                 view="index")

@web.route("/privacy")
def privacy():
    return flask.render_template("privacy.html",
                                 view="privacy")

@web.route("/survey")
def survey():
    return flask.render_template("survey.html")

@web.route("/thankyou", methods=["POST"])
def thankyou():
    data = flask.request.form
    pseudonym = data["pseudonym"].lower().replace(" ", "-")
    
    textfile = Path(f"fragebogen-{pseudonym}.json")

    # Dump forms to JSON:
    with textfile.open("w", encoding="utf-8") as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))
    
    print(f"INFO: Dumped survey data to '{textfile.absolute()}'.")
    return flask.render_template("thankyou.html",
                                 view="thankyou")
