# ports/teclado_ports.py

from adapters.teclado_adapter import TecladoAdapter as Adaptador

class TecladoPort:
    def __init__(self, adapter: Adaptador):
        self.adapter = adapter

    def inicio(self, admin, trabajador, entra = None, pausa = None, texto = None):
        if trabajador:
            print('se llama a inicioE')
            tecla = self.adapter.inicioE(admin, entra, pausa, texto)
            print('hora')
            return tecla
        else:
            print('se llama a inicio')
            return self.adapter.inicio(admin)
            

    def xinicio(self):
        return self.adapter.xinicio()
    
    def volver(self,texto):
        return self.adapter.volver(texto)
    
    def sino(self,texto):
        return self.adapter.si_no(texto)

    def empresa(self,empresa= None):
        return self.adapter.empresa(empresa)

    def configuracion(self):
        return self.adapter.configuracion()

    def config_usuarios(self):
        return self.adapter.config_usuarios()
    
    def config_usuario_seleccionado(self,usuario,telefono,apellido,administrador,dni, nss, mail, baja):
        return self.adapter.config_usuario_seleccionado(usuario,telefono,apellido,administrador,dni, nss, mail, baja)

    def add_usuario(self):
        return self.adapter.add_usuario()
    
    def listados(self, textos):
        return self.adapter.listados(textos)
    
    def e_listado_listados(self):
        return self.adapter.e_listado_listados()
    
    def e_listado_usuarios_telegram(self,usuario_telegram):
        return self.adapter.e_listado_usuarios_telegram(usuario_telegram)
    
    def horario(self,texto):
        return self.adapter.horario(texto)
    
    def e_horario(self,horarios):
        return self.adapter.e_horario(horarios)
    
    def editar_horario(self,frase):
        return self.adapter.editar_horario(frase)
    
    
