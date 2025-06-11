# objects/fichajes.py

# Proyecto desarrollado como parte del Trabajo de Fin de Grado (TFG)
# Curso de Adaptación al Grado en Ingeniería Informática - UNIR
# Autor: [Alberto Toledo Escrihuela]
# Año: 2025

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
