# ports/empresa_ports.py

from adapters.empresa_adapter import EmpresaAdapter as Adaptador
from objects.empresa import Empresa as Elemento

class EmpresaPort:

    def __init__(self, adapter: Adaptador):
        self.adapter = adapter

    def create(self, nombre, direccion=None, localidad=None, provincia=None, mail=None, CIF=None, CP=None):
        #print('vamos a crear el elemento con los valores por defecto')
        objectDB = Elemento(None, nombre, direccion, localidad, provincia, mail, CIF, CP)
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
     
    ############## modificacion de cada campo del registro ############################ 

    def cambiar(self,id,campo,dato):
        return self.adapter.modificar(id,campo,dato)

    def cambiar_nombre(self, id, nombre):
        return self.adapter.modificar(id,'nombre',nombre)
    
    def cambiar_direccion(self, id, direccion):
        return self.adapter.modificar(id,'direccion',direccion)
    
    def cambiar_localidad(self, id, localidad):
        return self.adapter.modificar(id,'localidad',localidad)

    def cambiar_provincia(self, id, provincia):
        return self.adapter.modificar(id,'provincia',provincia)

    def cambiar_mail(self, id, mail):
        return self.adapter.modificar(id,'mail',mail)

    def cambiar_CIF(self, id, CIF):
        return self.adapter.modificar(id,'CIF',CIF)

    def cambiar_CP(self, id, CP):
        return self.adapter.modificar(id,'CP',CP)