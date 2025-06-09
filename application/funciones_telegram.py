# application/funciones_telegram.py

import sys
import pdfkit
from datetime import datetime, timedelta, date

from application.user_servicios_inicializar import teclado_port, user_port, fichar_port, empresa_port, horario_port, usuario_horario_port
from application import listados



class FuncionTelegram:
    def __init__(self):
        None
    
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
    
    def actualizar_eteclat(self,user_id, message_id):
        try:
            # Obtener el usuario por ID
            usuario = user_port.get_user_by_id_telegram(user_id)
            if usuario:
                # Actualizar el campo eteclat
                usuario.eteclat = message_id
                # Confirmar los cambios en la base de datos
                user_port.modificar(usuario)
                print(f'Usuario {user_id} actualizado.')
            else:
                print(f'Usuario con ID {user_id} no encontrado.')
        except Exception as e:
            print(f'Error al actualizar eteclat: {e}')

    def eliminar_mensajes(self,chat_id, bot):
        try:
            print('elimando mensaje')
            usuario = user_port.get_user_by_id_telegram(chat_id)
            if usuario:
                if int(usuario.eteclat) > 0:
                    try:
                        bot.eliminar_etecado(chat_id, usuario.eteclat)
                        self.actualizar_eteclat(chat_id,0)
                    except:
                        print('error al eliminar el eteclat')
                else:
                    print(f'No se elimina mensaje por tener identificador con valor: {usuario.eteclat}')
            else:
                print(f'No existe el usuario con id: {chat_id}')
        except:
            print(f'No se ha podido eliminar el eteclado del usuario: {chat_id}')

    def existe_usuario(self,user_id,mensaje=None):
        if mensaje.text == '/empezamos':## Palabra clave para crear el administrador inicial.
            contador = user_port.usuarios()
            if contador == 0:
                print('id de usuario telegram: '+str(user_id))
                user_port.create_user(user_id,'Administrador','','Inicio','',None,1)
            else:
                return False

        usuario = user_port.get_user_by_id_telegram(user_id)
        if usuario:
            return True
        else:
            return False
        
    def actualizar_eteclat(self, user_id, message_id):
        try:
            # Obtener el usuario por ID
            usuario = user_port.get_user_by_id_telegram(user_id)
            if usuario:
                # Actualizar el campo eteclat
                usuario.eteclat = message_id
                # Confirmar los cambios en la base de datos
                user_port.modificar(usuario)
                print(f'Usuario {user_id} actualizado.')
            else:
                print(f'Usuario con ID {user_id} no encontrado.')
        except Exception as e:
            print(f'Error al actualizar eteclat: {e}')

    def inicio(self, chat_id, menu):
        print('funcion inicio')
        teclado = teclado_port.inicio(1,0)
        return teclado

    def inicioE(self, chat_id):
        print('funcion inicioE')
        user = user_port.get_user_by_id_telegram(chat_id)
        print('usuario demandado')
        if user:
            print('usuario obtenido')
            admin = user.administrador 
            print(f'admin= {admin}')
            entra = user.trabajando
            pausa = user.pausado
            hora = self.horas_trabajadas(user.id_usuario,fecha = date.today().strftime("%Y-%m-%d"))
            print(hora, entra, pausa, admin)
            if hora:
                print('existe hora')
                print(f"Tipo de hora: {type(hora)}") 
                None
            else:
                print('se crea hora')
                hora = '00:00'#datetime.strptime("0:00", "%H:%M")
            print(hora)
            teclado = teclado_port.inicio(admin,1, entra, pausa, hora)            
        else:
            print(f'no hay usuario con id: {chat_id}')
            teclado = 1
        print(teclado.botones)
        return teclado
    
    def es_admin(self,chat_id):
        print('dentro del es_admin')
        usuario = user_port.get_user_by_id_telegram(chat_id)
        if usuario:
            if usuario.administrador:
                return True
            else:
                return False
        else:
            return False
    
    def fichar_entrada(self, chat_id, entrada=1,pausa=0):
        '''
        inserta el fichaje para el usuario chat_id segun\n
        entrada si entrada es 1\n 
        salidad si entrada es 0\n 
        para que se marque como pausa debe estar la variable pausa a 1
        '''
        hora = str(datetime.now().hour)+":"+str(datetime.now().minute)
        print (hora)
        hora = datetime.now().strftime("%H:%M")
        print(hora)
        fecha = date.today()
        print (fecha)
        trab = user_port.get_user_by_id_telegram(chat_id)
        user_id = trab.id_usuario
        if entrada:
            fichar_port.create(user_id,fecha,hora,'',pausa)
        else:
            fichar_port.create(user_id,fecha,'',hora,pausa)
        
        user_port.cambiar_trabajando(user_id,entrada)
        user_port.cambiar_pausado(user_id,pausa)
        print('terminado entrar')
        return self.inicioE(chat_id)

    def horas_trabajadas(self, usuario_id, fecha):
        # Consultar los registros de fichaje para el usuario en la fecha especificada
        print('dentro del horas_trabajadas')
        registros = fichar_port.get_by_id_user_fecha(usuario_id, fecha)
        print(registros)
        total_horas_trabajadas = timedelta()
        tiempo_trabajado = timedelta()
        en_trabajo = False
        ultima_entrada = None

        if registros:
            print('dentro registros')
            for r in registros:
                print('dentro bucle')
                if r.hora_entrada:  # Registro de entrada
                    print(f'dentro hora_entrada: {r.hora_entrada}')
                    entrada = datetime.strptime(r.hora_entrada, '%H:%M')
                    
                    if en_trabajo:  # Si ya estaba trabajando, sumar el tiempo trabajado
                        # Si hay una entrada anterior, sumar el tiempo trabajado hasta esta nueva entrada
                        if ultima_entrada:
                            tiempo_trabajado += entrada - ultima_entrada
                    
                    ultima_entrada = entrada
                    en_trabajo = True

                elif r.hora_salida:  # Registro de salida
                    print('dentro hora_salida')
                    salida = datetime.strptime(r.hora_salida, '%H:%M')
                    
                    if en_trabajo:  # Si estaba trabajando, sumar el tiempo trabajado
                        tiempo_trabajado += salida - ultima_entrada
                        en_trabajo = False  # Cambiar el estado a no trabajando

                if r.pausa == 1:  # Si hay una pausa
                    if en_trabajo and ultima_entrada:  # Si estaba trabajando
                        # Detener el tiempo trabajado hasta la próxima entrada
                        # No se suma tiempo trabajado durante la pausa
                        en_trabajo = False  # Cambiar el estado a no trabajando
                        ultima_entrada = None  # Reiniciar la última entrada

                # Si hay una nueva entrada después de una pausa, se reinicia el tiempo
                if r.pausa == 0 and not en_trabajo and ultima_entrada is None:
                    # Reiniciar la última entrada para la nueva entrada
                    ultima_entrada = entrada

            # Sumar el tiempo trabajado
            total_horas_trabajadas += tiempo_trabajado
            total_horas_trabajadas = self.formato_timedelta(total_horas_trabajadas)
            print(f'Total horas trabajadas: {total_horas_trabajadas}')

            # Devolver el total de horas trabajadas
            return total_horas_trabajadas
        else:
            return self.formato_timedelta(timedelta(0))

    def formato_timedelta(self, td):
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}"

    def crear_empresa_si_eso(self):
        #print('en crear_empresa_si_eso')
        empresa=empresa_port.get_by_id(1)
        if empresa:
            print('hay empresa')
            return empresa
        else:  
            print('Se crea la empresa')
            empresa = empresa_port.create('Nombre Empresa')
            if empresa:
                print('Empresa Creada')
                return empresa
            else:
                return False
            
    def elistado_listados(self, call, bot, admin):
        print('funcion elistado_listados')
        operacion = call.data
        print(f'operacion: {operacion}')
        bien = False
        if operacion == 'hoy':
            bien = self.listadoUnDia(bot,call.message.chat.id,False,None,admin)
        elif operacion == 'ayer':
            bien = self.listadoUnDia(bot,call.message.chat.id,False,True,admin)            
        else:
            None
        if bien:
            None
            #self.eliminar_mensajes(call.message.chat.id,bot)
        return 2
       
    def elistado_listados_usuario(self, call, bot):
        print('funcion elistado_listados_usuario')
        operacion = call.data
        user = user_port.get_user_by_id_telegram(call.message.chat.id)
        if user:
            user_temp = user_port.get_user_by_id(user.id_usuario_temp)
            if user_temp:
                print(f'operacion: {operacion}')
                bien = False
                if operacion == 'hoy':
                    bien = self.listadoUnDia(bot,call.message.chat.id,False,None,True)
                elif operacion == 'ayer':
                    bien = self.listadoUnDia(bot,call.message.chat.id,False,True,True)            
                else:
                    None
                if bien:
                    None
                    #self.eliminar_mensajes(call.message.chat.id,bot)
                return 2
            else:
                print('no hay usuario temporal seleccionado')
                return False
        else:
            print('Error obteniendo el usuario')
            return False

    def listadoHoy(self,bot,chat_id,admin):
        self.listadoUnDia(bot,chat_id,True,None,admin)

    def listadoAyer(self,bot,chat_id,admin):
        self.listadoUnDia(bot,chat_id,True,True,admin)

    def listadoUnDia(self, bot, chat_id,eteclado=None,ayer=None,admin=None):
        '''
        "eteclado" para saber si se ha solicitado del teclado online y se requiere del contenido \n
        por pantalla \n
        o por el contrario si se requiere\n 
        de un archivo.\n
        "ayer" para saber si es el listado de hoy que seria None o de ayer con True.\n
        "admin" para saber i es el listado de un empleado que esta en la variable\n
        id_usuario_temp en el caso de ser True\n
        o ben la variable id propia del usuario en el caso de ser None\n
        id_usuario.
        '''
        print ("dentro funcion listadoUnDia")
        if ayer:
            print (str(ayer))
        else:
            print ("ayer none")

        trab = user_port.get_user_by_id_telegram(chat_id)
        if trab:
            if admin:
                id_trabajador = trab.id_usuario_temp
            else:
                id_trabajador = trab.id_usuario
        else:
            return ("empresa password")   
        if ayer is not None:
            texto, texto2 = listados.ayer(id_trabajador)
            #print(f'dia de ayer: {texto}')
            print ("se ha hecho el listado de ayer")
        else:
            print('hasta aqui02')
            texto, texto2 = listados.hoy(id_trabajador)
            print ("se ha hecho el listado de hoy")
        if eteclado is not None:
            print('hasta aqui')
            if texto2:
                print('hasta aqui1')
                bot.enviar_texto(chat_id,texto2)
            else:
                print('hasta aqui2')
                bot.enviar_texto(chat_id,"No tiene ningun fichaje.")
        else:     
            try:
                bot.enviar_accion(chat_id, 'upload_document')
                print ("chat action enviada")
            except:
                print('hasta aqui5')
                bot.enviar_texto(chat_id,"Envio de Documento")

            if texto:   
                pdfkit.from_string(texto, str(id_trabajador)+'.pdf')
                doc = open(str(id_trabajador)+'.pdf','rb')
                bot.enviar_archivo(chat_id, doc)
            else:
                print('no hay texto')
                return False
        return True

