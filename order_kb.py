from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# кнопки клавиатуры клиента
b12 = KeyboardButton('/скасувати замовлення')
b13 = KeyboardButton('/пропустити цю позицію')


button_order = ReplyKeyboardMarkup(resize_keyboard=True)#
#button_case_admin.add(b3_rahunok).insert(b4_price)
button_order.row(b13).row(b12)

#button_info = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)