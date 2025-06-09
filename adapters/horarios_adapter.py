# adapters/horarios_adapters.py

#from ports.user_repositorio import UserRepositorio
from objects.horarios import Horario as Elemento
from db.tables import HorarioDB as ObjeCTDB, db_session

class HorarioAdapter:
    def find_by_id(self, id):
        object_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_horario == id).first()
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
        if not self.find_by_id(objeto.id_horario):
            new_object = ObjeCTDB(
                id_horario = objeto.id_horario, # es autoincrement no se puede asignar valor ya que se asigna por defecto.
                nombre = objeto.nombre,
                inicio =objeto.inicio or None,
                fin = objeto.fin or None,
                horas_dia = objeto.horas_dia or None
            )
            #print('variable new_object creada')
            db_session.add(new_object)
            db_session.commit()
            #print('create new_object hecho')
            return self._map_db_to_domain(new_object)
        else:
            return False

    def update(self, objeto):
        objeto_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_horario == objeto.id_horario).first()
        if objeto_db:
            objeto_db.nombre =objeto.nombre
            objeto_db.inicio =objeto.inicio
            objeto_db.fin = objeto.fin
            objeto_db.horas_dia = objeto.horas_dia

            db_session.commit()
            return self._map_db_to_domain(objeto_db)
        return None

    def delete(self, id):
        objeto_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_horario == id).first()
        if objeto_db:
            db_session.delete(objeto_db)
            db_session.commit()

    def _map_db_to_domain(self, objeto):
        return Elemento(
            id_horario=objeto.id_horario,
            nombre =objeto.nombre,
            inicio =objeto.inicio,
            fin = objeto.fin,
            horas_dia = objeto.horas_dia
        )
    
    def modificar(self, id, atributo, valor):
        '''
        Modifica segun el campo que le llega en atributo por el valor pasado.
        '''
        objeto_db = db_session.query(ObjeCTDB).filter(ObjeCTDB.id_horario == id).first()
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
