from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove
'''ReplyKeyboardRemove - нужен для удаления клавиатуры, после того как клиент нажмет на любую кнопку'''

b1 = KeyboardButton('/Замовити воду')
b2 = KeyboardButton('/info')


#b4 = KeyboardButton('/share my phone number', request_contact=True)
#b5 = KeyboardButton('/send my location', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

'''варианты располажения кнопок'''
kb_client.add(b1).insert(b2)
#kb_client.add(b1).add(b2)
#kb_client.row(b1, b2).add(b4).add(b5)