from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from note import FAM, num, the_time, the_date, chat

class FSM_sklad(StatesGroup):
    Alaska = State()
    Morshinska = State()
    Bottle = State()
    Pompa = State()


q = 'Напиши сколько пришло или ушло\n'\
    'Отмена нажми:\n/cancel'


ame = 'Некорректное значение!\nОтправь только цифру, например: +10 или -10'

#Начало диалога загрузки нового пункта меню
@dp.message_handler(commands='Sklad', state=None)
async def sklad_start(message: types.Message):
    if message.from_user.id in FAM:
        with open('sklad_Alaska.txt', 'r') as a:
            s = a.read()
        i = 'Аляска'
        q0 = f'Текущий остаток {i}\nсоставляет {s}шт\n'

        await FSM_sklad.Alaska.set()
        with open('Аляска.png', 'rb') as photo:
            await message.answer_photo(photo, q0 + q)
        await message.delete()

#Выход из состояний если потребуется прервать процесс
@dp.message_handler(state="*", commands='cancel')
@dp.message_handler(Text(equals='s', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        current_state = await state.get_state()
        if current_state is None:
            return
        c = 'Добре\n💙\n💛\nБережи себе та своїх близьких!'
        await message.answer(c, reply_markup=client_kb.kb_client)
        await state.finish()

#Ловим 1 ответ и пишем в словарь
@dp.message_handler(state=FSM_sklad.Alaska)
async def sklad_Alaska(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        for x in message.text:
            if x not in num:
                await message.delete()
                await message.answer(ame)
                break
            elif x in num:
                continue
        if int(message.text) > -10000:
            with open('sklad_Morshinska.txt', 'r') as a:
                s = a.read()
            i = 'Моршинська'
            q0 = f'Текущий остаток {i}\nсоставляет {s}шт\n'
            with open('sklad_Alaska.txt', 'r') as a:
                s = int(a.read())
            with open('sklad_Alaska.txt', 'w') as a:
                a.write(str(s + int(message.text)))
            async with state.proxy() as data:
                data['Alaska'] = int(message.text)
            aa = f'=принято=\nНовый остаток Аляска = {str(s + int(message.text))}шт'
            await message.reply(aa)
            with open('Моршинская.png', 'rb') as photo:
                await message.answer_photo(photo, q0 + q)
            await FSM_sklad.next()

#Ловим 2 ответ
@dp.message_handler(state=FSM_sklad.Morshinska)
async def sklad_Morshinska(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        for x in message.text:
            if x not in num:
                await message.delete()
                await message.answer(ame)
                break
            elif x in num:
                continue
        if int(message.text) > -10000:
            with open('sklad_Bottle.txt', 'r') as a:
                s = a.read()
            i = 'Бутли'
            q0 = f'Текущий остаток {i}\nсоставляет {s}шт\n'
            with open('sklad_Morshinska.txt', 'r') as a:
                s = int(a.read())
            with open('sklad_Morshinska.txt', 'w') as a:
                a.write(str(s + int(message.text)))
            async with state.proxy() as data:
                data['Morshinska'] = int(message.text)
            aa = f'=принято=\nНовый остаток Моршинска = {str(int(s) + int(message.text))}шт'
            await message.reply(aa)
            with open('Bottle.png', 'rb') as photo:
                await message.answer_photo(photo, q0 + q)
            #await message.answer(q0 + q)
            await FSM_sklad.next()

#Ловим 3 ответ
@dp.message_handler(state=FSM_sklad.Bottle)
async def sklad_Bottle(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        for x in message.text:
            if x not in num:
                await message.delete()
                await message.answer(ame)
                break
            elif x in num:
                continue
        if int(message.text) > -10000:
            with open('sklad_Pompa.txt', 'r') as a:
                s = a.read()
            i = 'Помп'
            q0 = f'Текущий остаток {i}\nсоставляет {s}шт\n'
            with open('sklad_Bottle.txt', 'r') as a:
                s = int(a.read())
            with open('sklad_Bottle.txt', 'w') as a:
                a.write(str(s + int(message.text)))
            async with state.proxy() as data:
                data['Bottle'] = int(message.text)
            aa = f'=принято=\nНовый остаток Бутли = {str(int(s) + int(message.text))}шт'
            await message.reply(aa)
            with open('Помпа.png', 'rb') as photo:
                await message.answer_photo(photo, q0 + q)
            #await message.answer(q0 + q)
            await FSM_sklad.next()

#Ловим 4 последний ответ и используем полученые данные
@dp.message_handler(state=FSM_sklad.Pompa)
async def sklad_Pompa(message: types.Message, state: FSMContext):
    if message.from_user.id in FAM:
        for x in message.text:
            if x not in num:
                await message.delete()
                await message.answer(ame)
                break
            elif x in num:
                continue
        if int(message.text) > -10000:
            with open('sklad_Pompa.txt', 'r') as a:
                s = int(a.read())
            with open('sklad_Pompa.txt', 'w') as a:
                a.write(str(s + int(message.text)))
            async with state.proxy() as data:
                data['Pompa'] = int(message.text)
            aa = f'=принято=\nНовый остаток Помп = {str(int(s) + int(message.text))}шт'
            await message.reply(aa)
            async with state.proxy() as base:
                await bot.send_message(chat, f'СКЛАД Приход/Расход на {the_date}\n{base}')
                await message.answer('👍 👌\nпосмотреть остатки по складу:\n/Ostatki')
                await state.finish()

#формирует и показывает остатки по складу:
@dp.message_handler(commands='Ostatki', state=None)
async def sklad_ostatok(message: types.Message):
    if message.from_user.id in FAM:
        with open('sklad_Alaska.txt', 'r') as a:
            a_s = int(a.read())
        with open('alaska_price.txt', 'r') as ap:
            a_p = float(ap.read())
        with open('sklad_Morshinska.txt', 'r') as m:
            m_s = int(m.read())
        with open('morshin_price.txt', 'r') as mp:
            m_p = float(mp.read())
        with open('sklad_Bottle.txt', 'r') as sb:
            s_b = int(sb.read())
        with open('bottle_price.txt', 'r') as bp:
            b_p = float(bp.read())
        with open('sklad_Pompa.txt', 'r') as sp:
            s_p = int(sp.read())
        with open('pompa_price.txt', 'r') as pp:
            p_p = float(pp.read())
        total = a_s*(a_p+b_p) + m_s*(m_p+b_p) + s_b*b_p + s_p*p_p
        sklad = f'Залишки на складі Aqua-Berezivka станом на:'\
                f'\nчас {the_time} дата {the_date}\n\n'\
                f'Питна вода Аляска 18,9л:\n' \
                f'{a_s} * ({a_p} + {b_p}) грн\n' \
                f'Питна вода Моршинська 18,9л:\n' \
                f'{m_s} * ({m_p} + {b_p}) грн\n' \
                f'Порожній бутль 18,9л:\n' \
                f'{s_b} * {b_p} грн\n'\
                f'Помпа механічна:\n' \
                f'{s_p} *{p_p} грн\n\n' \
                f'Загальна вартість товару складає:' \
                f'{total} грн.'
        await message.answer(sklad)
        await message.delete()