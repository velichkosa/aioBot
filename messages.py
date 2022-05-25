import gettext

transLoc = "/Volumes/Data HD/MyProject/aioBot/i18n/"
t = gettext.translation('messages', transLoc, languages=['eng'])
_ = t.gettext
t.install()


registration_message = _("👋 Успешная регистрация, {0.first_name}!\n\n" \
                       "⚙️ Нажми Menu или прикрепи изображение для начала работы")
autorisation_message = _("👋 Успешная авторизация, {0.first_name}!\n\n" \
                       "⚙️ Нажми Menu или прикрепи изображение для начала работы")
wait_txtr_message = _("🕜 {0.first_name}, погоди, я разбираюсь... 🕜")
input_email_message = _("✉️ Введите адрес электронной почты: ")
select_email_message = _("✉️ Выбери e-mail: ")
waiting_message = _("⏳...")
send_to_email_message = _("👌 Отправлено на ")
bad_email_message = _("👺 Не правильный адрес, начинай все заново")
bot_settings_message = _("⚙️️ Меню настройки бота:")
select_language_message = _("❓ Выберите основной язык распознования: ")

MESSAGES ={
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
