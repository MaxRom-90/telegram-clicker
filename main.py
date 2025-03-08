import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram import Router


# --- Настройки ---
BOT_TOKEN = "7758985947:AAH7BVZHtLzlgbPB9Fk-vuVIl-1Mo78EC_w"  # Ваш токен 2
WEB_APP_URL = "https://maxrom-90.github.io/telegram-clicker/game.html"  # Ваш Web App
SCORES_FILE = "scores.json"

# --- Инициализация бота и диспетчера ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Работа с JSON ---
def load_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Ошибка загрузки scores.json: {e}")
            return {}
    return {}

def save_scores(scores):
    try:
        with open(SCORES_FILE, "w", encoding="utf-8") as file:
            json.dump(scores, file, indent=4, ensure_ascii=False)
        print("Данные сохранены в scores.json:", scores)
    except Exception as e:
        print(f"Ошибка сохранения scores.json: {e}")

# --- Команда /start ---
@dp.message(Command("start"))
async def start(message: types.Message):
    # Создаем клавиатуру с кнопкой для открытия Mini App
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="▶️ Играть", web_app=WebAppInfo(url=WEB_APP_URL))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(
        "Нажмите кнопку ниже, чтобы начать игру!",
        reply_markup=keyboard
    )

# --- Обработка данных из Mini App ---
@dp.message()
async def handle_web_app_data(message: types.Message):
    if message.web_app_data:
        try:
            print("\n--- Получены RAW данные ---")
            print("Веб-данные:", message.web_app_data)
            print("Сырые данные:", message.web_app_data.data)
            
            user_id = message.from_user.id
            data = json.loads(message.web_app_data.data)
            clicks = data["clicks"]
            print(f"Данные получены от пользователя {user_id}: {clicks} кликов.")
            
            scores = load_scores()
            print("Текущие данные из scores.json:", scores)
            
            scores[str(user_id)] = max(clicks, scores.get(str(user_id), 0))
            save_scores(scores)
            
            await message.answer(
                f"🏆 Результат: *{clicks}* кликов\n"
                f"🏅 Рекорд: *{scores[str(user_id)]}* кликов\n"
                "Еще разок? /start",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            print(f"Ошибка обработки данных из Web App: {e}")

# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())