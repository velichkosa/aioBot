registration_message = ["👋 Успешная регистрация, {0.first_name}!\n\n"
                        "⚙️ Нажми Menu или прикрепи изображение для начала работы",
                        "👋 Successful registration, {0.first_name}!\n\n"
                        "⚙️ Click Menu or attach an image to get started"]

autorisation_message = ["👋 Успешная авторизация, {0.first_name}!\n\n"
                        "⚙️ Нажми Menu или прикрепи изображение для начала работы",
                        "👋 Successful autorisation, {0.first_name}!\n\n"
                        "⚙️ Click Menu or attach an image to get started"]

wait_txtr_message = ["🕜 {0.first_name}, погоди, я разбираюсь... 🕜",
                     "🕜 {0.first_name}, Sergey, wait, please, I understand...🕜"]

input_email_message = ["✉️ Введите адрес электронной почты: ",
                       "✉️ Enter your email address: "]

select_email_message = ["✉️ Выбери e-mail: ",
                        "✉️ Choose email: "]

waiting_message = ["⏳...",
                   "⏳..."]

send_to_email_message = ["👌 Отправлено на ",
                         "👌 Sent to"]

bad_email_message = ["👺 Не правильный адрес, начинай все заново",
                     "👺 Wrong address, start over"]

bot_settings_message = ["⚙️️ Меню настройки бота:",
                        "⚙️️ Bot settings menu:"]

select_language_message = ["❓ Выберите основной язык распознования: ",
                           "❓ Select the main recognition language:"]


def text(mes, lang):
    LANG_CODE = {
        'ru': 0,
        'en': 1
    }
    MESSAGES = {
        'registration': registration_message,
        'autorisation': autorisation_message,
        'wait_txtr': wait_txtr_message,
        'input_email': input_email_message,
        'select_email': select_email_message,
        'waiting': waiting_message,
        'send_to_email': send_to_email_message,
        'bad_email': bad_email_message,
        'bot_settings': bot_settings_message,
        'select_language': select_language_message
    }
    return MESSAGES[str(mes)][LANG_CODE[lang[0]]]

# from utils import States
#
#
# help_message = 'Для того, чтобы изменить текущее состояние пользователя, ' \
#                f'отправь команду "/setstate x", где x - число от 0 до {len(TestStates.all()) - 1}.\n' \
#                'Чтобы сбросить текущее состояние, отправь "/setstate" без аргументов.'
#
# start_message = 'Привет! Это демонстрация работы FSM.\n' + help_message
# invalid_key_message = 'Ключ "{key}" не подходит.\n' + help_message
# state_change_success_message = 'Текущее состояние успешно изменено'
# state_reset_message = 'Состояние успешно сброшено'
# current_state_message = 'Текущее состояние - "{current_state}", что удовлетворяет условию "один из {states}"'
#
# MESSAGES = {
#     'start': start_message,
#     'help': help_message,
#     'invalid_key': invalid_key_message,
#     'state_change': state_change_success_message,
#     'state_reset': state_reset_message,
#     'current_state': current_state_message,
