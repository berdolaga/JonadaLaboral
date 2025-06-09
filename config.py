# config.py

import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    # Configuración del bot de Telegram
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_API_TOKEN', 'YOUR_DEFAULT_API_TOKEN')
    
    # Configuración de la base de datos sqlite
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')

    print('Configuración sistema cargada')

config = Config()
