import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import db_operator as db


def check_exists_email(user_id):
    email_len = db.to_mongo(user_id, None, 'email_len')
    if email_len == 0:
        return False, email_len
    elif email_len > 0:
        return True, email_len

#
# email_len = to_mongo(call.from_user.id, None, 'email_len')
# if email_len == 0:
#     del_message = bot.send_message(chat_id, f'✉️ Введите адрес электронной почты: ')
#
#     bot.register_next_step_handler(call.message, add_email, src, call.message.text, del_message.id)
# elif email_len > 0:
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     group = []
#     for el in range(email_len):
#         group.append(el)
#         email = to_mongo(call.from_user.id, el, 'find_email')
#         callback_data = 's_e' + '|' + email + '|' + str(src)
#         group[el] = types.InlineKeyboardButton(email, callback_data=callback_data)
#         markup.add(group[el])
#     group.append(el + 1)
#     group[el + 1] = types.InlineKeyboardButton('✉️ Добавить e-mail:',
#                                                callback_data='newemail' + '|' + str(src))
#     markup.add(group[el + 1])
#     to_mongo(call.from_user.id, call.message.text, 'update_temp')
#     del_message = bot.send_message(chat_id, text='✉️ Выбери e-mail:', reply_markup=markup)
#
#
#     def add_email(message, src, text, del_message):
#         chat_id = message.chat.id
#         email = message.text
#         message_wait = bot.send_message(chat_id, text=f'⏳...')
#         valid = validate(
#             email_address=email,
#             check_format=True,
#             check_blacklist=False,
#             check_dns=True,
#             dns_timeout=10,
#             check_smtp=True,
#             smtp_debug=False)
#         if valid:
#
#             to_mongo(message.from_user.id, email, 'add_email')
#             # create message object instance
#             to_email(src, text, email, chat_id)
#             # bot.delete_message(chat_id, message_wait.id)
#             bot.delete_message(chat_id, del_message)
#             os.remove(src)
#         else:
#             bot.delete_message(chat_id, message_wait.id)
#             bot.send_message(chat_id, f'Не правильный адрес, начинай все заново, мудак')
#             sticker = open("files/tea.webp", "rb")
#             bot.send_sticker(chat_id, sticker)
#
# def to_email(src, data, to, chat_id):
#     message_wait = bot.send_message(chat_id, text=f'⏳...')
#     msg = MIMEMultipart()
#
#     # setup the parameters of the message
#     password = config['email_pwd']
#     msg['From'] = "textrecognition.bot@gmail.com"
#     msg['To'] = to
#     msg['Subject'] = "txtr bot result"
#
#     # add in the message body
#     msg.attach(MIMEText(data, 'plain'))
#
#     # attach image to message body
#     with open(src, 'rb') as fp:
#         img = MIMEImage(fp.read())
#     msg.attach(img)
#
#     # create server
#     server = smtplib.SMTP(host='smtp.gmail.com', port=587)
#     server.starttls()
#
#     # Login Credentials for sending the mail
#     server.login(msg['From'], password)
#
#     # send the message via the server.
#     server.sendmail(msg['From'], msg['To'], msg.as_string())
#     server.quit()
#
#     bot.delete_message(message_wait.chat.id, message_wait.id - 1)
#     bot.delete_message(message_wait.chat.id, message_wait.id)
#
#     bot.send_message(chat_id, text=f'👌 Отправлено на {msg["To"]}')