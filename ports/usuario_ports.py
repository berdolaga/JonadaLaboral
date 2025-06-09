# ports/user_ports.py

from adapters.user_adapter import UserAdapter as Adaptador
from objects.usuarios import User as Elemento

class UserPort:
    ## User ##
    def __init__(self, adapter: Adaptador):
        self.adapter = adapter

    def create_user(self, id_telegram, nombre, apelllidos, menu, telefono, eteclat, id_usuario_temp, administrador):
        print('vamos a crear el user con los valores por defecto')
        dni = None
        n_ss = None
        mail = None
        trabajando = None
        pausado = None
        baja = 0
        user = Elemento(None,id_telegram, nombre, apelllidos, dni, n_ss, mail, telefono, trabajando, pausado, menu, eteclat, id_usuario_temp, administrador, baja)
        #print(user)
        created_user = self.adapter.create_user(user)
        #print('ports creado user')
        return created_user

    def modificar(self, user):
        return self.adapter.update_user(user)
    
    def eliminar_usuario(self, user_id):
        usuario = self.adapter.find_by_id(user_id)
        if usuario:# eliminar todos los registros en la bd.
            #self.user_telegram_repositorio.delete_user_telegram(usuario.id_telegram)
            return self.adapter.delete_user(user_id)
        
    def get_all_users(self):
        print('id de usuario: ')
        return self.adapter.find_all()

    def get_user_by_id(self, user_id):
        print('id de usuario: '+str(user_id))
        return self.adapter.find_by_id(user_id)
    
    def get_user_by_id_telegram(self, user_id):
        print('id de usuario telegram: '+str(user_id))
        return self.adapter.find_by_id_telegram(user_id)
        
    def usuarios(self):
        return self.adapter.count_users()
    
    def cambiar_menu(self, user_id, menu):
        usuario = self.adapter.find_by_id_telegram(user_id)
        #return self.adapter.mod_menu(user_id, menu)
        #print(f'usuario id: {usuario.id_user}')
        return self.adapter.modificar(usuario.id_usuario,'menu',menu)
    
    ############## modificacion de cada campo del registro ############################
    
    def cambiar_usuario(self, user_id, id_usuario):
        #return self.adapter.mod_usuario(user_id, id_usuario)
        return self.adapter.modificar(user_id,'id_usuario_temp',id_usuario)
    
    def cambiar_horario_temp(self, user_id, id_horario):
        return self.adapter.modificar(user_id,'id_horario_temp',id_horario)
    
    def cambiar_nombre(self, user_id, nombre):
        return self.adapter.modificar(user_id,'nombre',nombre)
    
    def cambiar_apellidos(self, user_id, apellidos):
        return self.adapter.modificar(user_id,'apellidos',apellidos)
    
    def cambiar_dni(self, user_id, dni):
        return self.adapter.modificar(user_id,'dni',dni)
    
    def cambiar_n_ss(self, user_id, n_ss):
        return self.adapter.modificar(user_id,'n_ss',n_ss)
    
    def cambiar_mail(self, user_id, mail):
        return self.adapter.modificar(user_id,'mail',mail)
    
    def cambiar_telefono(self, user_id, telefono):
        return self.adapter.modificar(user_id,'telefono',telefono)
    
    def cambiar_trabajando(self, user_id, trabajando):
        return self.adapter.modificar(user_id,'trabajando',trabajando)
    
    def cambiar_pausado(self, user_id, pausado):
        return self.adapter.modificar(user_id,'pausado',pausado)
    
    def cambiar_eteclat(self, user_id, eteclat):
        return self.adapter.modificar(user_id,'eteclat',eteclat)
    
    def cambiar_administrador(self, user_id, administrador):
        return self.adapter.modificar(user_id,'administrador',administrador)
    
    def cambiar_baja(self, user_id, baja):
        return self.adapter.modificar(user_id,'baja',baja)
    