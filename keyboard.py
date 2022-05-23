from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import db_operator as db


btnEmail = InlineKeyboardButton('✉️ На e-mail', callback_data='btnEmail')
btnCopy = InlineKeyboardButton('Скопировать', callback_data='btnCopy')
inline_text_kb = InlineKeyboardMarkup().add(btnEmail, btnCopy)


def email_keyboard(email_cnt, user_id):
    group = []
    keyboard_list = []
    for el in range(email_cnt):
        group.append(el)
        email = db.to_mongo(user_id, el, 'find_email')
        keyboard_list.append([InlineKeyboardButton(email, callback_data='select' + '|' + str(email))])
        print()
    keyboard_list.append([InlineKeyboardButton('✉️ Добавить e-mail:', callback_data='newemail')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


btnLanguage = InlineKeyboardButton("❓Язык распознавания", callback_data='set_language')
inline_settings_kb = InlineKeyboardMarkup().add(btnLanguage)

btnRussian = InlineKeyboardButton("🇷🇺 Русский", callback_data='set_lang' + '|' + 'ru' + '|' +  "🇷🇺 Русский")
btnEnglish = InlineKeyboardButton("🇬🇧 English", callback_data='set_lang' + '|' + 'en' + '|' + '🇬🇧 English')
btnUkraine = InlineKeyboardButton("🇺🇦 Український", callback_data='set_lang' + '|' + 'uk' + '|' + "🇺🇦 Український")
inline_lang_kb = InlineKeyboardMarkup().add(btnRussian, btnEnglish, btnUkraine)