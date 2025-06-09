# ports/fichaje_ports.py

from adapters.fichaje_adapter import FichajeAdapter as Adaptador
from objects.fichajes import Fichaje as Elemento

class FichajePort:

    def __init__(self, adapter: Adaptador):
        self.adapter = adapter

    def create(self, id_usuario, fecha, hora_entrada, hora_salida, pausa = 0):
        #print('vamos a crear el elemento con los valores por defecto')
        objectDB = Elemento(None,id_usuario, fecha, hora_entrada, hora_salida, pausa)
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
    
    def get_by_id_user_fecha(self, id, fecha):
        print('id del usuario: '+str(id))
        return self.adapter.find_by_id_user_fecha(id, fecha)
        
    def get_by_id_user_fecha_penultima(self, id, fecha):
        print('id del usuario: '+str(id))
        return self.adapter.find_by_id_user_fecha_penultima(id, fecha)
     
    ############## modificacion de cada campo del registro ############################ 

    def cambiar(self,id,campo,dato):
        return self.adapter.modificar(id,campo,dato)

    def cambiar_fecha(self, id, fecha):
        return self.adapter.modificar(id,'fecha',fecha)
    
    def cambiar_hora_entrada(self, id, hora_entrada):
        return self.adapter.modificar(id,'hora_entrada',hora_entrada)
    
    def cambiar_hora_salida(self, id, hora_salida):
        return self.adapter.modificar(id,'hora_salida',hora_salida)
    
    def cambiar_pausa(self, id, pausa):
        return self.adapter.modificar(id,'pausa',pausa)