# objects/empresa.py

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