import os
from datetime import datetime, timedelta

import peewee as pw

db = pw.SqliteDatabase(os.environ.get("DB_PATH", "inventory.db"))


class Label(pw.Model):
    id = pw.PrimaryKeyField()
    code = pw.CharField(unique=True, max_length=4)
    raw = pw.CharField(null=True)
    created_datetime = pw.DateTimeField(default=datetime.now)
    last_visit_datetime = pw.DateTimeField(default=datetime.now)
    # last_print_datetime = pw.DateTimeField(null=True)

    class Meta:
        database = db
