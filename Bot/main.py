from bot.telegram_bot import TelegramBot
import os

token = os.getenv("TOKEN")
bot = TelegramBot(token)
bot.start()