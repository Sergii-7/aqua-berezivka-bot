from aiogram import types, Dispatcher
from create_bot import dp, bot
import json, string
from note import FAM, the_date
import case_admin

@dp.message_handler()
async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('censorship.json')))) != set():
        await message.reply('Матюки в чаті заборонені!')
        await message.delete()
    elif {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('cens_english.json')))) != set():
        await message.reply('Profanity is prohibited in the chat!')
        await message.delete()
    elif message.text == 'Слава Україні!':
        await message.answer('Героям Слава!')

    elif message.text == 'Аляска':
        with open('alaska_price.txt', 'r') as ap:
            a = float(ap.read())
        text_ = f"{a} грн\n" \
                f"Аляска - кришталево чиста вода, з ідеальним балансом корисних мінералів. " \
                f"Срібний призер міжнародного конкурсу Gourmet Waters у 2017 році. " \
                f"Об'єм бутля - 18,9л\n" \
                f"Ключові переваги негазованої питної води «Аляска»:\nЗавдяки походженню з " \
                f"підземних джерел та свердловин екологічно чистих районів України (Миргород, Моршин, Гола Пристань), " \
                f"далеко від виробництв, вона збагачена природними мінералами та корисними мікроелементами.\n" \
                f"Ретельне очищення відбувається на нових фільтрах, зберігаючи природну структуру води.\n" \
                f"Проходить багатоступінчастий контроль якості (8 етапів), тому гарантовано відповідає " \
                f"міжнародним стандартам безпеки продукції ISO 22000.\n" \
                f"Воду «Аляска» варто купити тому, що вона не залишає осаду та нальоту на чайнику під час кип'ятіння.\n" \
                f"Підходить для пиття та приготування чаю, кави, інших напоїв та їжі, не впливає на смак продуктів.\n" \
                f"Воду «Аляска» можно використовувати у кавомашинах для приготування смачної кави, " \
                f"при цьому техніка не псується від осаду."
        with open('Аляска.png', 'rb') as photo:
            await message.answer_photo(photo)
        await message.answer(text_)
        await message.delete()

    elif message.text == 'Моршинська':
        with open('morshin_price.txt', 'r') as mp:
            m = float(mp.read())
        text_ = f'{m} грн\n' \
                f'Моршинська 18,9л – мінеральна природна столова вода, зі ' \
                f'збалансованим складом, яка повністю сприймається тілом і відновлює його ' \
                f'щодня. Вода походить з моршинської долини, що розкинулась поблизу східного ' \
                f'схилу Карпатського хребта та самотужки прокладає собі шлях на поверхню землі. ' \
                f'Моршинська обробляється виключно за допомогою механічної фільтрації, ' \
                f'що не порушує її природний склад. Ціна Моршинської 18,9 л ' \
                f'набагато вигідніша за покупку води в пляшках. До того ж бутильовану воду ' \
                f'набагато зручніше використовувати у побуті вдома та в офісах. Бутлі багаторазові ' \
                f'та допомагають знизити використання пластику.'
        with open('Моршинская.png', 'rb') as photo:
            await message.answer_photo(photo)
        await message.answer(text_)
        await message.delete()

    elif message.text == 'Помпа':
        with open('pompa_price.txt', 'r') as pp:
            p = float(pp.read())
        text_ = f'{p} грн\n' \
                f'До комплекту разом із помпою входять: носик для розливу води, три трубки для ' \
                f'набору та одноразові рукавички для гігієнічності введення пристрою в експлуатацію.\n' \
                f'ХАРАКТЕРИСТИКИ\n' \
                f'ВАГА 340г\n' \
                f'РОЗМІРИ 21Х13Х13 СМ\n' \
                f'ПРИЗНАЧЕННЯ ДЛЯ ПОДАЧІ ВОДИ З БУТЛІВ 18,9 Л\n' \
                f'МАТЕРІАЛ ЯКІСНИЙ І БЕЗПЕЧНИЙ ПЛАСТИК, ЩО НЕ ВПЛИВАЄ НА СМАКОВІ ВЛАСТИВОСТІ ПИТНОЇ ВОДИ\n' \
                f'КРАЇНА ВИРОБНИК ТУРЕЧЧИНА\n' \
                f'ГАРАНТІЯ 12 МІС'
        with open('Помпа.png', 'rb') as photo:
            await message.answer_photo(photo)
        await message.answer(text_)
        await message.delete()

    elif message.text == 'Кулери':
        with open('кулер_price.txt', 'r') as pp:
            p = float(pp.read())
        text_ = f'від {p} грн\n' \
                f'весь асортимент представлений тут:\n' \
                f'https://mywatershop.ua/catalog/kulery/\n' \
                f'Контакт для погодження умов замовлення:\n' \
                f'@OlgaBeshlyaga'
        with open('Кулер.png', 'rb') as photo:
            await message.answer_photo(photo)
        await message.answer(text_)
        await message.delete()

    elif message.text == '/Price' and message.from_user.id in FAM:
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
                 f'Ціни станом на {the_date}:\n\n' \
                 f'вода Аляска 18,9л = {alaska_p} грн\n' \
                 f'вода Моршинська 18,9n = {morshin_p}\n' \
                 f'порожній бутль 18,9n =  {bottle_p} грн\n' \
                 f'Помпа механічна = {pompa_p} грн\n' \
                 f'Кулери від = {kuler_p} грн'
        await message.answer(report)
        await message.delete()

    for n in message.text.split(' '):
        if n == '777' and message.from_user.id in FAM:
            await bot.send_message(message.from_user.id,
                                   'Выписать счет для клиента:\n/Rahunok\n\n'
                                   'Посмотреть цены на товары:\n/Price'
                                   '\n\nПоменять цены на товары:\n'
                                   '/Ціни\n\nПоменять фото товаров:'
                                   '\n/Фото\n\nПоменять условия доставки:\n/Доставка\n\n'
                                   'Изменить текст рассылки для клиентов:\n/Текст'
                                   '\n\nЗапустить рассылку для клиентов:\n/Fire'
                                   '\n\nСклад приход\расход:'
                                   '\n/Sklad\n\nПосмотреть остатки по складу:'
                                   '\n/Ostatki', reply_markup=case_admin.button_case_admin)
            await message.delete()
            break
        elif n.lower() == 'привіт' or n.lower() == 'привіт!' or n.lower() == 'доброго' \
                or n.lower() == 'hi' or n.lower() == 'hello' or n.lower() == 'hi!' \
                or n.lower() == 'hello!' or n.lower() == 'привет' \
                or n.lower() == 'привет!' or n.lower() == 'добрый':
            await message.reply('👋')
            break
