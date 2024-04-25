from telegram.ext import Updater
from .routes import setup_routes
from .config import TELEGRAM_TOKEN

def create_app():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    setup_routes(updater.dispatcher)
    return updater
