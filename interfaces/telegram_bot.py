# interfaces/telegram_bot.py

# Proyecto desarrollado como parte del Trabajo de Fin de Grado (TFG)
# Curso de Adaptación al Grado en Ingeniería Informática - UNIR
# Autor: [Alberto Toledo Escrihuela]
# Año: 2025

import telebot
import time
import threading
from config import config
from adapters.telegram_bot_adapter import TelegramBotAdaptador
from application.manejador_mensajes import ManejadorMensajes

# Inicializa el bot con el token de configuración
bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

# Variables globales del bot
bot_adaptador = TelegramBotAdaptador(bot)
manejador_mensajes = ManejadorMensajes(bot_adaptador)

# variables para el bot
running = True
    
def inicio(message):
    bot.reply_to(message, "menu inicio.")


@bot.callback_query_handler(func=lambda call: True)
def listener_inline(call):
    manejador_mensajes.manejar_mensaje_inline(call)

def listener(messages):
    for message in messages:
        manejador_mensajes.manejar_mensaje(message)

bot.set_update_listener(listener) # Asi, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada en la función anterior.

# Función que ejecuta bot.polling() en un hilo separado
def polling_thread():
    while True:  # Bucle para reiniciar automáticamente
        try:
            print("Iniciando Bot Telegram...")
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Error inesperado en polling del bot de Telegram: {e}. Reiniciando en 5 segundos...")
            time.sleep(5)
            raise

# Ejecuta el bot
def run():
    #running = True
    global running
    bot_thread = threading.Thread(target=polling_thread, daemon=True)
    try:
        bot_thread.start()  # Inicia bot.polling() en un hilo separado
    except:
        print('Error en el incio del bot de Telegram')
    print("Bot Telegram Iniciado")
    print('.')
    print('..')
    print('...')
    try:
        while running:  # Mantén el programa principal activo
            if running:
                time.sleep(2)  # Evita que consuma demasiada CPU
            else:
                break
    except KeyboardInterrupt:
        print("\nDeteniendo Bot Telegram...")
        running = False
        bot.stop_polling()  # Detiene el bucle interno de polling
        print("Bot Telegram detenido correctamente.")
        raise

if __name__ == "__main__":
    run()
