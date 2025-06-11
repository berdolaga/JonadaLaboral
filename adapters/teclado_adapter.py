# adapters/teclado_adapters.py

# Proyecto desarrollado como parte del Trabajo de Fin de Grado (TFG)
# Curso de Adaptación al Grado en Ingeniería Informática - UNIR
# Autor: [Alberto Toledo Escrihuela]
# Año: 2025

from objects.teclado import Teclado

class TecladoAdapter():

    def inicio(self, admin):
        print('teclado inicio.')
        if admin:
            contenido = []
            contenido.append([u"\U0001f558"+" Fichar"])
            contenido.append([u"\u2699\uFE0F"+" Configuración"])
            #contenido.append([u"\U0001f558"+" Ver Fichajes"])
            return Teclado(contenido, 'Elije una opción que desee del teclado:')
        else:
            return False
    
    def inicioE(self, admin, entra, pausa, texto):
        contenido = []
        if pausa == 1:
            if entra == 0:
                contenido.append([u"\U0000270B"+u"\U0001F6AB"+' Terminar Pausa'])
            else:
                contenido.append([u"\U00002B05"+u"\U0001F6AA"+' SALIDA'])
                contenido.append([u"\U0000270B"+' Empezar Pausa'])
        else:
            if entra == 1:
                contenido.append([u"\U00002B05"+u"\U0001F6AA"+' SALIDA'])
                contenido.append([u"\U0000270B"+' Empezar Pausa'])
            else:
                contenido.append([u"\U000027A1"+u"\U0001F6AA"+' ENTRADA'])
   
        contenido.append([u"\U0001F4DA"+' Listados'])

        print(texto)

        if admin:
            contenido.append([u"\U0001F519"+' Volver'])
        print(contenido)
        return Teclado(contenido, 'Elije una opción de fichaje o sacar listados, desde el teclado\n'
                       'El tiempo que lleva trabajando el día de hoy es:\n'+texto)
   
    def volver(self, texto):
        return Teclado([[u"\U0001f519"+" Volver"]],texto)
    
    def si_no(self, texto):
        return Teclado([[u"\u2714\uFE0F"+" SÍ",u"\u2716\uFE0F"+" NO"]],texto)

    def empresa(self,empresa):
        texto = 'Seleccione la tarea que requiera. '
        if empresa:
            texto += f'\nNombre Empresa{empresa.nombre}\n'
            texto += f'Dirección {empresa.direccion}\n'
            texto += f'Localidad {empresa.localidad}\n'
            texto += f'Provincia {empresa.provincia}\n'
            texto += f'Código Postal (CP) {empresa.CP}\n'
            texto += f'Correo Electrónico {empresa.mail}\n'
            texto += f'CIF {empresa.CIF}\n'
            print('hat empresa 4')
        return Teclado([[u"\U0001F4DD"+' Nombre',u"\U0001F4B3"+' CIF/NIF'], [u"\U0001F4CC"+' Dirección',u"\U0001F3E2"+' Población'], [u"\U0001F4EA"+' C.P.',u"\U0001F3F0"+' Provincia'], [u"\U00002709"+' EMAIL'], [u"\U0001f51d"+" Inicio",u"\U0001f519"+" Volver"]],texto)

    def configuracion(self):
        return Teclado([[u"\U0001F46B"+" Usuarios"], [u"\U0001f4cb"+" Empresa"], [u"\U0000231A"+' Horarios'],[u"\U0001f519"+" Volver"]],'Elije una opción que desee del teclado:')
    
    def config_usuarios(self):
        return Teclado([[u"\u2795"+" Añadir Usuario"], [u"\U0001f51d"+" Inicio", u"\U0001f519"+" Volver"]],'Elije una opción del menú usuarios:')
    
    def e_listado_usuarios_telegram(self,usuario_telegram):
        print('vamos con el eteclado usuarios telegram')
        teclado = []
        for l in usuario_telegram:
            print(f'Procesando usuario: {l}')
            # Cada empresa tendrá un texto y un callback_data
            if l.apellidos:
                boton = (l.nombre+' '+ l.apellidos, l.id_usuario)
            else:
                boton = (l.nombre, l.id_usuario)
            teclado.append([boton])
        texto = 'Seleccione el usuario'      
        print('eteclado terminado')
        return Teclado(teclado,texto)

    def config_usuario_seleccionado(self,usuario,telefono,apellido,administrador,dni, nss, mail, baja):
        telefono = 'Sin número' if telefono is None or telefono == 0 else str(telefono)
        apellido = '' if apellido is None or apellido == '' else apellido
        administrador2 = ' Hacer' if administrador is None or administrador == 0 else " Quitar de"
        administrador = 'No es ' if administrador is None or administrador == 0 else "Si es "
        dni = 'Sin NIF/NIE' if dni is None or dni == 0 else str(dni)
        nss = 'Sin número' if nss is None or nss == 0 else str(nss)
        mail = 'Sin Email' if mail is None or mail == '' else mail
        baja = 'Si' if baja else 'NO'
        texto = f'Usuario seleccionado:\nNombre: {usuario}\nApellido: {apellido}\nTelefono: {telefono}\n{administrador}Admimistrador.\nNIF/NIE: {dni}\nNº SS: {nss}\nEmail: {mail}\nBaja: {baja}'
        return Teclado([[u"\U0001F464"+" Nombre", u"\U0001F46A"+" Apellido"], 
                        [u"\U0001F4F1"+" Telefono", u"\U0001f9b8\u200D\u2642\uFE0F"+administrador2+" Administrador"], 
                        [u"\U0001F6C2"+" NIF/NIE", u"\U0001F4DC"+" Nº SS"],  
                        [u"\U00002709"+" Email", u"\u2796"+" Listados"], 
                        [u"\U0001F44E"+" Baja",u"\U0000231A"+' Horario'],
                        [u"\U0001f51d"+" Inicio", u"\U0001f519"+" Volver"]],texto)
    
    def add_usuario(self):
        return Teclado([[u"\U0001f519"+" Volver"]],'Envieme el contacto desde telegram.\n-Vaya al menú principal de telegram y busque el contacto.\n-Una vez en el chat de este contacto, pulse en la parte superior "Barra azul don de esta el logo y el nombre de este".\n-Pulse en el menú con los 3 puntos en vertical.\n-Seleccione compartir contacto.\nO pulse en Volver si no quiere añadir a nadie.')
    
    def listados(self,textos):
        #listadoElistados(bot,message,"Visualizar listado por pantalla:",id_empresa,id_trabajador) # esto es lo que se hace desde la funcion
        return Teclado([[u"\U0001F4C3"+' Hoy',u"\U0001F4C3"+' Ayer'],[u"\U0001f51d"+" Inicio",u"\U0001F519"+' Volver']],textos)
    
    def e_listado_listados(self):
        teclado = []
        print('e_listado_listados')
        boton = (u"\U0001F4C3"+' Hoy', "hoy")
        boton2 = (u"\U0001F4C3"+' Ayer', "ayer")
        teclado.append([boton])
        teclado.append([boton2])
        return Teclado(teclado,"Visualizar listado por pantalla:")
        
    def e_horario(self,horarios):
        teclado = []
        print('e_horario')
        for hora in horarios:
            boton = (hora.nombre+' '+str(hora.horas_dia)+'h. al día', str(hora.id_horario))
            teclado.append([boton])
        return Teclado(teclado,"Editar horario:")
        
    def horario(self,texto):
        texto = "Puede crear un horario nuevo o selecionar uno existente para su edición."
        return Teclado([[u"\U00002795"+' Crear'],[u"\U0001F519"+' Volver']],texto)
    
    def editar_horario(self,frase):
        return Teclado([[u"\U0001F3AB"+' Nombre'],[u"\U000023F3"+' Hora Inicio',u"\U0000231B"+' Hora Fin'],[u"\U000023F3"+ u"\U0000231B"+' Horas al Día',u"\U00002796"+' Eliminar'],[u"\U0001f51d"+" Inicio",u"\U0001F519"+' Volver']],frase)
