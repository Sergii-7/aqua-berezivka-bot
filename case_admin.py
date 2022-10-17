from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# кнопки клавиатуры админа
b3_rahunok = KeyboardButton('/Rahunok')
b4_price = KeyboardButton('/Price')
b5_sklad = KeyboardButton('/Sklad')
b6_ostatki = KeyboardButton('/Ostatki')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)#.add(b3_load).add(b4_delete)
#button_case_admin.add(b3_rahunok).insert(b4_price)
button_case_admin.row(b3_rahunok, b4_price).row(b5_sklad, b6_ostatki)

#button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)