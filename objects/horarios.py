# objects/horarios.py

# Proyecto desarrollado como parte del Trabajo de Fin de Grado (TFG)
# Curso de Adaptación al Grado en Ingeniería Informática - UNIR
# Autor: [Alberto Toledo Escrihuela]
# Año: 2025

class Horario:
    def __init__(self,
    id_horario,
    nombre,
    inicio,
    fin,
    horas_dia):        
        self.id_horario = id_horario
        self.nombre = nombre
        self.inicio = inicio
        self.fin = fin
        self.horas_dia = horas_dia
