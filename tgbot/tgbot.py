from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

TOKEN = 'REMOVED'
BITRIX_WEBHOOK_URL = 'REMOVED'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Здравствуйте, напишите ваш вопрос')

def message_handler(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    response = requests.post(f"{BITRIX_WEBHOOK_URL}/crm.lead.add", json={
        "fields": {
            "TITLE": "Новый лид из Telegram",
            "COMMENTS": text
        }
    })
    lead_id = response.json()["result"]
    update.message.reply_text('Пожалуйста, заполните форму.', reply_markup=ForceReply(selective=True))

def form_handler(update: Update, context: CallbackContext) -> None:
    phone = update.message.text
    # Аналогично обрабатываем другие поля и отправляем их в Bitrix24
    update.message.reply_text('[ФИО] спасибо, мы получили ваши данные, менеджер вам скоро напишет')

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))
    dispatcher.add_handler(MessageHandler(Filters.reply, form_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()