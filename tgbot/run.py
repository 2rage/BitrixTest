from app import create_app

if __name__ == '__main__':
    updater = create_app()
    updater.start_polling()
    updater.idle()
