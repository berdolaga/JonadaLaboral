# adapters/user_adapters.py

#from ports.user_repositorio import UserRepositorio
from objects.usuarios import User
from db.tables import UserDB, db_session

class UserAdapter:

    def count_users(self):
        users = db_session.query(UserDB).count()
        return users

    def find_by_id(self, user_id):
        user_db = db_session.query(UserDB).filter(UserDB.id_usuario == user_id).first()
        #print('dentro del adapter con id_user: '+str(user_id))
        return self._map_db_to_domain(user_db) if user_db else None
    
    def find_by_id_telegram(self, user_id):
        user_db = db_session.query(UserDB).filter(UserDB.id_telegram == user_id).first()
        #print('dentro del adapter con id_telegram: '+str(user_id))
        return self._map_db_to_domain(user_db) if user_db else None
    
    def find_all(self):
        # Filtra los registros donde baja es False
        user_db = db_session.query(UserDB).all()
        if user_db:
            #user_eva_dbs = eva_db_session.query(UserEvaDB).all()
            for user_telegram_db in user_db:
                print('id_telegram: '+str(user_telegram_db.id_telegram)+' nombre: '+str(user_telegram_db.nombre)+' apellido: '+str(user_telegram_db.apellidos))
            return [self._map_db_to_domain(user_telegram_db) for user_telegram_db in user_db]
        else:
            return False

    def create_user(self, object):
        #print('vamos a crear user')
        if not self.find_by_id(object.id_usuario) and (object.id_telegram is None or not self.find_by_id_telegram(object.id_telegram)):
            new_user = UserDB(
                id_usuario = object.id_usuario, # es autoincrement no se puede asignar valor ya que se asigna por defecto.
                id_telegram = object.id_telegram or None,
                nombre = object.nombre or None,
                apellidos =object.apellidos or None,
                dni = object.dni or None,
                n_ss = object.n_ss or None,
                mail = object.mail or None,
                telefono = object.telefono or None,
                trabajando = object.trabajando or None,
                pausado = object.pausado or None,
                menu = object.menu or None,
                eteclat = object.eteclat or None,
                id_usuario_temp = object.id_usuario_temp or None,
                id_horario_temp = object.id_horario_temp or None,
                administrador = object.administrador or None,
                baja = 0
            )
            #print('variable user creada')
            db_session.add(new_user)
            db_session.commit()
            #print('create user hecho')
            return self._map_db_to_domain(new_user)
        else:
            return False

    def update_user(self, user):
        user_db = db_session.query(UserDB).filter(UserDB.id_usuario == user.id_usuario).first()
        if user_db:
            user_db.id_telegram = user.id_telegram
            user_db.nombre =user.nombre
            user_db.apellidos =user.apellidos
            user_db.dni = user.dni
            user_db.n_ss = user.n_ss
            user_db.mail = user.mail
            user_db.telefono = user.telefono
            user_db.trabajando = user.trabajando
            user_db.pausado = user.pausado
            user_db.menu = user.menu
            user_db.eteclat = user.eteclat
            user_db.id_usuario_temp = user.id_usuario_temp
            user_db.id_horario_temp = user.id_horario_temp
            user_db.administrador = user.administrador
            user_db.baja = user.baja

            db_session.commit()
            return self._map_db_to_domain(user_db)
        return None

    def delete_user(self, user_id):
        user_db = db_session.query(UserDB).filter(UserDB.id_usuario == user_id).first()
        if user_db:
            db_session.delete(user_db)
            db_session.commit()

    def _map_db_to_domain(self, user_db):
        return User(
            id_usuario=user_db.id_usuario,
            id_telegram=user_db.id_telegram,
            nombre =user_db.nombre,
            apellidos =user_db.apellidos,
            dni = user_db.dni,
            n_ss = user_db.n_ss,
            mail = user_db.mail,
            telefono = user_db.telefono,
            trabajando = user_db.trabajando,
            pausado = user_db.pausado,
            menu=user_db.menu,
            eteclat=user_db.eteclat,
            id_usuario_temp=user_db.id_usuario_temp,
            id_horario_temp=user_db.id_horario_temp,
            administrador = user_db.administrador,
            baja = user_db.baja
        )
    
    def modificar(self, user_id, atributo, valor):
        '''
        Modifica segun el campo que le llega en atributo por el valor pasado.
        '''
        user_db = db_session.query(UserDB).filter(UserDB.id_usuario == user_id).first()
        if user_db:
            if hasattr(user_db, atributo):
                setattr(user_db, atributo, valor)
                db_session.commit()
                print(f'se ha modificado del usuario la variable {atributo} por el valor: {valor}')
                return self._map_db_to_domain(user_db)
            else:
                print(f"Atributo {atributo} no encontrado en UserDB")
        else:
            print(f'No hay usuario con el user_id: {user_id}')
        return None
