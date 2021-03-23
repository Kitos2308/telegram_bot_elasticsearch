
import requests

import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN

loop=asyncio.get_event_loop()

bot=Bot(BOT_TOKEN, parse_mode="HTML")
storage=MemoryStorage()
dp=Dispatcher(bot, loop=loop, storage=storage)

