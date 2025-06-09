# adapters/telegram_bot_adapters.py

from telebot import types
from ports.bot_ports import BotPuerto

class TelegramBotAdaptador(BotPuerto):
    def __init__(self, bot):
        self.bot = bot
        
    def enviar_teclado(self, chat_id, teclado, texto = None):
        markup = types.ReplyKeyboardMarkup()#row_width=2)
        for fila in teclado.botones:
            botones = [types.KeyboardButton(boton) for boton in fila]
            markup.add(*botones)
        self.bot.send_message(chat_id, teclado.texto, reply_markup=markup)

    def enviar_eteclado(self, chat_id, teclado, columnas):
        markup = types.InlineKeyboardMarkup(row_width=columnas)
        for fila in teclado.botones:
            botones = [types.InlineKeyboardButton(text=boton[0], callback_data=boton[1]) for boton in fila]
            markup.add(*botones)
        print('dentro del eteclado el texto es: '+str(teclado.texto))
        message = self.bot.send_message(chat_id, teclado.texto, reply_markup=markup)
        
        if message:
            return message
        else:
            print('no ha devuelto message el bot')
            # Actualizar el campo eteclat en la base de datos
            self.actualizar_eteclat(chat_id, message.message_id)
    
    def enviar_texto(self, chat_id, texto):
        limite = 4096# limite de caracteres por mensaje
        mensajes = [texto[i:i + limite] for i in range(0, len(texto), limite)]

        for mensaje in mensajes:
            try:
                self.bot.send_message(chat_id, mensaje)
                print("Texto enviado a Telegram con el contenido: " + mensaje)
            except Exception as e:
                print("Fallo al enviar el texto: " + mensaje)
                print("Error:", e)

    def enviar_archivo(self,chat_id,documento):
        try:
            #doc = open(documento,'rb')
            self.bot.send_document(chat_id, documento)
        except Exception as e:
            print(f'Error al enviar el documento: {e}')

    def eliminar_etecado(self, chat_id, message_id):
        try:
            self.bot.delete_message(chat_id, message_id)
        except Exception as e:
            print(f'Error al eliminar el emensaje {message_id}: {e}')

    def enviar_accion(self, chat_id, accion):
        self.bot.send_chat_action(chat_id, accion) #'typing' 'upload_photo' 'upload_video' upload_document find_location record_video record_audio record_video_note upload_video_note

    