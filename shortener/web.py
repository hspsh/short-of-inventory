__version__ = "0.1.0"
import logging
import os
import subprocess
import tempfile
import urllib
from datetime import datetime
from urllib.parse import quote_plus, urlencode

from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from shortener.database import Label, db

from .settings import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object("shortener.settings")

common_vars_tpl = {"app": app.config.get_namespace("APP_")}


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


def build_redirect_urls(obj_config, obj):
    escaped = {k: quote_plus(str(v).strip().encode()) for k, v in obj.items()}
    for r in obj_config["redirects"]:
        u = r["url"].format(**escaped)
        print(u)
        yield {**r, "url": u}


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        raw = request.values.get("raw")
        last_code = Label.select().order_by(Label.code)[-1].code
        code = f"{(int(last_code, 16) + 1):0>4X}"
        new_label = Label.create(code=code, raw=raw)
        new_label.save()
        return redirect(url_for("short", label_code=code))

    return render_template("add.html", **common_vars_tpl)


@app.route("/<label_code>", methods=["GET", "POST"])
def short(label_code):
    if label_code is not None and len(label_code) == 4:
        try:
            label = Label.select().where(Label.code == label_code).get()
        except Label.DoesNotExist as exc:
            return "Not found", 404
        if label:
            print_url = "http://banana.at.hsp.net.pl:8000/print/7?" + urlencode(
                {"code": label.code, "raw": label.raw}
            )

            try:
                _, items = label.raw.split("]")
            except:
                items = label.raw
            items = [{"name": n} for n in items.split(";")]

            for i in items:
                i["redirects"] = build_redirect_urls(config["item"], i)

            # if action == "print":
            #     redirect(print_url)
            return render_template(
                "label_view.html",
                label=label,
                items=items,
                next_code=f"{int(label.code, 16) + 1:0>4X}",
                prev_code=f"{int(label.code, 16) - 1:0>4X}",
                print_url=print_url,
                **common_vars_tpl,
            )
    return "No code", 400
