from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
import client_kb
import os
from note import FAM, na, chat, the_date, dostavka, text_fire

class FSMAdmin(StatesGroup):
    Alaska_ = State()
    Morshinska_ = State()
    bottle_ = State()
    add_item_ = State()
    the_note_ = State()
    Price_Alaska = State()
    Price_Morshinska = State()
    Price_bottle = State()
    Price_pompa = State()
    Price_kuler = State()
    Photo_Alaska = State()
    Photo_Morshin = State()
    Photo_bottle = State()
    Photo_pompa = State()
    Dostavka = State()
    Text_ = State()

#Начало диалога загрузки нового пункта меню
@dp.message_handler(commands='Rahunok', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id in FAM:
        q1 = 'Скільки бутлів АЛЯСКА купує клієнт?\n\n'\
             'Лише цифру, наприклад: 2\n\n'\
             'якщо у замовленні немає Аляски, напиши: 0\n\n'\
             'PS: якщо рахунок вже не потрібен – натисни на команду:\n/cancel'
        await FSMAdmin.Alaska_.set()
        await message.answer(q1)
        await message.delete()
    else:
        await message.answer(na)
        await message.delete()

#Выход из состояний если потребуется прервать процесс
@dp.message_handler(state="*", commands='cancel')
@dp.message_handler(Text(equals='s', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        current_state = await state.get_state()
        if current_state is None:
            return
        c = 'Добре\n💙💛\nБережи себе та своїх близьких!'
        await message.answer(c, reply_markup=client_kb.kb_client)
        await state.finish()

#Ловим 1 ответ и пишем в словарь
@dp.message_handler(state=FSMAdmin.Alaska_)
async def Alaska_(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        q2 = 'Скільки бутлів МОРШИНСЬКА купує клієнт?\n\n'\
             'Лише цифру, наприклад: 1\n\n'\
             'якщо у замовленні немає МОРШИНСЬКА, напиши: 0\n\n'\
             'PS: якщо рахунок вже не потрібен – натисни на команду:\n/cancel'
        async with state.proxy() as data:
            data['Alaska_'] = int(message.text)
        await FSMAdmin.next()
        await message.answer(q2)

#Ловим 2 ответ
@dp.message_handler(state=FSMAdmin.Morshinska_)
async def Morshinska_(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        q3 = 'Скільки порожніх бутлів купує клієнт?\n\n'\
             'Якщо у клієнта є вся тара на обмін, напиши: 0\n\n' \
             'PS: якщо рахунок вже не потрібен – натисни на команду:\n/cancel'
        async with state.proxy() as data:
            data['Morshinska_'] = int(message.text)
        await FSMAdmin.next()
        await message.answer(q3)

#Ловим 3 ответ
@dp.message_handler(state=FSMAdmin.bottle_)
async def bottle_(message: types.Message, state: FSMContext):
    q4 = 'Якщо є додатковий товар (помпа, стаканчики та тп), напиши на яку суму в грн.\n'\
         'Hаприклад: 186\n'\
         'Якщо нічого цього немає, напиши: 0\n\n'\
         'PS: якщо рахунок вже не потрібен – натисни на команду:\n/cancel'
    if message.from_user.id in FAM:
        async with state.proxy() as data:
            data['bottle_'] = int(message.text)
        await FSMAdmin.next()
        await message.answer(q4)

#Ловим 4 ответ
@dp.message_handler(state=FSMAdmin.add_item_)
async def add_item_(message: types.Message, state: FSMContext):
    q5 = 'Напиши примітку до рахунку, наприклад розпиши додатковий товар, ' \
         ' якщо він є або до якого числа необхідно зробити проплату.'\
         ' Якщо примітки немає, напиши: 0 або -\n\n' \
         'PS: якщо рахунок вже не потрібен – натисни на команду:\n/cancel'
    if message.from_user.id in FAM:
        async with state.proxy() as data:
            data['add_item_'] = float(message.text)
        await FSMAdmin.next()
        await message.answer(q5)

#Ловим 5 последний ответ и используем полученые данные
@dp.message_handler(state=FSMAdmin.the_note_)
async def the_note_(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        '''with open('the_note.txt', 'w') as tn:
            tn.write(message.text)'''
        async with state.proxy() as data:
            data['the_note_'] = message.text
        async with state.proxy() as base_1:
            smg = f'Користувач {message.from_user} \n' \
                  f'зробив рахунок:\n{base_1}'
            await bot.send_message(chat, smg)
            await message.answer('👍 👌')
            alaska = data['Alaska_']
            morshin = data['Morshinska_']
            bottle = data['bottle_']
            add_item = data['add_item_']
            the_note = data['the_note_']
            with open('alaska_price.txt', 'r') as ap:
                alaska_price = float((ap.read()))
            with open('morshin_price.txt', 'r') as mp:
                morshin_price = float((mp.read()))
            with open('bottle_price.txt', 'r') as bp:
                bottle_price = float((bp.read()))

            total = alaska * alaska_price + morshin * morshin_price \
                    + bottle * bottle_price + add_item
            bill = f'ФОП Бешляга Михайло Михайлович\n' \
                   f'IBAN: UA183220010000026006320059503\n' \
                   f'ІПН/ЄДРПОУ: 2116415395\n' \
                   f'м/т +38(098)476-03-68\n\n' \
                   f'рахунок від {the_date}\n\n' \
                   f'питна вода Аляска 18,9л:\n' \
                   f'{alaska} x {alaska_price} грн\n' \
                   f'питна вода Моршинська 18,9л:\n' \
                   f'{morshin} x {morshin_price} грн\n' \
                   f'порожній бутль:\n' \
                   f'{bottle} x {bottle_price} грн\n' \
                   f'додатковий товар:\n{add_item} грн\n' \
                   f'примітка:\n- {the_note} -\n\n' \
                   f'разом: {total} грн'
            await message.answer(bill, reply_markup=client_kb.kb_client)
            await state.finish()


#ИЗМЕНЕНИЕ ЦЕН = Начало диалога  загрузки нового пункта меню
@dp.message_handler(commands='Ціни', state=None)
async def price_start(message: types.Message):
    if message.from_user.id in FAM:
        with open('alaska_price.txt', 'r') as ap:
            a = float((ap.read()))
        q = f'Введи цену на воду Аляска\n\n' \
            f'Если цена не меняется - напиши {int(a)}\n\n'\
            f'если нужно отменить процесс, нажми\n'\
            f'/cancel'
        await FSMAdmin.Price_Alaska.set()
        await message.answer(q)
        await message.delete()
    else:
        await message.answer(na)
        await message.delete()

#Ловим 1 ответ и пишем в словарь
@dp.message_handler(state=FSMAdmin.Price_Alaska)
async def Price_Alaska(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        with open('morshin_price.txt', 'r') as mp:
            m = float((mp.read()))
        q1 = f'Введи цену на воду Моршинская\n\n'\
             f'Если цена не меняется - напиши {int(m)}'
        with open('alaska_price.txt', 'w') as a:
            a.write(message.text)
        async with state.proxy() as data:
            data['Price_Alaska'] = float(message.text)
        await FSMAdmin.next()
        await message.answer(q1)

#Ловим 2 ответ
@dp.message_handler(state=FSMAdmin.Price_Morshinska)
async def Price_Morshinska(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        with open('bottle_price.txt', 'r') as bp:
            b = float((bp.read()))
        q2 = f'Введи цену на пустой бутль\n\n'\
             f'Если цена не меняется - напиши {int(b)}'
        with open('morshin_price.txt', 'w') as m:
            m.write(message.text)
        async with state.proxy() as data:
            data['Price_Morshinska'] = float(message.text)
        await FSMAdmin.next()
        await message.answer(q2)

#Ловим 3 ответ
@dp.message_handler(state=FSMAdmin.Price_bottle)
async def Price_bottle(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        with open('pompa_price.txt', 'r') as bp:
            p = float((bp.read()))
        q3 = f'Введи цену на помпу\n\n' \
             f'Если цена не меняется - напиши {int(p)}'
        with open('bottle.txt', 'w') as b:
            b.write(message.text)
        async with state.proxy() as data:
            data['Price_bottle'] = float(message.text)
        await FSMAdmin.next()
        await message.answer(q3)


#Ловим 4 последний ответ
@dp.message_handler(state=FSMAdmin.Price_pompa)
async def Price_pompa(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        with open('кулер_price.txt', 'r') as bp:
            p = float((bp.read()))
        q4 = f'Введи минимальную цену на кулер\n\n' \
             f'Если цена не меняется - напиши {int(p)}'
        with open('pompa_price.txt', 'w') as tn:
            tn.write(message.text)
        async with state.proxy() as data:
            data['Price_pompa'] = float(message.text)
        await FSMAdmin.next()
        await message.answer(q4)


# Ловим 5 последний ответ и используем полученые данные
@dp.message_handler(state=FSMAdmin.Price_kuler)
async def Price_kuler(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        with open('кулер_price.txt', 'w') as tn:
            tn.write(message.text)
        async with state.proxy() as data:
            data['Price_kuler'] = float(message.text)
        async with state.proxy() as base_2:
            smg = f'Користувач {message.from_user} \n' \
                  f'змінив ціни:\n{base_2}'
            await bot.send_message(chat, smg)
            await message.answer('👍 👌')
            with open('alaska_price.txt', 'r') as ap:
                alaska_p = float((ap.read()))
            with open('morshin_price.txt', 'r') as mp:
                morshin_p = float((mp.read()))
            with open('bottle_price.txt', 'r') as bp:
                bottle_p = float((bp.read()))
            with open('pompa_price.txt', 'r') as bp:
                pompa_p = float((bp.read()))
            with open('кулер_price.txt', 'r') as kp:
                kuler_p = float((kp.read()))
            report = f'Aqua-Berezivka\n' \
                     f'Ціни станом на {the_date}:\n\n'\
                     f'вода Аляска 18,9л = {alaska_p} грн\n' \
                     f'вода Моршинська 18,9л = {morshin_p}\n' \
                     f'порожній бутль 18,9л =  {bottle_p} грн\n' \
                     f'Помпа механічна = {pompa_p} грн\n' \
                     f'Кулери від = {kuler_p} грн'
            mistake = '# если есть ошибка - начните процесс заново:\n/Ціни'
            await message.answer(report)
            await message.answer(mistake, reply_markup=client_kb.kb_client)
    # здесь мы сохраняем наш state в базу даных черех функцию которую создадим позже
            await state.finish()


#ИЗМЕНЕНИЕ ФОТО ТОВАРОЫ = Начало диалога  загрузки нового пункта меню
q0 = 'Пришли новое фото,\nесли это нужно ' \
     'заменить\nразмер 225*225\nНазвание\n'
q = '# отменить процесс, нажми\n/cancel'
@dp.message_handler(commands='Фото', state=None)
async def photo_start(message: types.Message):
    if message.from_user.id in FAM:
        await FSMAdmin.Photo_Alaska.set()
        q1 = 'Аляска.png'
        with open('Аляска.png', 'rb') as photo:
            await message.answer_photo(photo, q0+q1)
        await message.answer(q)
        await message.delete()
    else:
        await message.answer(na)
        await message.delete()

# 1 ловим фото Аляски и сохраняем его
@dp.message_handler(content_types=['photo'], state=FSMAdmin.Photo_Alaska)
async def Photo_Alaska(message: types.Message, state:FSMContext):
    if message.from_user.id in FAM:
        os.remove('Аляска.png')
        await message.photo[-1].download("Аляска.png")
        q1 = 'Моршинская.png'
        async with state.proxy() as date:
            date['Photo_Alaska'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.answer('фото Аляска загружено')
        with open('Моршинская.png', 'rb') as photo:
            await message.answer_photo(photo, q0+q1)
        await message.answer(q)

# 2 ловим фото Моршинська и сохраняем его
@dp.message_handler(content_types=['photo'], state=FSMAdmin.Photo_Morshin)
async def Photo_Morshin(message: types.Message, state:FSMContext):
    if message.from_user.id in FAM:
        os.remove('Моршинская.png')
        await message.photo[0].download("Моршинская.png")
        async with state.proxy() as date:
            date['Photo_Morshin'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.answer('фото Моршинська загружено')
        q1 = 'Bottle.png'
        with open('Bottle.png', 'rb') as photo:
            await message.answer_photo(photo, q0+q1)
        await message.answer(q)

# 3 ловим фото бутля и сохраняем его
@dp.message_handler(content_types=['photo'], state=FSMAdmin.Photo_bottle)
async def Photo_bottle(message: types.Message, state:FSMContext):
    if message.from_user.id in FAM:
        os.remove('Bottle.png')
        await message.photo[0].download("Bottle.png")
        async with state.proxy() as date:
            date['Photo_bottle'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.answer('фото бутля загружено')
        q1 = 'Помпа.png'
        with open('Помпа.png', 'rb') as photo:
            await message.answer_photo(photo, q0+q1)
        await message.answer(q)

# 4 ловим фото помпы и сохраняем его
@dp.message_handler(content_types=['photo'], state=FSMAdmin.Photo_pompa)
async def Photo_pompa(message: types.Message, state:FSMContext):
    if message.from_user.id in FAM:
        os.remove('Помпа.png')
        await message.photo[0].download("Помпа.png")
        async with state.proxy() as date:
            date['Photo_bottle'] = message.photo[0].file_id
        await message.answer('фото помпы загружено')
        async with state.proxy() as base:
            await bot.send_message(chat, base)
            await message.answer('👍 👌', reply_markup=client_kb.kb_client)
        # здесь мы сохраняем наш state в базу даных черех функцию которую создадим позже
        await state.finish()

# Начало диалога загрузки нового пункта меню УСЛОВИЯ ДОСТАВКИ
@dp.message_handler(commands='Доставка', state=None)
async def start_doastavka(message: types.Message):
    if message.from_user.id in FAM:
        q = f'Условия доставки, которые видит клиент при формировании' \
            f' заказа:\n=\n{dostavka}\n=\n' \
            f'Если нужно поменять условия - напиши новые сообщением\n' \
            f'PS:если нужно отменить процесс - нажми на команду:\n/cancel'
        await FSMAdmin.Dostavka.set()
        await message.answer(q)
        await message.delete()

# ловим 1-й и последний ответ и перезаписываем новые условия доставки:
@dp.message_handler(state=FSMAdmin.Dostavka)
async def Dostavka(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        global dostavka
        dostavka = message.text
        async with state.proxy() as date:
            date['Dostavka'] = message.text
        async with state.proxy() as base:
            await bot.send_message(chat, base)
        await message.answer('👍 👌', reply_markup=client_kb.kb_client)
        await state.finish()


# Начало диалога загрузки нового пункта меню ТЕКТ ДЛЯ РАССЫЛКИ
@dp.message_handler(commands='Текст', state=None)
async def start_Text(message: types.Message):
    if message.from_user.id in FAM:
        q = f'Текст, который видит клиент при рассылки ботом ' \
            f'смс:\n=\n{text_fire}=\n' \
            f'Если нужно поменять этот текст - напиши новый сообщением\n' \
            f'PS:если нужно отменить процесс - нажми на команду:\n/cancel'
        await FSMAdmin.Text_.set()
        await message.answer(q)
        await message.delete()

# ловим 1-й и последний ответ и перезаписываем текст для рассылки:
@dp.message_handler(state=FSMAdmin.Text_)
async def Text_(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        global text_fire
        text_fire = message.text
        async with state.proxy() as date:
            date['Text'] = message.text
        async with state.proxy() as base:
            await bot.send_message(chat, base)
        await message.answer('👍 👌', reply_markup=client_kb.kb_client)
        await state.finish()
