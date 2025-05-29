from database import get_db
from database.models import *
def get_all_users_tg_id():
    with next(get_db()) as db:
        users = db.query(User).all()
        return [i.tg_id for i in users]
def get_users_count():
    with next(get_db()) as db:
        all_users = db.query(User).count()
        return all_users