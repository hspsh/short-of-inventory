__version__ = "0.1.0"
import logging
import os
import subprocess
import tempfile
from datetime import datetime
import urllib

from flask import (
    Flask,
    flash,
    render_template,
    redirect,
    url_for,
    request,
    jsonify,
    abort,
)

from shortener import settings
from shortener.database import db, Label

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 69420

# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

common_vars_tpl = {
    "version": __version__,
    "site_name": settings.name,
    "base_url": settings.base_url,
    "wiki_url": settings.wiki_url,
    "git_url": settings.git_url,
}


@app.before_request
def before_request():
    app.logger.debug("connecting to db")
    db.connect()


@app.teardown_appcontext
def after_request(error):
    app.logger.debug("closing db")
    db.close()



@app.route("/")
def index():
    return render_template("index.html", **common_vars_tpl)


@app.route("/<label_code>", methods=["GET", "POST"])
def short(label_code):
    if label_code is not None and len(label_code) == 4:
        try:
            label = Label.select().where(Label.code == label_code).get()
        except Label.DoesNotExist as exc:
            return "Not found", 404
        if label:
            print_url = "http://banana.at.hsp.net.pl:8000/print/7?" + urllib.parse.urlencode({
                "code": label.code,
                "raw": label.raw
            })

            # if action == "print":
            #     redirect(print_url)
            return render_template(
                "label_view.html", label=label, print_url=print_url, **common_vars_tpl
            )
    return "No code", 400

