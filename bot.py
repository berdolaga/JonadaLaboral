# bot.py
# Proyecto desarrollado como parte del Trabajo de Fin de Grado (TFG)
# Curso de Adaptación al Grado en Ingeniería Informática - UNIR
# Autor: [Alberto Toledo Escrihuela]
# Año: 2025

from interfaces.telegram_bot import run as telegram_run

if __name__ == "__main__":
    print('Iniciando Sistema', flush=True)
    try:
        telegram_run()
    except:
        None
