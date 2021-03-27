import os
import sys
import logging
import requests
from datetime import datetime
from shortener.database import db, Label

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

initial_code = int(sys.argv[1],16)

for no, line in enumerate(sys.stdin):
    # TODO: strip to ASCII only
    line = line.strip()
    code=f'{initial_code + no:0>4X}' 
    raw=line

    res = requests.post("http://banana.at.hsp.net.pl:8000/print/7", data={
        "print": "yes",
        "code": code,
        "raw": raw,
    })
    logger.info(res)
    new_label = Label.create(code=code, raw=raw)
    new_label.save()