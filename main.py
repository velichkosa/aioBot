from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# import gettext
import yaml
import keyboard as kb
import text_recognition as textr
import db_operator as db
import mail
from utils import States
import messages

MESSAGES = messages.MESSAGES
with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

bot = Bot(token=config['token'])
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if db.to_mongo(message.from_user.id, None, 'start') > 0:
        await bot.send_message(message.chat.id, MESSAGES['autorisation'].
                               format(message.from_user))
    else:
        insert_data = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "full_name": message.from_user.full_name,
            "email": [],
            "language": ['ru', '🇷🇺 Русский'],
            "interface_language": ['ru', '🇷🇺 Русский'],
            "temp": str()}
        db.to_mongo(message.from_user.id, insert_data, 'new_user')
        await bot.send_message(message.chat.id, MESSAGES['registration'].
                               format(message.from_user))


@dp.message_handler(content_types=['photo'])
async def text_recognition(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    delete_message = await bot.send_message(chat_id, MESSAGES['wait_txtr'].
                                            format(message.from_user))
    src = f'files/{message.chat.id}/'
    language = db.to_mongo(user_id, None, 'current_language')[0]
    await message.photo[-1].download(destination_file=src + 'temp.jpg')
    image_text = textr.recognition(src, 'temp.jpg', language)
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
        await bot.send_message(chat_id, MESSAGES['input_email'])
        await state.set_state(States.all()[0])
    elif mail_cnt:
        kkb = kb.email_keyboard(mail_cnt, user_id)
        await bot.send_message(chat_id, text=MESSAGES['select_email'], reply_markup=kkb)


@dp.callback_query_handler(lambda c: c.data == 'newemail')
async def inline_callback_newemail(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    chat_id = callback_query.values['message']['chat']['id']
    user_id = callback_query.from_user.id
    await bot.delete_message(chat_id, message_id)
    await bot.send_message(chat_id, MESSAGES['input_email'])
    state = dp.current_state(user=user_id)
    await state.set_state(States.all()[0])


@dp.callback_query_handler(lambda c: c.data.split('|')[0] == 'select')
async def inline_callback_select_email(callback_query: types.CallbackQuery):
    chat_id = callback_query.values['message']['chat']['id']
    user_id = callback_query.from_user.id
    src = f'files/{chat_id}/temp.jpg'
    image_text = db.to_mongo(user_id, None, 'image_text')
    email = callback_query.data.split('|')[1]
    message_wait = await bot.send_message(chat_id, MESSAGES['waiting'])
    mail.to_email(src, image_text, email, chat_id)
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await bot.delete_message(chat_id, message_wait.message_id)
    await bot.send_message(chat_id, MESSAGES['send_to_email'] + email)


@dp.message_handler(state=States.NEW_EMAIL)
async def first_test_state_case_met(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    email = message.text
    src = f'files/{message.chat.id}/temp.jpg'
    state = dp.current_state(user=user_id)
    message_wait = await bot.send_message(chat_id, MESSAGES['waiting'])

    if mail.validate_email(email):
        db.to_mongo(user_id, email, 'add_email')
        image_text = db.to_mongo(user_id, None, 'image_text')
        mail.to_email(src, image_text, email, chat_id)
        await bot.delete_message(chat_id, message_wait.message_id - 2)
        await bot.delete_message(chat_id, message_wait.message_id - 1)
        await bot.delete_message(chat_id, message_wait.message_id)
        await bot.send_message(chat_id, MESSAGES['send_to_email'] + email)
        await state.reset_state()
    else:
        await bot.delete_message(chat_id, message_wait.message_id)
        await bot.send_message(chat_id, MESSAGES['bad_email'])
        await state.reset_state()
        # sticker = open("files/tea.webp", "rb")
        # bot.send_sticker(chat_id, sticker)
    # await bot.send_message(message.chat.id, f'dfgdfgdfgdfgdf ')
    # await message.reply('NEW_EMAIL!', reply=False)


@dp.message_handler(commands=['settings'])
async def settings_menu(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, MESSAGES['bot_settings'], reply_markup=kb.inline_settings_kb)


@dp.callback_query_handler(lambda c: c.data == 'select_language')
async def inline_select_language(callback_query: types.CallbackQuery):
    chat_id = callback_query.values['message']['chat']['id']
    # user_id = callback_query.from_user.id
    await bot.delete_message(chat_id, callback_query.message.message_id)
    # current_language = db.to_mongo(user_id, None, 'current_language')[1]
    await bot.send_message(chat_id, MESSAGES['select_language'], reply_markup=kb.inline_lang_kb)
    # state = dp.current_state(user=user_id)
    # await state.set_state(States.all()[0])


@dp.callback_query_handler(lambda c: c.data == 'process_select_language')
async def inline_select_language(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    chat_id = callback_query.values['message']['chat']['id']
    # user_id = callback_query.from_user.id
    await bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
    # current_language = db.to_mongo(user_id, None, 'current_language')[1]
    await bot.send_message(chat_id, MESSAGES['select_language'], reply_markup=kb.inline_lang_kb_Process)


@dp.callback_query_handler(lambda c: c.data.split('|')[0] == 'rstlng')
async def inline_set_language(callback_query: types.CallbackQuery):
    chat_id = callback_query.values['message']['chat']['id']
    user_id = callback_query.from_user.id
    await bot.delete_message(chat_id, callback_query.message.message_id)
    delete_message = await bot.send_message(chat_id, MESSAGES['wait_txtr'].format(callback_query.from_user))
    language = [i for i in callback_query.data.split('|')[1:]]
    db.to_mongo(user_id, language, 'set_language')
    src = f'files/{chat_id}/'
    image_text = textr.recognition(src, 'temp.jpg', language[0])
    db.to_mongo(user_id, image_text, 'update_temp')
    await bot.delete_message(chat_id, callback_query.message.message_id - 1)
    await bot.delete_message(chat_id, delete_message.message_id)
    await bot.send_message(chat_id, MESSAGES['current_rec_message'] + language[1])
    await bot.send_message(chat_id, text=image_text, reply_markup=kb.inline_text_kb)


@dp.callback_query_handler(lambda c: c.data.split('|')[0] == 'set_lang')
async def inline_set_language(callback_query: types.CallbackQuery):
    chat_id = callback_query.values['message']['chat']['id']
    user_id = callback_query.from_user.id
    language = [i for i in callback_query.data.split('|')[1:]]
    db.to_mongo(user_id, language, 'set_language')
    # await bot.delete_message(chat_id, callback_query.message.message_id - 1)
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await bot.send_message(chat_id, MESSAGES['current_rec_message'] + language[1])


@dp.callback_query_handler(lambda c: c.data == 'select_interface_language')
async def select_interface_language(callback_query: types.CallbackQuery):
    chat_id = callback_query.values['message']['chat']['id']
    # user_id = callback_query.from_user.id
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await bot.send_message(chat_id, MESSAGES['select_ilang'], reply_markup=kb.inline_interface_kb)


@dp.callback_query_handler(lambda c: c.data.split('|')[0] == 'ilang')
async def inline_set_language(callback_query: types.CallbackQuery):
    chat_id = callback_query.values['message']['chat']['id']
    user_id = callback_query.from_user.id
    # if (callback_query.data.split('|')[1]) == 'rus':
    #     messages.trans('rus')
    # elif (callback_query.data.split('|')[1]) == 'eng':
    #     messages.trans('eng')
    ilanguage = [i for i in callback_query.data.split('|')[1:]]
    db.to_mongo(user_id, ilanguage, 'set_ilang')
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await bot.send_message(chat_id, MESSAGES['ilang_set']+callback_query.data.split('|')[2])


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
