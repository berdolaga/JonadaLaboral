# ports/bot_ports.py

# Proyecto desarrollado como parte del Trabajo de Fin de Grado (TFG)
# Curso de Adaptación al Grado en Ingeniería Informática - UNIR
# Autor: [Alberto Toledo Escrihuela]
# Año: 2025
 
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
