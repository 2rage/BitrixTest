from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

TOKEN = 'REMOVED'
BITRIX_WEBHOOK = 'REMOVED'
BITRIX_WEBOOK2 = 'REMOVED'
#REMOVEDcrm.lead.fields.json


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Здравствуйте, напишите ваш вопрос")

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    response = requests.post(f"{BITRIX_WEBHOOK}/crm.lead.add", json={'fields': {'TITLE': 'Новый лид из Telegram', 'COMMENTS': text}})
    lead_id = response.json()['result']
    context.user_data['current_lead_id'] = lead_id 
    update.message.reply_text("Пожалуйста, укажите ваше ФИО, телефон и почту. Ответ отправьте в формате: ФИО, Телефон, Почта.")


def handle_form(update: Update, context: CallbackContext):
    user_data = update.message.text.split(", ")
    if len(user_data) == 3:
        fio, phone, email = user_data
        lead_id = context.user_data.get('current_lead_id')
        if lead_id:

            names = fio.split()
            first_name = names[0] if len(names) > 0 else ''
            last_name = names[1] if len(names) > 1 else ''
            second_name = names[2] if len(names) > 2 else ''
            
            lead_update_response = requests.post(f"{BITRIX_WEBOOK2}/crm.lead.update", json={
                'id': lead_id,
                'fields': {
                    'LAST_NAME': last_name,
                    'NAME': first_name,
                    'SECOND_NAME': second_name,
                    'PHONE': [{'VALUE': phone, 'VALUE_TYPE': 'WORK'}],
                    'EMAIL': [{'VALUE': email, 'VALUE_TYPE': 'WORK'}],
                    'STATUS_ID': '2'
                }
            })
            if lead_update_response.status_code == 200:
                update.message.reply_text(f"{fio} спасибо, мы получили ваши данные, менеджер вам скоро напишет.")

                requests.post(f"{BITRIX_WEBOOK2}/tasks.task.add", json={
                    'fields': {
                        'TITLE': 'Новый клиент для связи',
                        'DESCRIPTION': f'Свяжитесь с клиентом {fio}. Телефон: {phone}, Email: {email}',
                        'RESPONSIBLE_ID': 1  # ID ответственного сотрудника
                    }
                })
            else:
                update.message.reply_text("Не удалось обновить данные лида. Пожалуйста, попробуйте еще раз.")
        else:
            update.message.reply_text("Произошла ошибка при обработке вашего запроса, пожалуйста, начните заново.")


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
