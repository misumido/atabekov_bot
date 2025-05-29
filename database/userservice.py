from database import get_db
from database.models import User, Promos
from datetime import datetime
import pytz
tashkent_timezone = pytz.timezone('Asia/Tashkent')

def add_user(tg_id, phone_number, language):
    with next(get_db()) as db:
        new_user = User(tg_id=tg_id, phone_number=phone_number, language=language,
                        reg_date=datetime.now())
        db.add(new_user)
        db.commit()
def check_user_db(tg_id):
    with next(get_db()) as db:
        checker = db.query(User).filter_by(tg_id=tg_id).first()
        if checker:
            return True
        return False
def get_phone_db(tg_id):
    with next(get_db()) as db:
        user = db.query(User).filter_by(tg_id=tg_id).first()
        if user:
            return user.phone_number

def get_language_db(tg_id):
    with next(get_db()) as db:
        user = db.query(User).filter_by(tg_id=tg_id).first()
        if user:
            return user.language
def reg_promo_db(tg_id, promo):
    with next(get_db()) as db:
        promo = db.query(Promos).filter_by(promocode=promo).first()
        if not promo:
            return "нет промо"
        elif promo.owner:
            return "занято"
        elif promo:
            promo.owner = tg_id
            promo.promo_reg_date = datetime.now(tashkent_timezone)
            db.commit()
            return "удачно"
def get_user_promos_db(tg_id):
    with next(get_db()) as db:
        promos = db.query(Promos).filter_by(owner=tg_id).all()
        if promos:
            return [i.promocode for i in promos]
        else:
            return []
def change_language_db(tg_id, lang):
    with next(get_db()) as db:
        user = db.query(User).filter_by(tg_id=tg_id).first()
        if user:
            user.language = lang
            db.commit()
