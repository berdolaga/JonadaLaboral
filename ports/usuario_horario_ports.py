# ports/usuario_horario_ports.py

from adapters.usuario_horario_adapter import UsuarioHorarioAdapter as Adaptador
from objects.usuario_horarios import UsuarioHorario as Elemento

class UsuarioHorarioPort:

    def __init__(self, adapter: Adaptador):
        self.adapter = adapter

    def create(self, id_usuario, id_horario):
        #print('vamos a crear el elemento con los valores por defecto')
        objectDB = Elemento(None, id_usuario, id_horario)
        #print(objectDB)
        created_object = self.adapter.create(objectDB)
        #print('ports creado objectDB')
        return created_object

    def modificar(self, object):
        return self.adapter.update(object)
    
    def eliminar(self, id):
        elemento = self.adapter.find_by_id(id)
        if elemento:
            return self.adapter.delete(id)
    
    def get_by_id(self, id):
        print('id del elemento: '+str(id))
        return self.adapter.find_by_id(id)
    
    def get_by_id_user(self, id):
        print('id del usuario: '+str(id))
        return self.adapter.find_by_id_user(id)
    
    def get_by_id_horario(self, id):
        print('id del usuario: '+str(id))
        return self.adapter.find_by_id_horario(id)
    
    def get_by_id_user_id_horario(self, user_id, id):
        print('id del usuario: '+str(id))
        return self.adapter.find_by_id_user_and_id_horario(user_id,id)
     
    ############## modificacion de cada campo del registro ############################ 

    def cambiar(self,id,campo,dato):
        return self.adapter.modificar(id,campo,dato)

    def cambiar_id_usuario(self, id, id_usuario):
        return self.adapter.modificar(id,'id_usuario',id_usuario)
    
    def cambiar_id_horario(self, id, id_horario):
        return self.adapter.modificar(id,'id_horario',id_horario)