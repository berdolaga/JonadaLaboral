#adapters/diccionarios.py

# Proyecto desarrollado como parte del Trabajo de Fin de Grado (TFG)
# Curso de Adaptación al Grado en Ingeniería Informática - UNIR
# Autor: [Alberto Toledo Escrihuela]
# Año: 2025

def diccionari(dic):
    #print ("dentro del diccionari")
    diccionarios = {
        #"iconos" : generaiconos(),
        "operacion" : operacion()
    }
    #print ("diccionarios creados")
    if dic in diccionarios:
        #print ("return el diccionario")
        return diccionarios[dic]
    
def esta(dic,clave):
    if clave in diccionari(dic):
        return True
    else:
        return False

def devuelve(dic,clave):
    if clave in diccionari(dic):
        return diccionari(dic)[clave]
    else:
        if dic == 'operacion': #en el caso de no haber key que buscamos
            print(f'no existe la key: {clave}')
            return 'inicio'
        else:
            None #deberia devolver el valor por defecto del diccionario operacion u otros creados


def operacion():
    #print ("operacion")
    return{
    "Inicio"                                          :'inicio',
    "Inicio Empleado"                                 :'inicioE',
    "Fichar"                                          :'fichar',
    "Empresa"                                         :'empresa',
    "Empresa nombre"                                  :'empresa_nombre',
    "Empresa cif"                                     :'empresa_cif',
    "Empresa direccion"                               :'empresa_direccion',
    "Empresa poblacion"                               :'empresa_localidad',
    "Empresa cp"                                      :'empresa_cp',
    "Empresa provincia"                               :'empresa_provincia',
    "Empresa mail"                                    :'empresa_mail',
    "Configuración"                                   :'configuracion',
    "Configuración Horario"                           :'configuracion_horario',
    "Crear Horario"                                   :'configuracion_horario',
    "Horario"                                         :'horario',
    "Nombre Horario"                                  :'horario_cambiar',
    "Inicio Horario"                                  :'horario_cambiar',
    "Fin Horario"                                     :'horario_cambiar',
    "Horas Horario"                                   :'horario_cambiar',
    "Configuración Usuarios"                          :'configuracion_usuarios',
    "Configuración Usuario Seleccionado"              :'configuracion_usuario_seleccionado',
    "Configuración Usuario Nombre"                    :'configuracion_usuario_cambiar',
    "Configuración Usuario Apellido"                  :'configuracion_usuario_cambiar',
    "Configuración Usuario Telefono"                  :'configuracion_usuario_cambiar',
    "Configuración Usuario CIF"                       :'configuracion_usuario_cambiar',
    "Configuración Usuario SS"                        :'configuracion_usuario_cambiar',
    "Configuración Usuario Mail"                      :'configuracion_usuario_cambiar',
    "Configuración Usuario Baja"                      :'configuracion_usuario_baja',
    "Configuración Usuario Horario"                   :'configuracion_usuario_horario',
    "Configuración Usuario Listados"                  :'listado_usuario',
    "Añadir Usuario"                                  :'add_usuario',
    "Listado Empleado"                                :'listado_empleado'
    }
