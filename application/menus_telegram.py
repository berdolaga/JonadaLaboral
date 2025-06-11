# application/menus_telegram.py

# Proyecto desarrollado como parte del Trabajo de Fin de Grado (TFG)
# Curso de Adaptación al Grado en Ingeniería Informática - UNIR
# Autor: [Alberto Toledo Escrihuela]
# Año: 2025

import sys
#from application import funciones_telegram
from application.user_servicios_inicializar import teclado_port, user_port
from application.funciones_telegram import *
import adapters.diccionarios as diccionarios

class MenuTelegram:
    def __init__(self):
        from application.funciones_telegram import FuncionTelegram
        self.funcionTelegram = FuncionTelegram()
        #self.funciones = application.funciones
        #None
    
    def strToObj(self, astr):  # función que convierte str a valor/nombre función
        print('procesando %s' % astr)
        try:
            # Verifica si el nombre es un atributo del objeto actual
            return getattr(self, astr)
        except AttributeError:
            try:
                # Si no es un atributo del objeto, intenta buscar en el espacio de nombres global
                return globals()[astr]
            except KeyError:
                try:
                    # Si no está en el espacio de nombres global, intenta importar como un módulo
                    __import__(astr)
                    mod = sys.modules[astr]
                    return mod
                except ImportError:
                    module, _, basename = astr.rpartition('.')
                    if module:
                        # Si es un nombre calificado, intenta resolverlo recursivamente
                        mod = self.strToObj(module)
                        return getattr(mod, basename)
                    else:
                        raise

    def menu(self, mensaje, menu, chat_id, bot):
        try:
            return self.strToObj(diccionarios.devuelve('operacion',menu))(mensaje,menu,chat_id,bot)
        except:
            print(f'mensaje enviado por el usuario no valido')
            return 1
        
    def menu_archivo(self, mensaje, menu, chat_id, bot):
        try:
            return self.strToObj(diccionarios.devuelve('operacion',menu))(mensaje,menu,chat_id, bot)
        except:
            print(f'mensaje enviado por el usuario no valido:')
            return 1

    def inicio(self, mensaje, menu, chat_id,bot):
        print("menu inicio")
        texto = mensaje.text
        if texto == u"\U0001f558"+" Fichar":
            teclado = self.funcionTelegram.inicioE(chat_id)
            menu = 'Fichar'
            #user_port.cambiar_menu(chat_id,'Fichar')
        elif texto == u"\u2699\uFE0F"+" Configuración":
            teclado = self.funcionTelegram.configuracion(chat_id)
            if teclado == False or teclado == 2:
                print(menu)
            else:
                menu = 'Configuración'
        else:
            teclado = self.funcionTelegram.inicio(chat_id,menu)
            user_port.cambiar_menu(chat_id,'Inicio')
            return teclado
        #guardar el menu inicio
        user_port.cambiar_menu(chat_id,menu)
        return teclado
    

    def inicioE(self, mensaje, menu, chat_id,bot):
        print("menu inicioE")
        admin = self.funcionTelegram.es_admin(chat_id)
        print(f"obtenido admin: {admin}")
        teclado = self.funcionTelegram.inicioE(chat_id)
        print("teclado hecho para inicioE")
        if admin:
            user_port.cambiar_menu(chat_id,'Inicio')
        else:
            user_port.cambiar_menu(chat_id,'Fichar')
        return teclado

 ################### Fichar ###############################################

    def fichar(self, mensaje, menu, chat_id,bot):
        print("menu inicioE")
        texto = mensaje.text
        if texto == u"\U0001f519"+" Volver":
            usuario_t = user_port.get_user_by_id_telegram(chat_id)
            if usuario_t.administrador:
                menu = 'Inicio'
                teclado = self.funcionTelegram.inicio(chat_id,menu)
                user_port.cambiar_menu(chat_id,menu)
            else:
                print(f'mensaje enviado por el usuario no valido: {texto}')
                return 1
        elif texto == u"\U000027A1"+u"\U0001F6AA"+' ENTRADA':
            teclado = self.funcionTelegram.fichar_entrada(chat_id,1,0)
        elif texto == u"\U00002B05"+u"\U0001F6AA"+' SALIDA':
            teclado = self.funcionTelegram.fichar_entrada(chat_id,0,0)
        elif texto == u"\U0000270B"+' Empezar Pausa':
            teclado = self.funcionTelegram.fichar_entrada(chat_id,0,1)
        elif texto == u"\U0000270B"+u"\U0001F6AB"+' Terminar Pausa':
            teclado = self.funcionTelegram.fichar_entrada(chat_id,1,1)
        elif texto == u"\U0001F4DA"+' Listados':
            menu = "Listado Empleado"
            user_port.cambiar_menu(chat_id,menu)
            teclado = self.funcionTelegram.listados_empleado(chat_id,bot)
        else:
            print(f'mensaje enviado por el usuario no valido: {texto}')
            return 1
        
        return teclado
    
