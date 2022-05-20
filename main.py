import callback as callback
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
import keyboard as kb
import text_recognition as textr
import db_operator as db
import mail

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if db.to_mongo(message.from_user.id, None, 'start') > 0:
        await bot.send_message(message.chat.id, "👋 Успешная авторизация, {0.first_name}!\n\n"
                                                "⚙️ Нажми Menu или прикрепи изображение для начала работы".
                               format(message.from_user))
    else:
        insert_data = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "full_name": message.from_user.full_name,
            "email": [],
            "temp": str()}
        db.to_mongo(message.from_user.id, insert_data, 'new_user')
        await bot.send_message(message.chat.id, text="👋 Успешная регистрация, {0.first_name}!\n\n"
                                                     "⚙️ Нажми Menu или прикрепи изображение для начала работы".
                               format(message.from_user))


@dp.message_handler(content_types=['photo'])
async def text_recognition(message: types.Message):
    chat_id = message.chat.id
    delete_message = await bot.send_message(chat_id, text="🕜 {0.first_name}, погоди, я разбираюсь... 🕜".
                                            format(message.from_user))
    src = f'files/{message.chat.id}/'
    await message.photo[-1].download(destination_file=src + 'temp.jpg')
    await bot.send_message(chat_id, text=textr.recognition(src, 'temp.jpg'), reply_markup=kb.inline_text_kb)
    await bot.delete_message(chat_id, delete_message.message_id)
    print()


@dp.callback_query_handler(lambda c: c.data == 'btnEmail')
async def process_callback_button1(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    chat_id = callback_query.values['message']['chat']['id']
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
    mail_check, mail_cnt = mail.check_exists_email(user_id)
    if not mail_cnt:
        await bot.send_message(chat_id, text=f'✉️ Введите адрес электронной почты: ')
    elif mail_cnt:
        kkb = kb.email_keyboard(mail_cnt, user_id)
        await bot.send_message(chat_id, text=f'✉️ Выбери e-mail:', reply_markup=kkb)

    print()


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    executor.start_polling(dp)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
