from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from buttons import *
from database.adminservice import *
from states import ChangeAdminInfo
from converting import convert_to_excel
from aiogram.types.input_file import FSInputFile
import os
# TODO id admina
admin_id = [305896408, 1019755152]


admin_router = Router()

@admin_router.message(Command(commands=["admin"]))
async def admin_mm(message: Message):
    # TODO проверку админа после добавления админа
    if message.from_user.id in admin_id:
        count = get_users_count()
        await message.bot.send_message(message.from_user.id, f"🕵Панель админа\n"
                                                             f"Количество юзеров в боте: {count}",
                                       reply_markup=await admin_menu_in())
@admin_router.callback_query(F.data.in_(["cancel", "none", "mailing", "users_data", "promos_data", "send_mail"]))
async def call_backs(query: CallbackQuery, state: FSMContext):
    await state.clear()
    if query.data == "cancel":
        await query.bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        await state.clear()
    elif query.data == "none":
        pass
    elif query.data == "mailing":
        await query.bot.send_message(query.from_user.id, "Введите сообщение для рассылки, либо отправьте фотографии/видео с описанием",
                                     reply_markup=await cancel_admin_bt())
        await state.set_state(ChangeAdminInfo.mailing)
    elif query.data == "users_data":
        file = convert_to_excel("user")
        if file:
            try:
                document = FSInputFile(file)
                await query.bot.send_document(query.from_user.id, document)
            except Exception as e:
                await query.answer(f"Не удалось отправить файл: {e}")
            finally:
                if os.path.exists(file):
                    os.remove(file)
        else:
            await query.answer("Не удалось создать Excel-файл")
    elif query.data == "promos_data":
        file = convert_to_excel("promos")
        if file:
            try:
                document = FSInputFile(file)
                await query.bot.send_document(query.from_user.id, document)
            except Exception as e:
                await query.answer(f"Не удалось отправить файл: {e}")
            finally:
                if os.path.exists(file):
                    os.remove(file)
        else:
            await query.answer("Не удалось создать Excel-файл")
    elif query.data == "send_mail":
        await query.bot.send_message(query.from_user.id, "Введите айди юзера",
                                     reply_markup=await cancel_admin_bt())
        await state.set_state(ChangeAdminInfo.get_id)


@admin_router.message(ChangeAdminInfo.mailing)
async def mailing_admin(message: Message, state: FSMContext):
    if message.text == "❌Отменить":
        await message.bot.send_message(message.from_user.id, "🚫Действие отменено", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        all_users = get_all_users_tg_id()
        success = 0
        unsuccess = 0
        for i in all_users:
            try:
                await message.bot.copy_message(chat_id=i, from_chat_id=message.from_user.id,
                                               message_id=message.message_id, reply_markup=message.reply_markup)
                success += 1
            except:
                unsuccess +=1
        await message.bot.send_message(message.from_user.id, f"Рассылка завершена!\n"
                                                             f"Успешно отправлено: {success}\n"
                                                             f"Неуспешно: {unsuccess}")
        await state.clear()
@admin_router.message(ChangeAdminInfo.get_id)
async def mailing_admin(message: Message, state: FSMContext):
    if message.text == "❌Отменить":
        await message.bot.send_message(message.from_user.id, "🚫Действие отменено", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        all_users = get_all_users_tg_id()
        try:
            user_id = int(message.text)
            if user_id in all_users:
                await message.bot.send_message(message.from_user.id, "Введите текст сообщения")
                await state.set_data({"id": user_id})
                await state.set_state(ChangeAdminInfo.send_mail)
            else:
                await message.bot.send_message(message.from_user.id, "Некорректное айди. Попробуйте заново")
        except:
            await message.bot.send_message(message.from_user.id, "Некорректное айди. Попробуйте заново")

@admin_router.message(ChangeAdminInfo.send_mail)
async def mailing_admin(message: Message, state: FSMContext):
    if message.text == "❌Отменить":
        await message.bot.send_message(message.from_user.id, "🚫Действие отменено", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        data = await state.get_data()
        user_id = data.get("id")
        try:
            await message.bot.copy_message(chat_id=user_id, from_chat_id=message.from_user.id,
                                           message_id=message.message_id, reply_markup=message.reply_markup)
            await message.bot.send_message(message.from_user.id, "Сообщение успешно отправлено")
            await state.clear()
        except Exception:
            await message.bot.send_message(message.from_user.id, "🚫Юзер удалил или заблокировал бота")
            await state.clear()



@admin_router.message(F.text=="❌Отменить")
async def profile(message: Message, state: FSMContext):
    await message.bot.send_message(message.from_user.id, "️️Все действия отменены",
                                   reply_markup=ReplyKeyboardRemove())
    await state.clear()
