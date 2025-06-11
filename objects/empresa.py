# objects/empresa.py

# Proyecto desarrollado como parte del Trabajo de Fin de Grado (TFG)
# Curso de Adaptación al Grado en Ingeniería Informática - UNIR
# Autor: [Alberto Toledo Escrihuela]
# Año: 2025

class Empresa:
    def __init__(self,
    id_empresa,
    nombre,
    direccion,
    localidad,
    provincia,
    mail,
    CIF,
    CP):
        self.id_empresa = id_empresa
        self.nombre = nombre
        self.direccion = direccion
        self.localidad = localidad
        self.provincia = provincia
        self.mail = mail
        self.CIF = CIF
        self.CP = CP