## ****************************************************************** ##

################### Usuarios ###########################################
################### Funiones Usuarios ##################################

    def funcion_eteclado_usuario_telegram(self):
        print('funcion_config_usuario funcion_eteclado_usuario_telegram')
        print('dentro del eteclado usuario telegram')
        usuario = user_port.get_all_users()
        if usuario:
            print(f'usuario telegram: {usuario[0].nombre}')
            return teclado_port.e_listado_usuarios_telegram(usuario)
        else:
            return False


    def funcion_crear_eteclado_usuario_telegram(self,chat_id, bot):
        print('funcion_config_usuario funcion_crear_eteclado_usuario_telegram')
        try:
            teclado = self.funcion_eteclado_usuario_telegram()
            message = bot.enviar_eteclado(chat_id, teclado, 1)
            if message:
                print('id eteclado es: '+str(message.message_id))
                self.actualizar_eteclat(chat_id, message.message_id)
                return True
            else:
                print('no existe message')
                return 2
        except Exception as e:
            print(f'Error al actualizar eteclat: {e}')
            return 2
        
    def funcion_crear_eteclado_listados(self,chat_id, bot):
        print('funcion funcion_crear_eteclado_listados')
        try:
            teclado = teclado_port.e_listado_listados()
            message = bot.enviar_eteclado(chat_id, teclado, 1)
            if message:
                print('id eteclado es: '+str(message.message_id))
                self.actualizar_eteclat(chat_id, message.message_id)
                return True
            else:
                print('no existe message')
                return 2
        except Exception as e:
            print(f'Error al actualizar eteclat: {e}')
            return 2
        
    def funcion_crear_eteclado_horarios(self,chat_id, bot):
        print('funcion funcion_crear_eteclado_horarios')
        try:
            horarios = horario_port.get_all()
            if horarios:
                teclado = teclado_port.e_horario(horarios)
                message = bot.enviar_eteclado(chat_id, teclado, 1)
                if message:
                    print('id eteclado es: '+str(message.message_id))
                    self.actualizar_eteclat(chat_id, message.message_id)
                    return True
                else:
                    print('no existe message')
                    return 2
            else: return 2
        except Exception as e:
            print(f'Error al actualizar eteclat: {e}')
            return 2
           
