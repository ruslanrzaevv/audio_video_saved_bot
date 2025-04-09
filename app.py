import asyncio
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from aiogram import Bot, Dispatcher

from handlers.user_private import user_router
from handlers.calback import calback_router

dp = Dispatcher()
bot = Bot(token=os.getenv('TOKEN'))


async def main():
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    dp.include_router(user_router)
    dp.include_router(calback_router)

    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')
