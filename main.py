import os
import asyncio
from dotenv import load_dotenv # Эта библиотека умеет открывать .env
from aiogram import Bot, Dispatcher, types

# 1. Говорим программе: "Открой сейф .env"
load_dotenv()

# 2. Достаем токен из памяти (в коде его НЕТ!)
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ ОШИБКА: Токен не найден в файле .env!")
    exit()

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Дальше идет твоя логика Friden AI...
@dp.message()
async def welcome(message: types.Message):
    await message.answer("🦆 **Friden AI** успешно подключен к защищенному токену!")

async def main():
    print("🚀 [SYSTEM] Friden AI запущен. Токен скрыт.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