################### FIN --Teclados Usuarios ############################
################### Navegar Usuarios ###################################
    def seleccionar_usuario_telegram(self,call,menu,bot):
        usuario_id = str(call.data)
        chat_id = call.message.chat.id
        print(f'usuario bd: {usuario_id}')
        return self.seleccionar_usuario(chat_id,usuario_id,menu,bot)

    def seleccionar_usuario(self,chat_id,usuario_id,menu,bot,frase=''):
        print('funcion seleccionar_usuario')
        print(usuario_id)
        userbot = user_port.get_user_by_id_telegram(chat_id)# usuario administrador
        usuario = user_port.get_user_by_id(usuario_id)# usuario al que el administrador quiere modificar
        print('usuario obteniendo')
        if usuario:
            print('usuario obtenido')
            nombre = 'Sin Nombre' if usuario.nombre is None or usuario.nombre == '' else usuario.nombre
            teclado = teclado_port.config_usuario_seleccionado(nombre,usuario.telefono,usuario.apellidos,usuario.administrador,usuario.dni,usuario.n_ss,usuario.mail,usuario.baja)#funcion_crear_teclado_usuario_configuracion(call.message.chat.id,user=usuario,user_telegram=usuario_telegram)
            if teclado:
                user_port.cambiar_usuario(userbot.id_usuario,usuario.id_usuario)
                self.eliminar_mensajes(chat_id, bot) 
                print('Usuario inline seleccionado')
                menu = 'Configuración Usuario Seleccionado'
                if frase:
                    teclado.texto += '\n'+frase
            else:
                print('no hay usuario con el codigo pasado')
                teclado = teclado_port.config_usuarios()
                teclado.texto = '¡¡El usuario no existe!! '+ u"\U0001f61e"
                print(teclado)
        else:
            print(f'No se ha obtenido usuario, variable chat_id: {chat_id}, la varible usuario_id: {usuario_id}')
        
        user_port.cambiar_menu(chat_id,menu)
        return teclado
    
    def listados_empleado(self,chat_id,bot):
        print('funcion listados_empleado')
        self.funcion_crear_eteclado_listados(chat_id, bot)
        teclado = teclado_port.listados("Seleccione el listado que desee descargar desde el teclado de abajo.")
        return teclado

    
