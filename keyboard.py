from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import db_operator as db
import messages
BTN = messages.BTN

btnEmail = InlineKeyboardButton(BTN['btn_to_email'], callback_data='btnEmail')
# btnReply = InlineKeyboardButton(f'↩️ Переслать', callback_data='btnReply')
btnSetLanguage = InlineKeyboardButton(BTN['btn_lang_setting'], callback_data='process_select_language')
inline_text_kb = InlineKeyboardMarkup(row_width=1).add(btnEmail, btnSetLanguage)

btnRussianInterface = InlineKeyboardButton("🇷🇺 Русский", callback_data='ilang' + '|' + 'rus' + '|' +  "🇷🇺 Русский")
btnEnglishInterface = InlineKeyboardButton("🇬🇧 English", callback_data='ilang' + '|' + 'eng' + '|' + '🇬🇧 English')
inline_interface_kb = InlineKeyboardMarkup().add(btnRussianInterface, btnEnglishInterface)

btnRussianProcess = InlineKeyboardButton("🇷🇺 Русский", callback_data='rstlng' + '|' + 'ru' + '|' +  "🇷🇺 Русский")
btnEnglishProcess = InlineKeyboardButton("🇬🇧 English", callback_data='rstlng' + '|' + 'en' + '|' + '🇬🇧 English')
# btnUkraineProcess = InlineKeyboardButton("🇺🇦 Український", callback_data='rstlng' + '|' + 'uk' + '|' + "🇺🇦 Український")
inline_lang_kb_Process = InlineKeyboardMarkup().add(btnRussianProcess, btnEnglishProcess)


def email_keyboard(email_cnt, user_id):
    group = []
    keyboard_list = []
    for el in range(email_cnt):
        group.append(el)
        email = db.to_mongo(user_id, el, 'find_email')
        keyboard_list.append([InlineKeyboardButton(email, callback_data='select' + '|' + str(email))])
        print()
    keyboard_list.append([InlineKeyboardButton(BTN['btn_add_email'], callback_data='newemail')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


btnLanguage = InlineKeyboardButton(BTN['btn_rec_lang'], callback_data='select_language')
btnInterfaceLanguage = InlineKeyboardButton(BTN['btn_int_lang'], callback_data='select_interface_language')
inline_settings_kb = InlineKeyboardMarkup().add(btnLanguage, btnInterfaceLanguage)

btnRussian = InlineKeyboardButton("🇷🇺 Русский", callback_data='set_lang' + '|' + 'ru' + '|' +  "🇷🇺 Русский")
btnEnglish = InlineKeyboardButton("🇬🇧 English", callback_data='set_lang' + '|' + 'en' + '|' + '🇬🇧 English')
# btnUkraine = InlineKeyboardButton("🇺🇦 Український", callback_data='set_lang' + '|' + 'uk' + '|' + "🇺🇦 Український")
inline_lang_kb = InlineKeyboardMarkup().add(btnRussian, btnEnglish)