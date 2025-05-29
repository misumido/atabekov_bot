from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)

async def language_bt():
    buttons = [[KeyboardButton(text="🇺🇿O'zbek tili")], [KeyboardButton(text="🇷🇺Русский язык")]]
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    return kb
async def phone_bt(language):
    if language == "ru":
        buttons = [[KeyboardButton(text="📲Поделиться номером", request_contact=True)]]
    elif language == "uz":
        buttons = [[KeyboardButton(text="📲Телефон рақамингизни юбориш", request_contact=True)]]
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    return kb
async def main_menu_bt(language):
    text = {"promo": {"uz": "⬇️Promokodni kiritish",
                      "ru": "⬇️Ввести промокод"},
            "location": {"uz": "📍Bizning joylashuvimiz va kontaktlarimiz",
                         "ru": "📍Наша локация и контакты"},
            "lang": {"uz": "🔁Сменить язык на русский",
                     "ru": "🔁Tilni o'zbek tiliga o'zgartirish"}}
    buttons = [
        [InlineKeyboardButton(text=text.get("promo").get(language), callback_data="add_promo")],
        [InlineKeyboardButton(text=text.get("location").get(language), callback_data="contacts")],
        [InlineKeyboardButton(text=text.get("lang").get(language), callback_data=f"{language}")]

    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb
async def cancel_bt(language):
    text = {"uz": "❌Bekor qilish",
            "ru": "❌Отменить"}
    buttons = [
        [InlineKeyboardButton(text=text.get(language), callback_data="cancel")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb
async def admin_menu_in():
    buttons = [
        [InlineKeyboardButton(text="✉️Рассылка", callback_data="mailing")],
        [InlineKeyboardButton(text="👤База юзеров", callback_data="users_data")],
        [InlineKeyboardButton(text="ℹ️База промокодов", callback_data="promos_data")],
        [InlineKeyboardButton(text="📩Отправить сообщение юзеру", callback_data="send_mail")],
        [InlineKeyboardButton(text="Закрыть", callback_data="cancel")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb
async def cancel_admin_bt():
    buttons = [
        [KeyboardButton(text="❌Отменить")]
    ]
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    return kb