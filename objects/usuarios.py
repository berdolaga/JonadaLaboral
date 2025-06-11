# objects/usuarios.py

# Proyecto desarrollado como parte del Trabajo de Fin de Grado (TFG)
# Curso de Adaptación al Grado en Ingeniería Informática - UNIR
# Autor: [Alberto Toledo Escrihuela]
# Año: 2025

class User:
    def __init__(self,
    id_usuario,
    id_telegram,
    nombre,
    apellidos,
    dni,
    n_ss,
    mail,
    telefono,
    trabajando,
    pausado,
    menu,
    eteclat,
    id_usuario_temp,
    id_horario_temp,
    administrador,
    baja):
        self.id_usuario = id_usuario
        self.id_telegram = id_telegram
        self.nombre = nombre
        self.apellidos = apellidos
        self.dni = dni
        self.n_ss = n_ss
        self.mail = mail
        self.telefono = telefono
        self.trabajando = trabajando
        self.pausado = pausado
        self.menu = menu
        self.eteclat = eteclat
        self.id_usuario_temp = id_usuario_temp
        self.id_horario_temp = id_horario_temp
        self.administrador = administrador
        self.baja = baja