################### Fin Fichar ###########################################   


################### Listados #############################################   

    def listado_empleado(self,mensaje, menu, chat_id,bot):        
        print("menu Listado Empleado")
        texto = mensaje.text
        print(texto)
        if texto == u"\U0001f519"+" Volver":
            menu = 'Fichar'
            teclado = self.inicioE(mensaje,menu, chat_id, bot)
            self.funcionTelegram.eliminar_mensajes(chat_id,bot)
        elif texto == u"\U0001f51d"+" Inicio":
            usuario_t = user_port.get_user_by_id_telegram(chat_id)
            if usuario_t.administrador:
                menu = 'Inicio'
                teclado = self.funcionTelegram.inicio(chat_id,menu)
            else:
                menu = 'Fichar'
                teclado = self.inicioE(mensaje,menu, chat_id, bot)
            self.funcionTelegram.eliminar_mensajes(chat_id,bot)
            user_port.cambiar_usuario(usuario_t.id_usuario,0)
        elif texto == u"\U0001F4C3"+' Hoy':
            print ("dentro menu listados para hoy")
            if self.funcionTelegram.listadoUnDia(bot,chat_id) is False:
                bot.enviar_texto(chat_id, 'No hay registros')
            return 2
                
        elif texto == u"\U0001F4C3"+' Ayer':
            print ("dentro menu listados para ayer")
            if self.funcionTelegram.listadoUnDia(bot,chat_id,None,True):
                bot.enviar_texto(chat_id, 'No hay registros')
            return 2

        user_port.cambiar_menu(chat_id,menu)
        return teclado 
    
    def listado_usuario(self,mensaje, menu, chat_id,bot):        
        print("menu Configuración Usuario Listados")
        texto = mensaje.text
        print(texto)
        if texto == u"\U0001f519"+" Volver":
            menu = 'Configuración Usuario Seleccionado'
            teclado = self.funcionTelegram.editar_usuario(chat_id,menu,bot)
            self.funcionTelegram.eliminar_mensajes(chat_id,bot)
        elif texto == u"\U0001f51d"+" Inicio":
            menu = 'Inicio'
            teclado = self.funcionTelegram.inicio(chat_id,menu)
            self.funcionTelegram.eliminar_mensajes(chat_id,bot)
            usuario_t = user_port.get_user_by_id_telegram(chat_id)
            user_port.cambiar_usuario(usuario_t.id_usuario,0)
        elif texto == u"\U0001F4C3"+' Hoy':
            print ("dentro menu listados para hoy")
            if self.funcionTelegram.listadoUnDia(bot,chat_id,None,False,True) is False:
                bot.enviar_texto(chat_id, 'No hay registros')
            return 2
        elif texto == u"\U0001F4C3"+' Ayer':
            print ("dentro menu listados para ayer")
            if self.funcionTelegram.listadoUnDia(bot,chat_id,None,True,True) is False:
                bot.enviar_texto(chat_id, 'No hay registros')
            return 2

        user_port.cambiar_menu(chat_id,menu)
        return teclado 

