import os
from dotenv import load_dotenv
load_dotenv()


# Конфигурация Telegram
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
