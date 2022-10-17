from aiogram.utils import executor
from create_bot import dp
import client, admin, sklad, other



async def on_startup(_):
    print('Aqua-Berezivka_bot online 💙💛')





executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
