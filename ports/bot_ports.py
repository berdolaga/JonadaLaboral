# ports/bot_ports.py
 
from abc import ABC, abstractmethod

class BotPuerto(ABC):
    @abstractmethod
    def enviar_teclado(self, chat_id, teclado, texto = None):
        pass

    @abstractmethod
    def enviar_teclado(self, chat_id, teclado):
        pass

    @abstractmethod
    def enviar_eteclado(self, chat_id, teclado,columnas):
        pass

    @abstractmethod
    def enviar_texto(self, chat_id, texto):
        pass

    @abstractmethod
    def eliminar_etecado(self, chat_id, message_id):
        pass