################### FIN --Navegar Usuarios #############################
################### Edicion Usuarios ################################### 
    def modificar_usuario_administrador(self,chat_id,admin,menu,bot):
        print('funcion modificar_usuario_administrador')
        usuario = user_port.get_user_by_id_telegram(chat_id)
        if usuario:
            id_usuario_temp = usuario.id_usuario_temp
            usuario_tmp = user_port.get_user_by_id(id_usuario_temp)
            if usuario_tmp:
                #print(usuario_tmp.nombre)
                usuario_tmp.administrador = admin
                usuario_tmp = user_port.modificar(usuario_tmp)
                print(f'usuario modificado: {usuario_tmp.administrador}')
                return self.editar_usuario(chat_id,menu,bot,'Se ha modificado el estado de la propiedad: Administrador')
            else:
                return 2
        else:
            return 2
            
    def editar_usuario(self,chat_id,menu,bot,frase= 'Edite el campo que necesite.'):
        userbot = user_port.get_user_by_id_telegram(chat_id)
        usuario = user_port.get_user_by_id(userbot.id_usuario_temp)
        if userbot:
            print('aqui')
            return self.seleccionar_usuario(chat_id,usuario.id_usuario,menu,bot,frase)
        else:
            print('no existe el usuario')
            return False
            
    def cambiar_usuario(self,chat_id,tipo,texto):
        usuario = user_port.get_user_by_id_telegram(chat_id)
        if usuario:
            id = usuario.id_usuario_temp
            if tipo == 1:
                user_port.cambiar_nombre(id,texto)
            elif tipo == 2:
                user_port.cambiar_apellidos(id,texto)
            elif tipo == 3:
                user_port.cambiar_telefono(id,texto)
            elif tipo == 4:
                user_port.cambiar_dni(id,texto)
            elif tipo == 5:
                user_port.cambiar_n_ss(id,texto)
            elif tipo == 6:
                user_port.cambiar_mail(id,texto)
        else:
            return 2
        return True
    
    def baja_usuario(self,chat_id):
        usuario = user_port.get_user_by_id_telegram(chat_id)
        if usuario:
            usu = user_port.get_user_by_id(usuario.id_usuario_temp)
            if usu:
                if usu.baja == 0:
                    user_port.cambiar_baja(usu.id_usuario,1)
                else:
                    user_port.cambiar_baja(usu.id_usuario,0)
                return True
            else:
                return False
        else:
            return False

    def horario_seleccionado_usuario(self,call, bot):
        horario_id = str(call.data)
        chat_id = call.message.chat.id
        usuario = user_port.get_user_by_id_telegram(chat_id)
        #user_port.cambiar_horario_temp(usuario.id_usuario,horario_id)

        horario = usuario_horario_port.get_by_id_user_id_horario(usuario.id_usuario_temp,horario_id)
        if horario:
            texto = 'El usuario ya tiene asignado este horario.'
        else:
            hora = usuario_horario_port.create(usuario.id_usuario_temp,horario_id)
            if hora:
                horari = horario_port.get_by_id(horario_id)
                if horari:
                    texto = f'Horario seleccionado ({horari.nombre}) asignado al usuario.'
                else:
                    texto = 'Horario seleccionado asignado al usuario.'
        self.eliminar_mensajes(chat_id,bot)
        menu = 'Configuración Usuario Seleccionado'
        teclado = self.editar_usuario(chat_id,menu,bot,texto)
        user_port.cambiar_menu(chat_id,menu)
        return teclado

