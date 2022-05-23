from aiogram.utils.helper import Helper, HelperMode, ListItem


class States(Helper):
    mode = HelperMode.snake_case

    NEW_EMAIL = ListItem()
    SETTINGS = ListItem()