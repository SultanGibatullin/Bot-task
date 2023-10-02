import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from settings import KEY, URL
from data_post import post


TOKEN = KEY
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Добрый день, отправьте свой токен")


@dp.message()
async def message_handler(message: types.Message) -> None:
    try:
        status = await post(f'{URL}/tokens/{message.text}/',
                             message.chat.id)
        if status == 200:
             await message.answer("Токен зарегистрирован")
        else:
             await message.answer("Ключ не найден")
    except TypeError:
        await message.answer("Ключ не найден")

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())