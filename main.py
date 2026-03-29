import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Конфигурация
TOKEN = os.getenv("BOT_TOKEN")
AI_KEY = os.getenv("GEMINI_API_KEY") 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Кнопки ---
def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🎨 Создать фото", callback_data="gen_photo"))
    builder.row(types.InlineKeyboardButton(text="🎬 Создать видео", callback_data="gen_video"))
    builder.row(types.InlineKeyboardButton(text="🔧 Изменить моё фото/видео", callback_data="edit_media"))
    return builder.as_markup()

# --- Логика ИИ ---
async def get_ai_prompt(text, mode):
    task = f"Create a detailed English prompt for {mode} based on: {text}. Output ONLY the prompt."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={AI_KEY}"
    payload = {"contents": [{"parts": [{"text": task}]}]}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data['candidates'][0]['content']['parts'][0]['text']
            return "⚠️ Ошибка связи с ИИ. Проверь ключ в GitHub!"

# --- Хендлеры ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🦆 **Friden AI Core** активен!\n\nВыбери режим работы:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "gen_photo")
async def press_photo(callback: types.CallbackQuery):
    await callback.message.answer("🖼 **Режим ФОТО.** Опиши, что нарисовать?")
    await callback.answer()

@dp.callback_query(F.data == "gen_video")
async def press_video(callback: types.CallbackQuery):
    await callback.message.answer("🎥 **Режим ВИДЕО.** Напиши сюжет для ролика:")
    await callback.answer()

@dp.callback_query(F.data == "edit_media")
async def press_edit(callback: types.CallbackQuery):
    await callback.message.answer("📸 **Режим ПРАВКИ.** Пришли фото/видео и напиши, что изменить.")
    await callback.answer()

# Хендлер для ФОТО (если пользователь прислал картинку)
@dp.message(F.photo)
async def handle_user_photo(message: types.Message):
    await message.answer("📸 **Фото получено!**\n\nТеперь напиши текстом (ответом на это фото), что именно нужно изменить или добавить. Я составлю промпт для нейросети!")

# Хендлер для ТЕКСТА
@dp.message(F.text)
async def handle_msg(message: types.Message):
    if message.text.startswith('/'): return
    
    status = await message.answer("📡 *Friden AI готовит промпт...*")
    
    # Пытаемся понять режим (по контексту)
    mode = "image editing" if "ПРАВКИ" in (message.reply_to_message.text if message.reply_to_message else "") else "generation"
    
    prompt = await get_ai_prompt(message.text, mode)
    
    await status.edit_text(
        f"✅ **Промпт готов!**\n\nСкопируй его и отправь мне (в чат с Gemini):\n\n`{prompt}`\n\n_Я сразу сделаю магию!_",
        parse_mode="Markdown"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            import time
            time.sleep(5)
