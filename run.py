from aiogram import Bot, Dispatcher
import os
import asyncio
from dotenv import load_dotenv
from app.handlers.start_handler import start_router
from database.models import async_main
from app.handlers.admin import admin_router

load_dotenv()

async def on_shutdown(bot):
    print("Бот устал")

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

async def main():
    await async_main()
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход")
