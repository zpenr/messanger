import os
from app import create_app
from dotenv import load_dotenv

# Загружаем .env только если файл существует
if os.path.exists('.env'):
    load_dotenv('.env')

application = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port)