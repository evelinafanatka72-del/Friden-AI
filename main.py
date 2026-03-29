import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Настройки (токен подтянется из GitHub Secrets)
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню с кнопками под сообщением
def main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🎨 Создать фото", callback_data="gen_photo"))
    builder.row(types.InlineKeyboardButton(text="🎬 Создать видео", callback_data="gen_video"))
    builder.row(types.InlineKeyboardButton(text="🔧 Изменить моё фото", callback_data="edit_photo"))
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🦆 Привет! Я Friden AI. Что будем творить сегодня?", reply_markup=main_menu())

# Хендлер для нажатия на кнопки (Callback)
@dp.callback_query(F.data == "gen_photo")
async def press_gen_photo(callback: types.Callback_query):
    await callback.message.answer("🖼 Напиши, что именно хочешь увидеть на фото?")
    await callback.answer()

@dp.callback_query(F.data == "gen_video")
async def press_gen_video(callback: types.Callback_query):
    await callback.message.answer("🎥 Опиши сцену для короткого видео:")
    await callback.answer()

@dp.callback_query(F.data == "edit_photo")
async def press_edit_photo(callback: types.Callback_query):
    await callback.message.answer("📸 Просто пришли мне фото, и в описании напиши, что в нем изменить!")
    await callback.answer()

async def main():
    print("🚀 Friden AI: Медиа-бот запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
