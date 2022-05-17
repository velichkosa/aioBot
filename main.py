from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from pymongo import MongoClient
from config import TOKEN
import keyboard as kb
import text_recognition as textr

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if to_mongo(message.from_user.id, None, 'start') > 0:
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
        to_mongo(message.from_user.id, insert_data, 'new_user')
        await bot.send_message(message.chat.id, text="👋 Успешная регистрация, {0.first_name}!\n\n"
                                                     "⚙️ Нажми Menu или прикрепи изображение для начала работы".
                               format(message.from_user))


@dp.message_handler(content_types=['photo'])
async def text_recognition(message: types.Message):
    delete_message = await bot.send_message(message.chat.id, text="🕜 {0.first_name}, погоди, я разбираюсь... 🕜".
                           format(message.from_user))
    src = f'files/{message.chat.id}/'
    await message.photo[-1].download(destination_file=src + 'temp.jpg')
    await bot.send_message(message.chat.id, text=textr.recognition(src, 'temp.jpg'))
    await bot.delete_message(message.chat.id, delete_message.message_id)



@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


def to_mongo(user_id, data, action):
    MONGO_HOST = "localhost"
    MONGO_PORT = 27017
    MONGO_DB = 'textfinder_bot_db'
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        users = db['users']
        if action == 'start':
            try:
                result = len(users.find_one({'user_id': user_id}))
                return result
            except:
                return 0
        elif action == 'new_user':
            users.insert_one(data)
            return
        elif action == 'add_email':
            users.update_one({'user_id': user_id},
                             {'$addToSet': {'email': data}})
            return

        elif action == 'text_message':
            return users.find_one({'user_id': user_id})['temp']
        elif action == 'email_len':
            return len(users.find_one({'user_id': user_id})['email'])
        elif action == 'find_email':
            return users.find_one({'user_id': user_id})['email'][data]
        elif action == 'update_temp':
            users.update_one({'user_id': user_id},
                             {'$set': {'temp': data}})
            return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    executor.start_polling(dp)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
