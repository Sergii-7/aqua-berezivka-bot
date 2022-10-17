from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import dp, bot
import client_kb, order_kb, info_kb
from note import num, the_date, chat, FAM, dostavka, text_fire

class FSM_zakaz(StatesGroup):
    Alaska = State()
    Morshinska = State()
    Pompa = State()
    Zametka = State()


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    user_id = message.from_user.id
    mess = f'Привіт, {message.from_user.first_name}!\n' \
           f'Для отримання інформації про наші товари натисніть кнопку:\n/info\n' \
           f'Щоб зробити замовлення, натисніть кнопку\n/order Замовити воду'
    try:
        await bot.send_message(message.from_user.id, mess, reply_markup=client_kb.kb_client)
        await message.delete()
    except:
        await message.reply('Спілкування з ботом через особисте повідомлення,\
        напиши йому:\nhttps://t.me/AquaBerezivkaBot')
    l = set()
    with open('clients.txt', 'r') as f:
        for i in f.read().split(' '):
            l.add(int(i))
    l.add(int(user_id))
    with open('clients.txt', 'w') as f:
        st = str(l)
        for i in st:
            if i in num or i == ' ':
                f.write(str(i))

ame = 'Некоректне значення!\nНадішліть лише цифру, наприклад: 2 або 3'
ame2 = "Якщо ви дійсно хочете замовити таку кількість, "\
       "зв'яжіться, будь ласка, за цим контактом, щоб " \
       "отримати можливу знижку:\n@OlgaBeshlyaga"
# запуск процесса приема заказов
@dp.message_handler(commands=['order', 'Замовити'], state=None)
async def menu_commands(message: types.Message):
    with open('alaska_price.txt', 'r') as a:
        s = a.read()
    i = 'Аляска'
    q = f'{i} {s} грн\n' \
         f'Напишіть у відповідь на це повідомлення скільки ' \
         f'бутлів {i} необхідно вам привезти.\n' \
         f'Якщо ви не планували замовляти воду {i} надішліть 0'
    with open('Аляска.png', 'rb') as photo:
        await message.answer_photo(photo, q, reply_markup=order_kb.button_order)
    await message.delete()
    await FSM_zakaz.Alaska.set()

