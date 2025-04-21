import asyncio
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from aiogram import Bot, Dispatcher

from handlers.user_private import user_router
from handlers.calback import calback_router
from db.database import init_db

dp = Dispatcher()
bot = Bot(token=os.getenv('TOKEN'))


async def main():
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        
    webhook_response = await bot.delete_webhook(drop_pending_updates=True)
    if webhook_response:
        print('OK')
    else:
        print('Ошибка при удалении webhook.')

        
    dp.include_router(user_router)
    dp.include_router(calback_router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == '__main__':
    init_db()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')
