import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from os import getenv
from start import start_router
from homeworks import homework_router


async def main():
    load_dotenv()
    bot = Bot(token=getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(homework_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
