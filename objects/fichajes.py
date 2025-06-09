# objects/fichajes.py

class Fichaje:
    def __init__(self,
    id_fichaje,
    id_usuario,
    fecha,
    hora_entrada,
    hora_salida,
    pausa):        
        self.id_fichaje = id_fichaje
        self.id_usuario = id_usuario
        self.fecha = fecha
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida
        self.pausa = pausa