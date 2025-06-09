# bot.py

from interfaces.telegram_bot import run as telegram_run

if __name__ == "__main__":
    print('Iniciando Sistema', flush=True)
    try:
        telegram_run()
    except:
        None
