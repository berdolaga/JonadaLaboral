# ports/horario_ports.py

from adapters.horarios_adapter import HorarioAdapter as Adaptador
from objects.horarios import Horario as Elemento

class HorarioPort:

    def __init__(self, adapter: Adaptador):
        self.adapter = adapter

    def create(self, nombre, inicio=None, fin=None, horas_dia=0):
        #print('vamos a crear el elemento con los valores por defecto')
        objectDB = Elemento(None, nombre, inicio, fin, horas_dia)
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
        
    def get_all(self):
        print('todos los horarios')
        return self.adapter.find_all()
     
    ############## modificacion de cada campo del registro ############################ 

    def cambiar(self,id,campo,dato):
        return self.adapter.modificar(id,campo,dato)

    def cambiar_nombre(self, id, nombre):
        return self.adapter.modificar(id,'nombre',nombre)
    
    def cambiar_inicio(self, id, inicio):
        return self.adapter.modificar(id,'inicio',inicio)
    
    def cambiar_fin(self, id, fin):
        return self.adapter.modificar(id,'fin',fin)

    def cambiar_horas_dia(self, id, horas_dia):
        return self.adapter.modificar(id,'horas_dia',horas_dia)