# application/manejador_mensajes.py


from application.menus_telegram import MenuTelegram
from application.funciones_telegram import FuncionTelegram
from application.user_servicios_inicializar import user_port


class ManejadorMensajes:
    #def __init__(self, teclado_servicio, bot_adaptador):
    def __init__(self, bot_adaptador):
        #self.teclado_servicio = teclado_servicio
        self.bot_adaptador = bot_adaptador
        self.menus = MenuTelegram()
        self.funcion_telegram = FuncionTelegram()

    def quinMenu(self,user_id):
        user = user_port.get_user_by_id_telegram(str(user_id))
        if user:
            if user.menu:
                return user.menu
            else:
                user_port.cambiar_menu(user_id,'inicio')
                return 'inicio' 
        else:
            return False

    def enviar_mensaje(self,teclado, chat_id, textos = None):
        if teclado:
            if teclado == 1:
                self.bot_adaptador.enviar_texto(chat_id,u"\U0001f6ab"+" Parámetro no válido "+u"\U0001f6ab")
            elif teclado == 2:
                None
            else: 
                print('botones: '+str(teclado.botones))
                print('texto: '+str(teclado.texto))
                if textos:
                    teclado.texto = textos
                else: 
                    None
                self.bot_adaptador.enviar_teclado(chat_id, teclado)
        else:
            if textos:
                self.bot_adaptador.enviar_texto(chat_id,u"\U0001F6A7"+"  "+textos+"  "+u"\U0001F6A7")
            else:
                self.bot_adaptador.enviar_texto(chat_id,u"\U0001F6A7"+" En Construcción "+u"\U0001F6A7")

    def manejar_mensaje(self, mensaje):
        chat_id = mensaje.chat.id
        if self.funcion_telegram.existe_usuario(chat_id,mensaje):
            print('existe usuario')
            menu = self.quinMenu(chat_id)
            if mensaje.content_type == 'text':
                self.bot_adaptador.enviar_accion(chat_id, 'typing') #'upload_photo' 'upload_video'
                texto = mensaje.text            
                print(menu)
                print(texto)
                if menu:
                    teclado = self.menus.menu(mensaje,menu,chat_id,self.bot_adaptador)
                    self.enviar_mensaje(teclado,chat_id)               
                else:
                    print('No existe el usuario')
            else:
                print (str(mensaje.content_type))
                print ("Recibido: "+str(mensaje.text))
                if mensaje.content_type == "document":
                    print ("Recibido: Procesando Archivo")
                elif mensaje.content_type == "contact":	
                    print ("Recibido: Procesando Contacto")
                    teclado = self.menus.menu_archivo(mensaje,menu,chat_id,self.bot_adaptador)
                    if teclado:
                        tex = 'Usuario Añadido correctamente'
                    else:
                        tex = 'Error al añadir el usuario, vuelva a intentarlo'
                    self.enviar_mensaje(teclado,chat_id,tex)
                elif mensaje.content_type == "location": 
                    print ("Recibida una ubicación: "+str(mensaje.location))
                    self.enviar_mensaje(1,chat_id)
                elif mensaje.content_type == "photo": 
                    print ("Recibida una foto: "+str(mensaje.photo))
                    self.enviar_mensaje(1,chat_id)
                elif mensaje.content_type == "voice":
                    # El mensaje contiene una nota de voz
                    print("Nota de voz recibida")
                    self.enviar_mensaje(1,chat_id)
                else:
                    print("Comando no reconocido.")
        else:
            print(f'No existe el usuario en la bd con el id_telegram {chat_id}')

    def manejar_mensaje_inline(self, call):
        print ("manejador de mensajes  ")        
        chat_id = call.message.chat.id
        menu = self.quinMenu(chat_id)
        self.bot_adaptador.enviar_accion(chat_id, 'typing')  #'upload_photo' 'upload_video'
        
        print ("Estamos en el Menu del teclado inline: "+menu)
        if menu == "Configuración Usuarios": 
            teclado = self.funcion_telegram.seleccionar_usuario_telegram(call,menu,self.bot_adaptador)
            self.enviar_mensaje(teclado,chat_id)
        elif menu == "Listado Empleado": 
            teclado = self.funcion_telegram.elistado_listados(call,self.bot_adaptador,False)
            self.enviar_mensaje(teclado,chat_id)
        elif menu == "Configuración Horario": 
            #self.bot_adaptador.answer_callback_query(call.id,text='Generando pdf')
            teclado = self.funcion_telegram.horario_seleccionado(call, self.bot_adaptador)
            self.enviar_mensaje(teclado,chat_id)
        elif menu == "Configuración Usuario Horario": 
            teclado = self.funcion_telegram.horario_seleccionado_usuario(call, self.bot_adaptador)
            self.enviar_mensaje(teclado,chat_id)
        elif menu == "Configuración Usuario Listados": 
            teclado = self.funcion_telegram.elistado_listados(call, self.bot_adaptador,True)
            self.enviar_mensaje(teclado,chat_id)