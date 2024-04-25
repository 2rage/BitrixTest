from telegram.ext import CommandHandler, MessageHandler, Filters
from .handlers import start, handle_message, handle_form

def setup_routes(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command & Filters.regex(r"^[^,]+, [^,]+, [^,]+$"), handle_form))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
