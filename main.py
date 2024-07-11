from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()
TOKEN = os.getenv('TOKEN')
mybot = Bot(token=TOKEN)


async def main():
    from handlers.initial_handler import router
    from handlers.submit_handler import router_submit
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(router_submit)
    await dp.start_polling(mybot)


if __name__ == '__main__':
    asyncio.run(main())
