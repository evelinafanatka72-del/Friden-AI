import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Конфигурация
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Генератор кнопок меню
def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🎨 Сгенерировать фото", callback_data="gen_photo"))
    builder.row(types.InlineKeyboardButton(text="🎬 Сгенерировать видео", callback_data="gen_video"))
    builder.row(types.InlineKeyboardButton(text="🔧 Изменить моё фото/видео", callback_data="edit_media"))
    return builder.as_markup()

# --- Хендлеры сообщений ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"🦆 **Friden AI** готов к работе!\n\nЯ могу создавать контент по твоему описанию или редактировать твои файлы.",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "gen_photo")
async def press_gen_photo(callback: types.CallbackQuery):
    await callback.message.answer("🖼 **Режим фото.** Напиши, что мне нарисовать? (например: 'Кот в космосе в стиле киберпанк')")
    await callback.answer()

@dp.callback_query(F.data == "gen_video")
async def press_gen_video(callback: types.CallbackQuery):
    await callback.message.answer("🎥 **Режим видео.** Опиши короткую сцену, которую хочешь оживить:")
    await callback.answer()

@dp.callback_query(F.data == "edit_media")
async def press_edit_media(callback: types.CallbackQuery):
    await callback.message.answer("📸 **Режим правки.** Просто пришли мне фото или видео, а в описании к нему напиши, что нужно изменить.")
    await callback.answer()

# Хендлер для получения фото от пользователя
@dp.message(F.photo)
async def handle_user_photo(message: types.Message):
    await message.reply("📸 Я получил твое фото! Дай мне секунду, чтобы проанализировать его...")

# Хендлер для любого текста (если это описание для генерации)
@dp.message(F.text)
async def handle_text_requests(message: types.Message):
    # Игнорируем команды, чтобы не было конфликтов
    if message.text.startswith('/'):
        return
    await message.answer("🛠 Принял запрос! Начинаю обработку в Friden AI Core... 🚀")

async def main():
    print("🚀 Бот Friden AI запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот выключен")
