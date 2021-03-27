import os
import logging
from datetime import datetime
from shortener.database import db, Label

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("db_create")

logger.info("connect to db at {}".format(os.environ.get("DB_PATH", "shortener.db")))
db.connect()
logger.info("creating tables")
db.create_tables([Label])

# dm1 = Device.create(mac_address='00:00:00:00:00:00', last_seen=datetime.now())
# dm1.save()
