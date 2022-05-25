from pymongo import MongoClient


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

        elif action == 'image_text':
            return users.find_one({'user_id': user_id})['temp']
        elif action == 'email_len':
            return len(users.find_one({'user_id': user_id})['email'])
        elif action == 'find_email':
            return users.find_one({'user_id': user_id})['email'][data]
        elif action == 'update_temp':
            users.update_one({'user_id': user_id},
                             {'$set': {'temp': data}})
            return
        elif action == 'current_language':
            return users.find_one({'user_id': user_id})['language']
        elif action == 'set_language':
            users.update_one({'user_id': user_id},
                             {'$set': {'language': data}})
        elif action == 'interface_language':
            return users.find_one({'user_id': user_id})['interface_language']

# class Database:
#     def __init__(self, db_file):
#         self.connection = sqlite3.connect(db_file)
#         self.cursor = self.connection.cursor()
#
# # для работы с БД
# # Добавление нового пользователя
# # !проверка на пользователя(сделать)
# def add_user(self, user_id):
#     with self.connection:
#        return self.cursor.execute("INSERT INTO `company` (`user_id`) VALUES (?)", (user_id,))
#
# # проверка на существование в данный момент
# def user_exists(self, user_id):
#     with self.connection:
#         result = self.cursor.execute("SELECT * FROM `company` WHERE `user_id` = ?", (user_id,)).fetchall()
#         return bool(len(result))