################### Fin Lisatados ########################################   

    
################### CONFIGURACION ########################################
    def configuracion(self,mensaje, menu, chat_id,bot):        
        print("menu configuracion")
        texto = mensaje.text
        print(texto)
        if texto == u"\U0001f519"+" Volver":
            menu = 'Inicio'
            teclado = self.funcionTelegram.inicio(chat_id,menu)
            #teclado = teclado_port.inicio()
        elif texto == u"\U0001f51d"+" Inicio":
            menu = 'Inicio'
            teclado = self.funcionTelegram.inicio(chat_id,menu)
        elif texto == u"\U0001F46B"+" Usuarios":
            if self.funcionTelegram.funcion_crear_eteclado_usuario_telegram(chat_id, bot) == 2:
                return 2          
            menu = 'Configuración Usuarios'
            teclado = teclado_port.config_usuarios()       
        elif texto ==u"\U0001f4cb"+" Empresa": 
            empresa = self.funcionTelegram.crear_empresa_si_eso()            
            if empresa:
                menu = 'Empresa'
                teclado = teclado_port.empresa(empresa)
            else:
                print('no se ha creado la empresa')
                teclado = False
        elif texto == u"\U0000231A"+' Horarios':
            if self.funcionTelegram.funcion_crear_eteclado_horarios(chat_id, bot) == 2:
                return 2          
            menu = 'Configuración Horario'
            teclado = self.funcionTelegram.config_horario(chat_id, bot)     
        else:
            print(f'mensaje enviado por el usuario no valido: {texto}')
            return 1 #teclado = 1 parametro no valido

        user_port.cambiar_menu(chat_id,menu)
        return teclado
    
    def configuracion_horario(self,mensaje, menu, chat_id,bot):        
        print("menu configuracion_horario")
        texto = mensaje.text
        print(texto)
        if texto == u"\U0001f519"+" Volver":
            menu = 'Configuración'
            teclado = self.funcionTelegram.configuracion(chat_id)
            self.funcionTelegram.eliminar_mensajes(chat_id,bot)
        elif texto == u"\U00002795"+' Crear':
            if self.funcionTelegram.funcion_crear_eteclado_usuario_telegram(chat_id, bot) == 2:
                return 2          
            menu = 'Crear Horario'
            teclado = teclado_port.volver('Escriba el nombre del horario o pulse en volver.')
            #teclado = teclado_port.editar_horario()         
        else:
            print(f'mensaje enviado por el usuario no valido: {texto}')
            return 1 #teclado = 1 parametro no valido

        user_port.cambiar_menu(chat_id,menu)
        return teclado
    
## ****************************************************************** ##
    
