
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from aiogram.types import Message, CallbackQuery
from states import *
from buttons import *
from database.userservice import *
from all_txt import txts
from aiogram.types import ReplyKeyboardRemove
bot_router = Router()
@bot_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    checker = check_user_db(message.from_user.id)
    if not checker:
        photo = FSInputFile(path="./pictures/lang.png")
        await message.bot.send_photo(chat_id=message.from_user.id, photo=photo,
                                     reply_markup=await language_bt())

        await state.set_state(Registration.language_st)
    elif checker:
        language = get_language_db(message.from_user.id)
        await state.clear()
        photo = FSInputFile(path=f"pictures/gifts_{language}.png")
        await message.bot.send_photo(chat_id=message.from_user.id, photo=photo,
                                     reply_markup=await main_menu_bt(language))


@bot_router.message(Registration.language_st)
async def get_language(message: Message, state: FSMContext):
    language = None
    if message.text == "🇺🇿O'zbek tili" or message.text == "🇷🇺Русский язык":
        if message.text == "🇺🇿O'zbek tili":
            language = "uz"
        elif message.text == "🇷🇺Русский язык":
            language = "ru"
        photo = FSInputFile(path=f"pictures/phone_{language}.png")
        await message.bot.send_photo(chat_id=message.from_user.id, photo=photo,
                                     reply_markup=await phone_bt(language))
        await state.set_data({"language": language})
        await state.set_state(Registration.number_st)
    else:
        photo = FSInputFile(path="./pictures/lang.png")
        await message.bot.send_photo(chat_id=message.from_user.id, photo=photo,
                                     reply_markup=await language_bt())
        await state.set_state(Registration.language_st)


@bot_router.message(Registration.number_st)
async def get_number(message: Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language")
    if message.contact:
        number = message.contact.phone_number
        add_user(tg_id=message.from_user.id, phone_number=number, language=language)
        await state.clear()
        photo = FSInputFile(path=f"pictures/gifts_{language}.png")
        await message.bot.send_message(chat_id=message.from_user.id, text=txts.get("reg").get(language),
                                       reply_markup=ReplyKeyboardRemove())
        await message.bot.send_photo(chat_id=message.from_user.id, photo=photo,
                                     reply_markup=await main_menu_bt(language))

    else:
        await message.bot.send_message(chat_id=message.from_user.id, text=txts.get("phone").get(language),
                                       reply_markup= await phone_bt(language))
        await state.set_state(Registration.number_st)

@bot_router.callback_query(F.data.in_(["add_promo", "contacts", "cancel", "uz", "ru"]))
async def call_backs(query: CallbackQuery, state: FSMContext):
    language = get_language_db(query.from_user.id)
    if query.data == "cancel":
        await query.bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        await state.clear()
    elif query.data == "add_promo":
        await query.bot.send_message(chat_id=query.from_user.id, text=txts.get("promo").get(language),
                                     reply_markup=await cancel_bt(language))
        await state.set_state(Registration.add_promo_st)
    elif query.data == "contacts":
        await query.bot.send_message(chat_id=query.from_user.id, text=txts.get("location").get(language))
        await query.bot.send_location(chat_id=query.from_user.id, latitude=41.292293, longitude=69.198892)
    elif query.data == "uz":
        await query.bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        change_language_db(tg_id=query.from_user.id, lang="ru")
        language = get_language_db(query.from_user.id)
        await state.clear()
        photo = FSInputFile(path=f"pictures/gifts_{language}.png")
        await query.bot.send_photo(chat_id=query.from_user.id, photo=photo,
                                   reply_markup=await main_menu_bt(language))
    elif query.data == "ru":
        await query.bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        change_language_db(tg_id=query.from_user.id, lang="uz")
        language = get_language_db(query.from_user.id)
        await state.clear()
        photo = FSInputFile(path=f"pictures/gifts_{language}.png")
        await query.bot.send_photo(chat_id=query.from_user.id, photo=photo,
                                   reply_markup=await main_menu_bt(language))

@bot_router.message(Registration.add_promo_st)
async def add_promo(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    language = get_language_db(tg_id)
    promo = message.text
    status = reg_promo_db(tg_id, promo)
    await state.clear()
    if status == "удачно":
        text = txts.get("added").get(language)
        all_promos = get_user_promos_db(tg_id)
        for i in all_promos:
            text += "\n" + i
        await message.bot.send_message(chat_id=tg_id, text=text)
    else:
        text = txts.get("not added").get(language)
        all_promos = get_user_promos_db(tg_id)
        for i in all_promos:
            text += "\n" + i
        await state.clear()
        photo = FSInputFile(path=f"pictures/gifts_{language}.png")
        await message.bot.send_message(chat_id=message.from_user.id, text=text,
                                       reply_markup= await phone_bt(language))
        await message.bot.send_photo(chat_id=message.from_user.id, photo=photo,
                                     reply_markup=await main_menu_bt(language))
        await state.set_state(Registration.number_st)