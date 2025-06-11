# adapters/empresa_adapters.py

# Proyecto desarrollado como parte del Trabajo de Fin de Grado (TFG)
# Curso de Adaptación al Grado en Ingeniería Informática - UNIR
# Autor: [Alberto Toledo Escrihuela]
# Año: 2025

from objects.empresa import Empresa as Elemento
from db.tables import EmpresaDB as ObjeCTDB, db_session

class EmpresaAdapter:
    def find_by_id(self, id):
        object_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_empresa == id).first()
        #print('dentro del adapter con id_user: '+str(user_id))
        return self._map_db_to_domain(object_db) if object_db else None
    
    def find_all(self):
        # Filtra los registros donde baja es False
        object_db = db_session.query(ObjeCTDB).all()
        if object_db:
            return [self._map_db_to_domain(object_dbs) for object_dbs in object_db]
        else:
            return False

    def create(self, objeto):
        #print('vamos a crear new_object')
        if not self.find_by_id(objeto.id_empresa):
            new_object = ObjeCTDB(
                id_empresa = objeto.id_empresa, # es autoincrement no se puede asignar valor ya que se asigna por defecto.
                nombre = objeto.nombre,
                direccion =objeto.direccion or None,
                localidad = objeto.localidad or None,
                provincia = objeto.provincia or None,
                mail = objeto.mail or None,
                CIF = objeto.CIF or None,
                CP = objeto.CP or None
            )
            #print('variable new_object creada')
            db_session.add(new_object)
            db_session.commit()
            #print('create new_object hecho')
            return self._map_db_to_domain(new_object)
        else:
            return False

    def update(self, objeto):
        objeto_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_empresa == objeto.id_empresa).first()
        if objeto_db:
            objeto_db.nombre =objeto.nombre
            objeto_db.direccion =objeto.direccion
            objeto_db.localidad = objeto.localidad
            objeto_db.provincia = objeto.provincia
            objeto_db.mail = objeto.mail
            objeto_db.CIF = objeto.CIF
            objeto_db.CP = objeto.CP

            db_session.commit()
            return self._map_db_to_domain(objeto_db)
        return None

    def delete(self, id):
        objeto_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_empresa == id).first()
        if objeto_db:
            db_session.delete(objeto_db)
            db_session.commit()

    def _map_db_to_domain(self, objeto):
        return Elemento(
            id_empresa=objeto.id_empresa,
            nombre =objeto.nombre,
            direccion =objeto.direccion,
            localidad = objeto.localidad,
            provincia = objeto.provincia,
            mail = objeto.mail,
            CIF = objeto.CIF,
            CP = objeto.CP
        )
    
    def modificar(self, id, atributo, valor):
        '''
        Modifica segun el campo que le llega en atributo por el valor pasado.
        '''
        objeto_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_empresa == id).first()
        if objeto_db:
            if hasattr(objeto_db, atributo):
                setattr(objeto_db, atributo, valor)
                db_session.commit()
                print(f'se ha modificado del objeto la variable {atributo} por el valor: {valor}')
                return self._map_db_to_domain(objeto_db)
            else:
                print(f"Atributo {atributo} no encontrado en la BD")
        else:
            print(f'No hay elemento con el id: {id}')
        return None