#Выход из состояний если потребуется прервать процесс
@dp.message_handler(state="*", commands=['скасувати'])
@dp.message_handler(Text(equals='s', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    c = 'Добре\n💙💛\nБережіть себе та своїх близьких!'
    await message.answer(c, reply_markup=client_kb.kb_client)
    await state.finish()

#Ловим 1 ответ и пишем в словарь
@dp.message_handler(state=FSM_zakaz.Alaska)
async def zakaz_Alaska(message: types.Message, state: FSMContext):
    with open('morshin_price.txt', 'r') as a:
        s = a.read()
    i = 'Моршинська'
    q = f'{i} {s} грн\n' \
        f'Напишіть у відповідь на це повідомлення скільки ' \
        f'бутлів {i} необхідно вам привезти.\n' \
        f'Якщо ви не планували замовляти воду {i} надішліть 0'
    if message.text == '/пропустити цю позицію':
        async with state.proxy() as data:
            data['Alaska'] = 0
        with open('Моршинская.png', 'rb') as photo:
            await message.answer_photo(photo, q)
        await FSM_zakaz.next()
    else:
        for x in message.text:
            if x not in num:
                await message.answer(ame)
                break
            elif x in num:
                continue
        if abs(int(message.text)) > 10:
            await message.reply(ame2, reply_markup=client_kb.kb_client)
            await state.finish()
        elif 10 >= int(message.text) >= -10:
            a = abs(int(message.text))
            async with state.proxy() as data:
                data['Alaska'] = a
            with open('Моршинская.png', 'rb') as photo:
                await message.answer_photo(photo, q)
            await FSM_zakaz.next()

#Ловим 2 ответ и пишем в словарь
@dp.message_handler(state=FSM_zakaz.Morshinska)
async def zakaz_Morshinska(message: types.Message, state: FSMContext):
    with open('pompa_price.txt', 'r') as a:
        s = a.read()
        i = 'Помпа механічна'
        q = f'{i} {s} грн\n' \
            f'Якщо ви бажаєте придбати помпу, напишіть цифру 1 ' \
            f'(або іншу необхідну кількість).\n' \
            f'Якщо ви не плануєте купувати помпу, напишіть 0.'
    if message.text == '/пропустити цю позицію':
        async with state.proxy() as data:
            data['Morshinska'] = 0
        with open('Помпа.png', 'rb') as photo:
            await message.answer_photo(photo, q)
        await FSM_zakaz.next()
    else:
        for x in message.text:
            if x not in num:
                await message.answer(ame)
                break
            elif x in num:
                continue
        if abs(int(message.text)) > 10:
            await message.reply(ame2, reply_markup=client_kb.kb_client)
            await state.finish()
        elif 10 >= int(message.text) >= -10:
            m = abs(int(message.text))
            async with state.proxy() as data:
                data['Morshinska'] = m
            with open('Помпа.png', 'rb') as photo:
                await message.answer_photo(photo, q)
            await FSM_zakaz.next()

#Ловим 3 ответ и пишем в словарь
@dp.message_handler(state=FSM_zakaz.Pompa)
async def zakaz_Pompa(message: types.Message, state: FSMContext):
    q = f'Напишіть примітку до замовлення. Наприклад, вашу адресу, або ' \
        f'щоб ми вам зателефонували.\n' \
        f'Якщо у вас немає примітки, можете надіслати 0 або -, або *, або будь-що.'
    if message.text == '/пропустити цю позицію':
        async with state.proxy() as data:
            data['Pompa'] = 0
        with open('примітка.png', 'rb') as photo:
            await message.answer_photo(photo, q)
        await FSM_zakaz.next()
    else:
        for x in message.text:
            if x not in num:
                await message.answer(ame)
                break
            elif x in num:
                continue
        if abs(int(message.text)) > 5:
            await message.reply(ame2, reply_markup=client_kb.kb_client)
            await state.finish()
        elif 5 >= int(message.text) >= -5:
            p = abs(int(message.text))
            async with state.proxy() as data:
                data['Pompa'] = p
            with open('примітка.png', 'rb') as photo:
                await message.answer_photo(photo, q)
            await FSM_zakaz.next()

#Ловим 4 ответ и пишем в словарь
@dp.message_handler(state=FSM_zakaz.Zametka)
async def zakaz_Zametka(message: types.Message, state: FSMContext):
    if message.text == '/пропустити цю позицію':
        async with state.proxy() as data:
            data['Zametka'] = '-'
    elif message.text != '/пропустити цю позицію':
        async with state.proxy() as data:
            data['Zametka'] = message.text
    async with state.proxy() as base:
        bs = base
    smg = f'Користувач {message.from_user} \n' \
          f'зробив замовлення:\n{bs}'
    await bot.send_message(chat, smg)
    alaska = data['Alaska']
    morshin = data['Morshinska']
    pompa = data['Pompa']
    note = data['Zametka']
    with open('alaska_price.txt', 'r') as ap:
        alaska_price = float(ap.read())
    with open('morshin_price.txt', 'r') as mp:
        morshin_price = float(mp.read())
    with open('bottle_price.txt', 'r') as bp:
        bottle_price = float(bp.read())
    with open('pompa_price.txt') as pp:
        pompa_price = float(pp.read())
    total = alaska * alaska_price + morshin * morshin_price \
            + pompa * pompa_price
    bill = f'ФОП Бешляга Михайло Михайлович\n' \
           f'IBAN: UA183220010000026006320059503\n' \
           f'ІПН/ЄДРПОУ: 2116415395\n' \
           f'м/т +38(098)476-03-68\n\n' \
           f'рахунок від {the_date}\n\n' \
           f'питна вода Аляска 18,9л:\n' \
           f'{alaska} x {alaska_price} грн\n' \
           f'питна вода Моршинська 18,9л:\n' \
           f'{morshin} x {morshin_price} грн\n' \
           f'Помпа механічна:\n{pompa} * {pompa_price} грн\n' \
           f'примітка:\n- {note} -\n\n' \
           f'разом: {total} грн\n\n' \
           f'PS: підготуйти *{alaska + morshin}* порожніх бутлів на обмін. ' \
           f'або додаткову суму грошей ' \
           f'із розрахунку *{bottle_price}* грн за один бутль.'
    if total == 0:
        await message.answer('Ви нічого не замовили. '
                             'Не засмучуйтесь, спробуйте ще раз.',
                             reply_markup=client_kb.kb_client)
        await state.finish()
    else:
        await message.answer(bill, reply_markup=client_kb.kb_client)
        await state.finish()
        await message.answer(f'Дякуємо за замовлення!\n'
                             f'{dostavka}'
                             f'\n💙💛\nБережіть себе та своїх близьких!')

@dp.message_handler(commands=['info'])
async def menu_commands(message: types.Message):
    info_ = 'Виберіть товар, що цікавить, або можете відразу зробити замовлення.'
    await bot.send_message(message.from_user.id, info_, reply_markup=info_kb.button_info)
    await message.delete()

@dp.message_handler(commands=['Fire'])
async def menu_commands(message: types.Message):
    if message.from_user.id in FAM:
        ct2 = ' 💙💛'
        ct = text_fire+ct2
        s = set()
        with open('clients.txt', 'r') as f:
            for i in f.read().split(' '):
                s.add(int(i))
        for i in s:
            try:
                await bot.send_message(i, ct)
            except:
                'Chat not found'
        await bot.send_message(chat, f'база клиентов:{s}')
        await message.delete()