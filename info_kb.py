from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# кнопки клавиатуры клиента
b11 = KeyboardButton('/Замовити воду')
b7 = KeyboardButton('Аляска')
b8 = KeyboardButton('Моршинська')
b9 = KeyboardButton('Помпа')
b10 = KeyboardButton('Кулери')

button_info = ReplyKeyboardMarkup(resize_keyboard=True)#
#button_case_admin.add(b3_rahunok).insert(b4_price)
button_info.row(b11).row(b7, b8).row(b9, b10)