################### horario ############################################

    def crear_horario(self, mensaje, menu, chat_id, bot):
        print ('en el menu crear_horario')
        texto = mensaje.text
        print (texto)
        if texto == u"\U0001F519"+' Volver':
            print ("en el volver")
            if self.funcionTelegram.funcion_crear_eteclado_horarios(chat_id, bot) == 2:
                return 2          
            menu = 'Configuración Horario'
            teclado = self.funcionTelegram.config_horario(chat_id, bot) 
            user_port.cambiar_menu(chat_id,menu)
            return teclado
        else:
            menu = 'Horario'
            teclado = self.funcionTelegram.crear_horario(chat_id)
            #teclado_port.editar_horario()

        user_port.cambiar_menu(chat_id,menu)
        return teclado


    def horario(self, mensaje, menu, chat_id,bot):
        print ('en el menu horario')
        texto = mensaje.text
        print (texto)
        dato_empresa = {
            u"\U0001F3AB"+' Nombre':"Nombre",
            u"\U000023F3"+' Hora Inicio':"Inicio",
            u"\U0000231B"+' Hora Fin':"Fin",
            u"\U000023F3"+ u"\U0000231B"+' Horas al Día':"Horas"
        }
        if texto == u"\U0001F519"+' Volver':
            print ("en el volver")
            if self.funcionTelegram.funcion_crear_eteclado_horarios(chat_id, bot) == 2:
                return 2          
            menu = 'Configuración Horario'
            teclado = self.funcionTelegram.config_horario(chat_id, bot) 
            user_port.cambiar_menu(chat_id,menu)
            return teclado
        elif texto == u"\U0001f51d"+" Inicio":
            menu = 'Inicio'
            teclado = self.funcionTelegram.inicio(chat_id,menu)
            usuario_t = user_port.get_user_by_id_telegram(chat_id)
            user_port.cambiar_horario_temp(usuario_t.id_usuario,0) 
        elif texto == u"\U00002796"+' Eliminar':
            print ("en eliminar")
            teclado = teclado_port.sino('¿Seguro que desea eliminar el horario seleccionado?')
            menu = 'Eliminiar Horario'
        else:
            print ("Vamos a ejecutar: "+str(dato_empresa[texto]))
            if texto in dato_empresa:
                menu = dato_empresa[texto]+' Horario'
                print(menu)
                teclado = teclado_port.volver(f'Introduzca el valor para: {dato_empresa[texto]}')
                user_port.cambiar_menu(chat_id,menu)
                return teclado
            else:
                print(f'mensaje enviado por el usuario no valido: {texto}')
                return 1
            
    def eliminar_horario(self, mensaje, menu, chat_id, bot):
        print("menu eliminar_horario")
        texto = mensaje.text
        if texto == u"\u2714\uFE0F"+" SÍ":
            self.funcionTelegram.eliminar_horario(chat_id)
            if self.funcionTelegram.funcion_crear_eteclado_horarios(chat_id, bot) == 2:
                return 2             
            menu = 'Configuración Horario'
            teclado = self.funcionTelegram.config_horario(chat_id, bot) 
        elif texto == u"\u2716\uFE0F"+" NO":
            menu = 'Horario'
            teclado = self.funcionTelegram.editar_horario(chat_id)
        else:
            print(f'mensaje enviado por el usuario no valido: {texto}')
            teclado = 1         
        
        user_port.cambiar_menu(chat_id,menu)
        return teclado

    def horario_cambiar(self, mensaje, menu, chat_id,bot):
        print("menu horario cambiar")
        print(f'con el menu: {menu}')
        texto = mensaje.text
        print (texto)
        if texto == u"\U0001F519"+' Volver':
            print ("en el volver")  
        elif texto == u"\U0001f51d"+" Inicio":
            menu = 'Inicio'
            teclado = self.funcionTelegram.inicio(chat_id,menu)  
            usuario_t = user_port.get_user_by_id_telegram(chat_id)
            user_port.cambiar_horario_temp(usuario_t.id_usuario,0)       
        else:
            if menu == 'Nombre Horario':
                self.funcionTelegram.cambiar_horario(chat_id,1,texto)
                frase = f'Nombre del horario cambiado a: {texto}.'
            elif menu == 'Inicio Horario':
                self.funcionTelegram.cambiar_horario(chat_id,2,texto)
                frase = f'Inicio del horario cambiado a: {texto}.'
            elif menu == 'Fin Horario':
                self.funcionTelegram.cambiar_horario(chat_id,3,texto)
                frase = f'Fin del horario cambiado a: {texto}.'
            elif menu == 'Horas Horario':
                self.funcionTelegram.cambiar_horario(chat_id,4,texto)
                frase = f'Horas del día en el horario cambiado a: {texto} horas.'

        menu = 'Horario'
        teclado = self.funcionTelegram.editar_horario(chat_id, bot,frase)
        user_port.cambiar_menu(chat_id,menu)
        return teclado

## ****************** FIN Horario ************************************* ##
    
