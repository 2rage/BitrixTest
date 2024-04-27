from app import create_app

def main():
    updater = create_app()
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
