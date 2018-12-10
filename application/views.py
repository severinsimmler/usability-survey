import json
from pathlib import Path
import random
import sys

import flask

from application import utils


web = utils.init_app("usability-survey")

@web.route("/")
def index():
    return flask.render_template("index.html",
                                 view="index")


@web.route("/privacy")
def privacy():
    return flask.render_template("privacy.html",
                                 view="privacy")


@web.route("/pre")
def pre():
    return flask.render_template("pre.html",
                                 view="pre")


@web.route("/quesi")
def quesi():
    # Copy the items list:
    items = utils.QUESI.copy()
    # Shuffle items:
    random.shuffle(items)
    return flask.render_template("quesi.html",
                                 view="quesi",
                                 items=items)


@web.route("/nasa")
def nasa():
    # Copy the items list:
    items = utils.NASA.copy()
    # Shuffle items:
    random.shuffle(items)
    return flask.render_template("nasa.html",
                                 view="nasa",
                                 items=items)


@web.route("/post")
def post():
    return flask.render_template("post.html",
                                 view="post")


@web.route("/export/<fragebogen>", methods=["POST"])
def export(fragebogen):
    # Get data from HTML forms:
    data = flask.request.form

    # Construct folderpath object:
    root = Path("fragebogen-daten")

    # Create folder if it doesn't exist yet:
    if not root.exists():
        root.mkdir()

    # Include website in filename, if any:
    if "website" in data:
        filename = f"{data['website']}-{fragebogen}.json"
    else:
        filename = f"{fragebogen}.json"

    # Construct filepath object:
    path = Path(root, filename)

    # Dump data:
    utils.dump(path, data)
    if fragebogen in {"quesi"}:
        return flask.redirect(flask.url_for("nasa"))
    else:
        return flask.render_template("thankyou.html")
