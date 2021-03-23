
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choice = InlineKeyboardMarkup(row_width=2)

prohibited_api = InlineKeyboardButton(text="Запрещенные АПИ", callback_data="запрещенные апи")
choice.insert(prohibited_api)

find_ip = InlineKeyboardButton(text="IP в одной сессии", callback_data="поиск двух ip")
choice.insert(find_ip)

cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
choice.insert(cancel_button)


logging_deep = InlineKeyboardMarkup(row_width=1)

debug = InlineKeyboardButton(text="DEBUG", callback_data="DEBUG")
logging_deep.insert(debug)

info = InlineKeyboardButton(text="INFO", callback_data="INFO")
logging_deep.insert(info)

warning = InlineKeyboardButton(text="WARNING", callback_data="WARNING")
logging_deep.insert(warning)


error = InlineKeyboardButton(text="ERROR", callback_data="ERROR")
logging_deep.insert(error)


critical = InlineKeyboardButton(text="CRITICAL", callback_data="CRITICAL")
logging_deep.insert(critical)



cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
logging_deep.insert(cancel_button)


prohibited_api_ = InlineKeyboardMarkup(row_width=1)

add = InlineKeyboardButton(text="Добавить путь", callback_data="добавить путь")
prohibited_api_.insert(add)

delete = InlineKeyboardButton(text="Удалить путь", callback_data="удалить путь")
prohibited_api_.insert(delete)

show = InlineKeyboardButton(text="Показать пути", callback_data="показать пути")
prohibited_api_.insert(show)

cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
prohibited_api_.insert(cancel_button)