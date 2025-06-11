# adapters/fichaje_adapters.py

# Proyecto desarrollado como parte del Trabajo de Fin de Grado (TFG)
# Curso de Adaptación al Grado en Ingeniería Informática - UNIR
# Autor: [Alberto Toledo Escrihuela]
# Año: 2025

from sqlalchemy import desc
from objects.fichajes import Fichaje as Elemento
from db.tables import FichajeDB as ObjeCTDB, db_session

class FichajeAdapter:
    def find_by_id(self, id):
        object_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_fichaje == id).first()
        #print('dentro del adapter con id_user: '+str(user_id))
        return self._map_db_to_domain(object_db) if object_db else None
    
    def find_by_id_user(self, id):
        object_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_usuario == id).all()
        #print('dentro del adapter con id_telegram: '+str(id))
        if object_db:
            return [self._map_db_to_domain(object_dbs) for object_dbs in object_db]
        else:
            return False
    
    def find_by_id_user_fecha(self, id, fecha):
        object_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_usuario == id, ObjeCTDB.fecha == fecha).all()
        #print('dentro del adapter con id_telegram: '+str(id))
        if object_db:
            return [self._map_db_to_domain(object_dbs) for object_dbs in object_db]
        else:
            return False
    
    def find_by_id_user_fecha_penultima(self, id, fecha_actual):
        #object_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_usuario == id, ObjeCTDB.fecha == fecha_actual).all()
        #object_db = db_session.query(db_session.func.max(ObjeCTDB.fecha)).filter(ObjeCTDB.fecha > fecha_actual).scalar()
        try:
            object_db = db_session.query(ObjeCTDB.fecha).filter(ObjeCTDB.fecha < fecha_actual).order_by(desc(ObjeCTDB.fecha)).first()
        except Exception as e:
            print("Error:", e)
            raise
        return object_db
        #print('dentro del adapter con id_telegram: '+str(id))
        if object_db:
            return [self._map_db_to_domain(object_dbs) for object_dbs in object_db]
        else:
            return False
    
    def find_all(self):
        # Filtra los registros donde baja es False
        object_db = db_session.query(ObjeCTDB).all()
        if object_db:
            return [self._map_db_to_domain(object_dbs) for object_dbs in object_db]
        else:
            return False    

    def create(self, objeto):
        print('vamos a crear new_object')
        if not self.find_by_id(objeto.id_fichaje):
            new_object = ObjeCTDB(
                id_fichaje = objeto.id_fichaje, # es autoincrement no se puede asignar valor ya que se asigna por defecto.
                id_usuario = objeto.id_usuario,
                fecha = objeto.fecha,
                hora_entrada =objeto.hora_entrada or '',
                hora_salida = objeto.hora_salida or '',
                pausa = objeto.pausa or 0
            )
            print(f'variable new_object creada: {new_object}')
            db_session.add(new_object)
            try:
                #db_session.merge(new_object)     
                db_session.commit()        
            except Exception as e:
                db_session.rollback() 
                print(f'Error al update: {e}')
                raise
            print('commit hecho')
            #print('aqui')
            #db_session.commit()
            print('create new_object hecho')
            return self._map_db_to_domain(new_object)
        else:
            return False

    def update(self, objeto):
        objeto_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_fichaje == objeto.id_fichaje).first()
        if objeto_db:
            objeto_db.fecha =objeto.fecha
            objeto_db.hora_entrada =objeto.hora_entrada
            objeto_db.hora_salida = objeto.hora_salida
            objeto_db.pausa = objeto.pausa

            db_session.commit()
            return self._map_db_to_domain(objeto_db)
        return None

    def delete(self, id):
        objeto_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_fichaje == id).first()
        if objeto_db:
            db_session.delete(objeto_db)
            db_session.commit()

    def _map_db_to_domain(self, objeto):
        return Elemento(
            id_fichaje=objeto.id_fichaje,
            id_usuario=objeto.id_usuario,
            fecha =objeto.fecha,
            hora_entrada =objeto.hora_entrada,
            hora_salida = objeto.hora_salida,
            pausa = objeto.pausa
        )
    
    def modificar(self, id, atributo, valor):
        '''
        Modifica segun el campo que le llega en atributo por el valor pasado.
        '''
        objeto_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_fichaje == id).first()
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
