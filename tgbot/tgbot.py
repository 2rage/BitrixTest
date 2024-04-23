from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

TOKEN = 'REMOVED'
BITRIX_WEBHOOK = 'REMOVED'
BITRIX_WEBOOK2 = 'https://b24-355fx6.bitrix24.ru/rest/1/45l37h83ivtpiqsl/'

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Здравствуйте, напишите ваш вопрос")

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    response = requests.post(f"{BITRIX_WEBHOOK}/crm.lead.add", json={'fields': {'TITLE': 'Новый запрос', 'COMMENTS': text}})
    lead_id = response.json()['result']
    update.message.reply_text("Пожалуйста, укажите ваше ФИО, телефон и почту. Ответ отправьте в формате: ФИО, Телефон, Почта.")

def handle_form(update: Update, context: CallbackContext):
    user_data = update.message.text.split(", ")
    if len(user_data) == 3:
        fio, phone, email = user_data
        lead_id = context.user_data['current_lead_id'] 
        requests.post(f"{BITRIX_WEBOOK2}/crm.lead.update", json={
            'id': lead_id,
            'fields': {'NAME': fio, 'PHONE': [{'VALUE': phone}], 'EMAIL': [{'VALUE': email}], 'STATUS_ID': '2'}
        })
        update.message.reply_text(f"{fio} спасибо, мы получили ваши данные, менеджер вам скоро напишет.")

        requests.post(f"{BITRIX_WEBHOOK}/tasks.task.add", json={
            'fields': {
                'TITLE': 'Новый клиент для связи',
                'DESCRIPTION': f'Свяжитесь с клиентом {fio}. Телефон: {phone}, Email: {email}',
                'RESPONSIBLE_ID': 1  # ID ответственного сотрудника
            }
        })

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command & Filters.regex(r"^[^,]+, [^,]+, [^,]+$"), handle_form))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()