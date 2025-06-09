# adapters/usuario_horario_adapters.py

#from ports.user_repositorio import UserRepositorio
from objects.usuario_horarios import UsuarioHorario as Elemento
from db.tables import Usuario_HorarioDB as ObjeCTDB, db_session


class UsuarioHorarioAdapter:
    def find_by_id(self, id):
        object_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_usuario_horario == id).first()
        #print('dentro del adapter con id_user: '+str(user_id))
        return self._map_db_to_domain(object_db) if object_db else None
    
    def find_by_id_user(self, id):
        object_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_usuario == id).first()
        #print('dentro del adapter con id_telegram: '+str(id))
        return self._map_db_to_domain(object_db) if object_db else None
    
    def find_by_id_horario(self, id):
        object_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_horario == id).first()
        #print('dentro del adapter con id_telegram: '+str(id))
        return self._map_db_to_domain(object_db) if object_db else None
    
    def find_by_id_user_and_id_horario(self, user_id, id):
        object_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_usuario == user_id, ObjeCTDB.id_horario == id).first()
        #print('dentro del adapter con id_telegram: '+str(id))
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
        if not self.find_by_id(objeto.id_usuario_horario):
            new_object = ObjeCTDB(
                id_usuario_horario = objeto.id_usuario_horario, # es autoincrement no se puede asignar valor ya que se asigna por defecto.
                id_usuario = objeto.id_usuario,
                id_horario =objeto.id_horario
            )
            #print('variable new_object creada')
            db_session.add(new_object)
            db_session.commit()
            #print('create new_object hecho')
            return self._map_db_to_domain(new_object)
        else:
            return False

    def update(self, objeto):
        objeto_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_usuario_horario == objeto.id_usuario_horario).first()
        if objeto_db:
            objeto_db.id_usuario =objeto.id_usuario
            objeto_db.id_horario =objeto.id_horario

            db_session.commit()
            return self._map_db_to_domain(objeto_db)
        return None

    def delete(self, id):
        objeto_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_usuario_horario == id).first()
        if objeto_db:
            db_session.delete(objeto_db)
            db_session.commit()

    def _map_db_to_domain(self, objeto):
        return Elemento(
            id_usuario_horario=objeto.id_usuario_horario,
            id_usuario =objeto.id_usuario,
            id_horario =objeto.id_horario
        )
    
    def modificar(self, id, atributo, valor):
        '''
        Modifica segun el campo que le llega en atributo por el valor pasado.
        '''
        objeto_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_usuario_horario == id).first()
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