################### Empresa ##############################################


    def empresa(self, mensaje, menu, chat_id,bot):
        print ('en el menu empresa')
        texto = mensaje.text
        print (texto)
        dato_empresa = {
            u"\U0001F4DD"+' Nombre':"nombre",
            u"\U0001F4B3"+' CIF/NIF':"cif",
            u"\U0001F4CC"+' Dirección':"direccion",
            u"\U0001F3E2"+' Población':"poblacion",
            u"\U0001F4EA"+' C.P.':"cp",
            u"\U0001F3F0"+' Provincia':"provincia",
            u"\U00002709"+' EMAIL':"mail"
        }
        if texto == u"\U0001F519"+' Volver':
            print ("en el volver")
            menu = 'Configuración'
            teclado = self.funcionTelegram.configuracion(chat_id)
            user_port.cambiar_menu(chat_id,menu)
            return teclado
        elif texto == u"\U0001f51d"+" Inicio":
            teclado = self.funcionTelegram.inicio(chat_id,menu)
            user_port.cambiar_menu(chat_id,'Inicio')
            return teclado
        else:
            print ("Vamos a ejecutar: "+str(dato_empresa[texto]))
            if texto in dato_empresa:
                menu = 'Empresa '+dato_empresa[texto]
                teclado = teclado_port.volver(f'Introduzca el valor para: {dato_empresa[texto]}')
                user_port.cambiar_menu(chat_id,menu)
                return teclado
            else:
                print(f'mensaje enviado por el usuario no valido: {texto}')
                return 1

    def empresa_nombre(self, mensaje, menu, chat_id,bot):
        print("menu empresa nombre")
        texto = mensaje.text
        print (texto)
        if texto == u"\U0001F519"+' Volver':
            print ("en el volver")            
        else:
            empresa_port.cambiar_nombre(1,texto)
        menu = 'Empresa'
        teclado = teclado_port.empresa(empresa_port.get_by_id(1))
        user_port.cambiar_menu(chat_id,menu)
        return teclado

    def empresa_cif(self, mensaje, menu, chat_id,bot):
        print("menu empresa cif")
        texto = mensaje.text
        print (texto)
        if texto == u"\U0001F519"+' Volver':
            print ("en el volver")            
        else:
            empresa_port.cambiar_CIF(1,texto)
        menu = 'Empresa'
        teclado = teclado_port.empresa(empresa_port.get_by_id(1))
        user_port.cambiar_menu(chat_id,menu)
        return teclado

    def empresa_direccion(self, mensaje, menu, chat_id,bot):
        print("menu empresa direccion")
        texto = mensaje.text
        print (texto)
        if texto == u"\U0001F519"+' Volver':
            print ("en el volver")            
        else:
            empresa_port.cambiar_direccion(1,texto)
        menu = 'Empresa'
        teclado = teclado_port.empresa(empresa_port.get_by_id(1))
        user_port.cambiar_menu(chat_id,menu)
        return teclado

    def empresa_localidad(self, mensaje, menu, chat_id,bot):
        print("menu empresa localidad")
        texto = mensaje.text
        print (texto)
        if texto == u"\U0001F519"+' Volver':
            print ("en el volver")            
        else:
            empresa_port.cambiar_localidad(1,texto)
        menu = 'Empresa'
        teclado = teclado_port.empresa(empresa_port.get_by_id(1))
        user_port.cambiar_menu(chat_id,menu)
        return teclado

    def empresa_cp(self, mensaje, menu, chat_id,bot):
        print("menu empresa cp")
        texto = mensaje.text
        print (texto)
        if texto == u"\U0001F519"+' Volver':
            print ("en el volver")            
        else:
            empresa_port.cambiar_CP(1,texto)
        menu = 'Empresa'
        teclado = teclado_port.empresa(empresa_port.get_by_id(1))
        user_port.cambiar_menu(chat_id,menu)
        return teclado

    def empresa_provincia(self, mensaje, menu, chat_id,bot):
        print("menu empresa provincia")
        texto = mensaje.text
        print (texto)
        if texto == u"\U0001F519"+' Volver':
            print ("en el volver")            
        else:
            empresa_port.cambiar_provincia(1,texto)
        menu = 'Empresa'
        teclado = teclado_port.empresa(empresa_port.get_by_id(1))
        user_port.cambiar_menu(chat_id,menu)
        return teclado

    def empresa_mail(self, mensaje, menu, chat_id,bot):
        print("menu empresa mail")
        texto = mensaje.text
        print (texto)
        if texto == u"\U0001F519"+' Volver':
            print ("en el volver")            
        else:
            empresa_port.cambiar_mail(1,texto)
        menu = 'Empresa'
        teclado = teclado_port.empresa(empresa_port.get_by_id(1))
        user_port.cambiar_menu(chat_id,menu)
        return teclado
    
