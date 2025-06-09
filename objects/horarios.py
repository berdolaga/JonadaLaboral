# objects/horarios.py

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