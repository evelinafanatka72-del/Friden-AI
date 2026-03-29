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
async def press_gen_photo(callback: types.Callback_query):
    await callback.message.answer("🖼 **Режим фото.** Напиши, что мне нарисовать? (например: 'Кот в космосе в стиле киберпанк')")
    await callback.answer()

@dp.callback_query(F.data == "gen_video")
async def press_gen_video(callback: types.Callback_query):
    await callback.message.answer("🎥 **Режим видео.** Опиши короткую сцену, которую хочешь оживить:")
    await callback.answer()

@dp.callback_query(F.data == "edit_media")
async def press_edit_media(callback: types.Callback_query):
    await callback.message.answer("📸 **Режим правки.** Просто пришли мне фото или видео, а в описании к нему напиши, что нужно изменить.")
    await callback.answer()

# Хендлер для получения фото от пользователя
@dp.message(F.photo)
async def handle_user_photo(message: types.Message):
    await message.reply("📸 Я получил твое фото! Дай мне секунду, чтобы проанализировать его...")
    # Здесь в будущем будет логика изменения через ИИ

# Хендлер для любого текста (если это описание для генерации)
@dp.message(F.text & ~F.status_text.startswith('/'))
async def handle_text_requests(message: types.Message):
    await message.answer("🛠 Принял запрос! Начинаю обработку в Friden AI Core... 🚀")
    # Здесь будет вызов API для генерации

async def main():
    print("🚀 Бот Friden AI запущен и готов генерировать!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
