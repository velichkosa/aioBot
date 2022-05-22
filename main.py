from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import yaml
import keyboard as kb
import text_recognition as textr
import db_operator as db
import mail
from utils import States

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

bot = Bot(token=config['token'])
dp = Dispatcher(bot, storage=MemoryStorage())


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
    user_id = message.from_user.id
    delete_message = await bot.send_message(chat_id, text="🕜 {0.first_name}, погоди, я разбираюсь... 🕜".
                                            format(message.from_user))
    src = f'files/{message.chat.id}/'
    await message.photo[-1].download(destination_file=src + 'temp.jpg')
    image_text = textr.recognition(src, 'temp.jpg')
    db.to_mongo(user_id, image_text, 'update_temp')
    await bot.send_message(chat_id, text=image_text, reply_markup=kb.inline_text_kb)
    await bot.delete_message(chat_id, delete_message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'btnEmail')
async def process_callback_button1(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    chat_id = callback_query.values['message']['chat']['id']
    user_id = callback_query.from_user.id
    state = dp.current_state(user=user_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
    mail_check, mail_cnt = mail.check_exists_email(user_id)
    if not mail_cnt:
        await bot.send_message(chat_id, text=f'✉️ Введите адрес электронной почты: ')
        await state.set_state(States.all()[0])
    elif mail_cnt:
        kkb = kb.email_keyboard(mail_cnt, user_id)
        await bot.send_message(chat_id, text=f'✉️ Выбери e-mail:', reply_markup=kkb)


@dp.callback_query_handler(lambda c: c.data == 'newemail')
async def inline_callback_newemail(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    chat_id = callback_query.values['message']['chat']['id']
    user_id = callback_query.from_user.id
    await bot.delete_message(chat_id, message_id)
    await bot.send_message(chat_id, f'✉️ Введите адрес электронной почты: ')
    state = dp.current_state(user=user_id)
    await state.set_state(States.all()[0])


@dp.callback_query_handler(lambda c: c.data.split('|')[0] == 'select')
async def inline_callback_select_email(callback_query: types.CallbackQuery):
    chat_id = callback_query.values['message']['chat']['id']
    user_id = callback_query.from_user.id
    src = f'files/{chat_id}/temp.jpg'
    image_text = db.to_mongo(user_id, None, 'image_text')
    email = callback_query.data.split('|')[1]
    message_wait = await bot.send_message(chat_id, text=f'⏳...')
    mail.to_email(src, image_text, email, chat_id)
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await bot.delete_message(chat_id, message_wait.message_id)
    await bot.send_message(chat_id, text=f'👌 Отправлено на {email}')


@dp.message_handler(state=States.NEW_EMAIL)
async def first_test_state_case_met(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    email = message.text
    src = f'files/{message.chat.id}/temp.jpg'
    state = dp.current_state(user=user_id)
    message_wait = await bot.send_message(chat_id, text=f'⏳...')

    if mail.validate_email(email):
        db.to_mongo(user_id, email, 'add_email')
        image_text = db.to_mongo(user_id, None, 'image_text')
        mail.to_email(src, image_text, email, chat_id)
        await bot.delete_message(chat_id, message_wait.message_id - 2)
        await bot.delete_message(chat_id, message_wait.message_id - 1)
        await bot.delete_message(chat_id, message_wait.message_id)
        await bot.send_message(chat_id, text=f'👌 Отправлено на {email}')
        await state.reset_state()
    else:
        await bot.delete_message(chat_id, message_wait.message_id)
        await bot.send_message(chat_id, f' 👺 Не правильный адрес, начинай все заново')
        await state.reset_state()
        # sticker = open("files/tea.webp", "rb")
        # bot.send_sticker(chat_id, sticker)
    # await bot.send_message(message.chat.id, f'dfgdfgdfgdfgdf ')
    # await message.reply('NEW_EMAIL!', reply=False)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
