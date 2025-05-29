from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    language_st = State()
    number_st = State()
    payment_st = State()
    add_promo_st = State()
class ChangeAdminInfo(StatesGroup):
    mailing = State()
    get_id = State()
    send_mail = State()