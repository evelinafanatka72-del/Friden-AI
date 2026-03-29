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
        f"🦆 **Friden AI** на связи!\n\nЯ подключен к ядрам генерации. Что создадим?",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "gen_photo")
async def press_gen_photo(callback: types.CallbackQuery):
    await callback.message.answer("🖼 **Режим фото.** Опиши, что нарисовать?")
    await callback.answer()

@dp.callback_query(F.data == "gen_video")
async def press_gen_video(callback: types.CallbackQuery):
    await callback.message.answer("🎥 **Режим видео.** Напиши сюжет для анимации:")
    await callback.answer()

@dp.callback_query(F.data == "edit_media")
async def press_edit_media(callback: types.CallbackQuery):
    await callback.message.answer("📸 **Режим правки.** Пришли файл и напиши, что изменить.")
    await callback.answer()

# Хендлер для фото
@dp.message(F.photo)
async def handle_user_photo(message: types.Message):
    wait_msg = await message.answer("📸 Фото получено. Анализирую структуру пикселей...")
    await asyncio.sleep(2)
    await wait_msg.edit_text("⚙️ Применяю нейросетевые фильтры Friden AI... 🚀")
    # Тут можно добавить логику обработки через Pillow

# Хендлер для текста (ГЕНЕРАЦИЯ)
@dp.message(F.text)
async def handle_text_requests(message: types.Message):
    if message.text.startswith('/'):
        return
    
    # Эффект живой генерации
    status_msg = await message.answer(f"🔄 Запрос: «{message.text}»\n\n[░░░░░░░░░░] 0%")
    
    await asyncio.sleep(1)
    await status_msg.edit_text(f"🔄 Запрос: «{message.text}»\n\n[▓▓▓░░░░░░░] 30% — Сборка промпта...")
    
    await asyncio.sleep(1.5)
    await status_msg.edit_text(f"🚀 Запрос: «{message.text}»\n\n[▓▓▓▓▓▓▓░░░] 70% — Рендеринг в облаке...")
    
    await asyncio.sleep(1)
    await status_msg.edit_text(f"✅ Готово! Отправляю результат...")
    
    # Если ты напишешь "Злая утка", бот может ответить чем-то особенным
    if "утка" in message.text.lower():
         await message.answer_sticker("CAACAgIAAxkBAAEL...") # Если есть стикер
         await message.answer("🦆 Ваша злая утка готова! (Здесь будет файл)")
    else:
         await message.answer("🎨 Контент успешно сгенерирован в Friden AI Core!")

async def main():
    print("🚀 Бот Friden AI запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот выключен")