################### FIN --Empresa ########################################

    """     def informes(self, mensaje,menu, chat_id,bot):
        print("menu informes")
        texto = mensaje.text
        if texto == u"\U0001f519"+" Volver":
            user_port.cambiar_menu(chat_id,'Inicio')
            teclado = self.funcionTelegram.inicio(chat_id,menu) 
        else:
            user_port.cambiar_menu(chat_id,'Inicio')
            teclado = self.funcionTelegram.inicio(chat_id,menu)
        return teclado
    """
## ****************************************************************** ##

    
################### CONFIGURACION Usuarios ###############################
    def configuracion_usuarios(self, mensaje, menu, chat_id,bot):
        print("menu configuracion usuarios")
        #return menu_configuracion.menu_configuracion_usuarios(mensaje,menu,chat_id,bot)
        texto = mensaje.text
        if texto == u"\U0001f519"+" Volver":
            teclado = self.funcionTelegram.configuracion(chat_id)
            if teclado == False or teclado == 2:
                print(menu)
            else:
                menu = 'Configuración'                
        elif texto == u"\U0001f51d"+" Inicio":
            menu = 'Inicio'
            teclado = self.funcionTelegram.inicio(chat_id,menu)
            usuario_t = user_port.get_user_by_id_telegram(chat_id)
            user_port.cambiar_usuario(usuario_t.id_usuario,0)
        elif texto == u"\u2795"+" Añadir Usuario":
            menu = 'Añadir Usuario'
            teclado = teclado_port.add_usuario()
        else:
            print(f'mensaje enviado por el usuario no valido: {texto}')
            return 1
        
        user_port.cambiar_menu(chat_id,menu)
        return teclado
       
    def configuracion_usuario_seleccionado(self,mensaje, menu, chat_id,bot):
        print("menu configuracion usuario seleccionado")
        texto = mensaje.text
        dato_empresa = {
            u"\U0001F464"+" Nombre":"Nombre",
            u"\U0001F46A"+" Apellido":"Apellido",
            u"\U0001F4F1"+" Telefono":"Telefono",
            u"\U0001F6C2"+" NIF/NIE":"CIF",
            u"\U0001F4DC"+" Nº SS":"SS",
            u"\U00002709"+" Email":"Mail",
            u"\U0001F44E"+" Baja":"Baja"
        }
        if texto == u"\U0001f519"+" Volver":
            if self.funcionTelegram.funcion_crear_eteclado_usuario_telegram(chat_id, bot) == 2:
                return 2
            menu = 'Configuración Usuarios'
            teclado = teclado_port.config_usuarios()
            usuario_t = user_port.get_user_by_id_telegram(chat_id)
            user_port.cambiar_usuario(usuario_t.id_usuario,0)
            user_port.cambiar_menu(chat_id,menu)
            return teclado
        
        elif texto == u"\U0001f51d"+" Inicio":
            menu = 'Inicio'
            teclado = self.funcionTelegram.inicio(chat_id,menu)
            usuario_t = user_port.get_user_by_id_telegram(chat_id)
            user_port.cambiar_usuario(usuario_t.id_usuario,0)
        elif texto == u"\u2796"+" Eliminar Usuario":
            print('vamos con la eliminacion')
            if self.funcionTelegram.eliminar_usuario(chat_id) == False:
                return 2
            usuario_t = user_port.get_user_by_id_telegram(chat_id)
            user_port.cambiar_usuario(usuario_t.id_usuario,chat_id)
            if self.funcionTelegram.funcion_crear_eteclado_usuario_telegram(chat_id, bot) == 2:
                return 2
            menu = 'Configuración Usuarios'
            teclado = teclado_port.config_usuarios()
            usuario_t = user_port.get_user_by_id_telegram(chat_id)
            user_port.cambiar_usuario(usuario_t.id_usuario,0)
            user_port.cambiar_menu(chat_id,menu)
        elif texto == u"\U0001f9b8\u200D\u2642\uFE0F"+" Hacer Administrador":
            print('dentro de hacer administrador')
            teclado = self.funcionTelegram.modificar_usuario_administrador(chat_id,1,menu,bot)
        elif texto == u"\U0001f9b8\u200D\u2642\uFE0F"+" Quitar de Administrador":
            teclado = self.funcionTelegram.modificar_usuario_administrador(chat_id,0,menu,bot)

        elif texto == u"\U0000231A"+' Horario':
            menu = 'Configuración Usuario Horario'
            if self.funcionTelegram.funcion_crear_eteclado_horarios(chat_id,bot) == 2:
                print('Error en la creacion de horarios')
                return 2
            teclado = teclado_port.volver('Seleccione el horario que desee o pulse en volver.')
        elif texto == u"\U0001F44E"+" Baja":
            menu = 'Configuración Usuario Baja'
            teclado = teclado_port.sino('Esta seguro de dar de Baja?, el usuario ya no podrá realizar fichajes\nSi pulsa en "NO", no se hará ningún cambio si pulsa en "SÍ", se hara el cambio de estado de baja.')
        elif texto == u"\u2796"+" Listados":
            menu = 'Configuración Usuario Listados'
            teclado = self.funcionTelegram.listados_empleado(chat_id,bot)


        elif texto in dato_empresa:
            print ("Vamos a ejecutar: "+str(dato_empresa[texto]))
            menu = 'Configuración Usuario '+dato_empresa[texto]
            teclado = teclado_port.volver(f'Introduzca el valor para: {dato_empresa[texto]}')
            user_port.cambiar_menu(chat_id,menu)
            return teclado
        else:
            print(f'mensaje enviado por el usuario no valido: {texto}')
            return 1 #teclado = 1 parametro no valido
        
        #self.funcionTelegram.eliminar_mensajes(chat_id,bot)
        user_port.cambiar_menu(chat_id,menu)
        return teclado

    def configuracion_usuario_horario(self, mensaje, menu, chat_id, bot):
        print("menu configuracion_usuario_baja")
        texto = mensaje.text
        if texto == u"\U0001F519"+' Volver':
            print ("en el volver") 
        else:
            print(f'mensaje enviado por el usuario no valido: {texto}')
            return 1         
        menu = 'Configuración Usuario Seleccionado'
        teclado = self.funcionTelegram.editar_usuario(chat_id,menu,bot)
        user_port.cambiar_menu(chat_id,menu)
        return teclado

    def configuracion_usuario_baja(self, mensaje, menu, chat_id, bot):
        print("menu configuracion_usuario_baja")
        texto = mensaje.text
        if texto == u"\u2714\uFE0F"+" SÍ":
            frase = 'Se ha cambiado el estado baja.' 
            self.funcionTelegram.baja_usuario(chat_id)
        elif texto == u"\u2716\uFE0F"+" NO":
            frase = 'No se ha modificado el estado'
        else:
            print(f'mensaje enviado por el usuario no valido: {texto}')
            return 1         
        print(frase)
        menu = 'Configuración Usuario Seleccionado'
        teclado = self.funcionTelegram.editar_usuario(chat_id,menu,bot,frase)
        user_port.cambiar_menu(chat_id,menu)
        return teclado

    def configuracion_usuario_cambiar(self, mensaje, menu, chat_id,bot):
        print("menu horario cambiar")
        print(f'con el menu: {menu}')
        texto = mensaje.text
        print (texto)
        if texto == u"\U0001F519"+' Volver':
            print ("en el volver")  
        elif texto == u"\U0001f51d"+" Inicio":
            menu = 'Inicio'
            teclado = self.funcionTelegram.inicio(chat_id,menu)         
        else:
            if menu == 'Configuración Usuario Nombre':
                self.funcionTelegram.cambiar_usuario(chat_id,1,texto)
                frase = f'Nombre del usuario cambiado a: {texto}.'
            elif menu == 'Configuración Usuario Apellido':
                self.funcionTelegram.cambiar_usuario(chat_id,2,texto)
                frase = f'Apellidos del usuario cambiado a: {texto}.'
            elif menu == 'Configuración Usuario Telefono':
                self.funcionTelegram.cambiar_usuario(chat_id,3,texto)
                frase = f'Telefono del usuario cambiado a: {texto}.'
            elif menu == 'Configuración Usuario CIF':
                self.funcionTelegram.cambiar_usuario(chat_id,4,texto)
                frase = f'El DNI/NIE del usuario cambiado a: {texto}.'
            elif menu == 'Configuración Usuario SS':
                self.funcionTelegram.cambiar_usuario(chat_id,5,texto)
                frase = f'Nº Seguridad Social del usuario cambiado a: {texto}.'
            elif menu == 'Configuración Usuario Mail':
                self.funcionTelegram.cambiar_usuario(chat_id,6,texto)
                frase = f'El correo electrónico del usuario cambiado a: {texto}.'
            else:
                print(f'mensaje enviado por el usuario no valido: {texto}')
                return 1

        print(frase)
        menu = 'Configuración Usuario Seleccionado'
        teclado = self.funcionTelegram.editar_usuario(chat_id,menu,bot,frase)
        user_port.cambiar_menu(chat_id,menu)
        return teclado
    
    def add_usuario(self,mensaje, menu, chat_id, bot):
        print("menu añadir usuario")
        error = False
        if mensaje.content_type == 'text':
            print('es texto')
            if mensaje.text == u"\U0001f519"+" Volver":
                if self.funcionTelegram.funcion_crear_eteclado_usuario_telegram(chat_id, bot) == 2:
                    return 2
                menu = 'Configuración Usuarios'
                teclado = teclado_port.config_usuarios()              
            else:
                print(f'mensaje enviado por el usuario no valido: {mensaje.text}')
                return 1 #teclado = 1 parametro no valido
        elif mensaje.content_type == "contact":	
            menu = 'Configuración'
            teclado = teclado_port.configuracion()
            #if mensaje.contact.user_id is None or mensaje.contact.first_name is None or mensaje.contact.phone_number is None:
            #if mensaje.contact.user_id == None or mensaje.contact.first_name == None or mensaje.contact.phone_number == None:
            if any(var is None for var in (mensaje.contact.user_id, mensaje.contact.first_name, mensaje.contact.phone_number)):
                bot.enviar_texto(chat_id, 'El contacto pasado no contiene los parametros necesarios\n*ID_User: '+str(mensaje.contact.user_id)+'\n*Nombre: '+str(mensaje.contact.first_name)+'\nApellido: '+str(mensaje.contact.last_name)+'\n*Telefono: '+str(mensaje.contact.phone_number)+'\n(*) Campos obligatorios.\nSi el campo ID_User es None es que el usuario pasado no tiene cuenta en Telegram.')
                print(mensaje.contact)
                return None
            try:
                #print(mensaje.contact.user_id)
                print('vamos con el create_user')
                estado = user_port.create_user(str(mensaje.contact.user_id),str(mensaje.contact.first_name),str(mensaje.contact.last_name),'Inicio',str(mensaje.contact.phone_number),None,None,False)
            except Exception as e:
                print('error insert user:', e)
                error = True 
            if estado == False:
                bot.enviar_texto(chat_id, 'El usuario ya existe en la base de datos como usuario del sistema')          
        if error:
            return None
        else:
            user_port.cambiar_menu(chat_id,menu)
            return teclado
################### FIN --CONFIGURACION Usuarios #########################

## ****************************************************************** ##

################### FIN --CONFIGURACION ##################################