################### FIN --Edicion Usuarios #############################
################### FIN --Usuarios #####################################
    
################### --Horarios #########################################

    def config_horario(self,chat_id,bot):
        teclado = teclado_port.horario("Seleccione el horario que desee modificar o cree uno.")
        return teclado
     
    def crear_horario(self,chat_id, nombre):
        horario = horario_port.create(nombre = nombre)
        usuario = user_port.get_user_by_id_telegram(chat_id)
        if horario:
            if usuario:
                user_port.cambiar_horario_temp(usuario.id_usuario,horario.id_horario)
                return teclado_port.editar_horario(horario.id_horario)
            else:
                return 2
        else:
            return 2
    
    def editar_horario(self,chat_id,bot,frase= 'Edite el campo que necesite.'):
        usuario = user_port.get_user_by_id_telegram(chat_id)
        if usuario:
            
            self.eliminar_mensajes(chat_id,bot)
            menu = 'Horario'
            user_port.cambiar_menu(chat_id,menu)
            return teclado_port.editar_horario(frase)
        else:
            print('no existe el usuario')
            return False
        
    def cambiar_horario(self,chat_id,tipo,texto):
        usuario = user_port.get_user_by_id_telegram(chat_id)
        if usuario:
            id = usuario.id_horario_temp
            if tipo == 1:
                horario_port.cambiar_nombre(id,texto)
            elif tipo == 2:
                horario_port.cambiar_inicio(id,texto)
            elif tipo == 3:
                horario_port.cambiar_fin(id,texto)
            elif tipo == 4:
                horario_port.cambiar_horas_dia(id,texto)
        else:
            return 2
        return True

    def eliminar_horario(self,chat_id):
        usuario = user_port.get_user_by_id_telegram(chat_id)
        if usuario:
            id = usuario.id_horario_temp
            horario_port.eliminar(id)
            user_port.cambiar_horario_temp(usuario.id_usuario,None)

    def horario_seleccionado(self,call, bot):
        horario_id = str(call.data)
        chat_id = call.message.chat.id
        usuario = user_port.get_user_by_id_telegram(chat_id)
        user_port.cambiar_horario_temp(usuario.id_usuario,horario_id)
        horario = horario_port.get_by_id(horario_id)
        if horario:
            texto = f'Nombre del Horario: {horario.nombre}\nHora Inicio: {horario.inicio}\nHora Fin: {horario.fin}\nHoras Día: {horario.horas_dia}\nModifique el campo que necesite.'
        return self.editar_horario(chat_id,bot,texto)

################### FIN --Horarios ######################################        
    
    def configuracion(self,chat_id):
        print('dentro funcion configuracion')
        usuario = user_port.get_user_by_id_telegram(chat_id)
        if usuario:
            admin = usuario.administrador
        else:
            print('no existe usuario')
            return 2
        if admin:
            return teclado_port.configuracion()
        else:
            return False

    def menu(self,chat_id):
        usuario =user_port.get_user_by_id_telegram(chat_id)
        print('tenemos el usuario vamos a por el menu')
        if usuario:
            return usuario.menu
        else:
            return None