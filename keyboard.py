from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import db_operator as db


btnEmail = InlineKeyboardButton('✉️ На e-mail', callback_data='btnEmail')
# btnReply = InlineKeyboardButton(f'↩️ Переслать', callback_data='btnReply')
btnSetLanguage = InlineKeyboardButton(f'⚙️️ Настроить язык', callback_data='process_select_language')
inline_text_kb = InlineKeyboardMarkup(row_width=1).add(btnEmail, btnSetLanguage)


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
    keyboard_list.append([InlineKeyboardButton('✉️ Добавить e-mail:', callback_data='newemail')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


btnLanguage = InlineKeyboardButton("❓Язык распознавания", callback_data='select_language')
inline_settings_kb = InlineKeyboardMarkup().add(btnLanguage)

btnRussian = InlineKeyboardButton("🇷🇺 Русский", callback_data='set_lang' + '|' + 'ru' + '|' +  "🇷🇺 Русский")
btnEnglish = InlineKeyboardButton("🇬🇧 English", callback_data='set_lang' + '|' + 'en' + '|' + '🇬🇧 English')
# btnUkraine = InlineKeyboardButton("🇺🇦 Український", callback_data='set_lang' + '|' + 'uk' + '|' + "🇺🇦 Український")
inline_lang_kb = InlineKeyboardMarkup().add(btnRussian, btnEnglish)