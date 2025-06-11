# application/listados.py

# Proyecto desarrollado como parte del Trabajo de Fin de Grado (TFG)
# Curso de Adaptación al Grado en Ingeniería Informática - UNIR
# Autor: [Alberto Toledo Escrihuela]
# Año: 2025

from datetime import date, datetime, timedelta
from application.user_servicios_inicializar import user_port, fichar_port, empresa_port, usuario_horario_port, horario_port


def convertirTexto(textos):
    #texto = textos.decode('utf-8')
    texto = textos
    texto = texto.encode('ascii','xmlcharrefreplace')
    #print('texto convertido')
    return str(texto)


fecha = date.today().strftime("%d/%m/%Y")
print (fecha)

def dia(id_trabajador,fecha=None):
    trabajador = user_port.get_user_by_id(id_trabajador)
    empresa = empresa_port.get_by_id(1)
    nempresa = empresa.nombre
    print(f'fecha: {fecha}')
    if fecha is None:
        fecha = date.today()#.strftime("%d/%m/%Y")
        texto2 = 'Listado de hoy '
    else:
        texto2 = 'Listado del dia: '
        fechax = fecha[0]
        fecha = fechax
    #fecha2 = fecha[0]
    print(fecha)
    fecha2 = fecha.strftime("%d/%m/%Y")
    print(fecha2)
    texto2 += fecha2+':\n'
    #fecha2 = fecha.strftime("%d/%m/%Y")
    #fecha = "14/04/2020"
    print(texto2)
    print(id_trabajador)
    print(trabajador.nombre)
    print(fecha)
    if trabajador:
        if trabajador.apellidos is not None:
            traba = trabajador.nombre+" "+trabajador.apellidos
        else:
            traba = trabajador.nombre
        texto = '<!DOCTYPE html><html lang="es"><body><strong>Horario Trabajador: "'+traba+'" <br>Empresa: "'+nempresa+'" <br>Fecha: "'+ fecha2+'"</strong><br><br>'
        print(texto)
        texto2 += 'Entrada || Salida || Total || Tipo\n'
        #texto2 += 'Hora  || Total || Tipo\n'
        print('antes de horas')
        horas = fichar_port.get_by_id_user_fecha(id_trabajador,fecha)
        print('despues de horas')
        #print(f'horas: {horas[0].fecha}')
        print(f'horas: {horas}')
        if horas:
            trabajando = False
            texto += '<table cellpadding="1" cellspacing="1" border="1%" text-align="left" frame="border" rules="all">'
            texto += "<tr>"
            texto += "<td>Fecha del fichaje </td><td>tipo fichaje </td><td>Hora Entrada</td><td>Hora Salida</td><td>Horas trabajadas</td>"
            texto += "<tr>"
            total = timedelta(days=0,hours=0,minutes=0,seconds=0)
            parcial = 0
            parciales = "0:00"
            entrada = datetime.strptime("23:59", "%H:%M")#deberia ser una variable global para que fuera la jornada maxima del dia para ese trabajador.
            hora = "0:00"
            for t in horas:
                print ("t0 "+t.hora_entrada)
                print ("t1 "+t.hora_salida)
                if t.hora_entrada in [None, '', '0', '00:00']:
                    if t.hora_salida:
                        date_object = datetime.strptime(t.hora_salida, "%H:%M") 
                        parcial = date_object-entrada
                        total += parcial
                        #print ("parcial: "+str(parcial))
                        parciales = ':'.join(str(parcial).split(':')[:2])
                        #print ("parcial con formato: "+parciales)
                        hora = str(t.hora_salida)
                        trabajando = False
                    else:
                        print("Error: hora_salida es inválida para t.hora_entrada == '0'")
                        continue
                else:
                    entrada = datetime.strptime(t.hora_entrada, "%H:%M")
                    parciales = "0:00"
                    #print ("hora entrada "+str(entrada))
                    hora = str(t.hora_entrada)
                    trabajando = True
                if t.pausa == 1:
                    if t.hora_entrada != '':
                        tipo = "Fin Pausa"
                        trabajando = True
                    else:
                        tipo = "Ini. Pausa"
                        trabajando = False
                else: 
                    tipo = "Marcaje"
                texto += "<tr>"
                texto += "<td>"+str(fecha)+"</td><td>"+str(tipo)+"</td><td>"+str(t.hora_entrada)+"</td><td>"+str(t.hora_salida)+"</td><td>"+str(parciales)+"</td>"
                texto += "<tr>"    
                entra = str(t.hora_entrada) if t.hora_entrada else '  0:00' 
                sali = str(t.hora_salida) if t.hora_salida else '  0:00' 

                texto2 += entra+"    || "+sali+"   || "+str(parciales)+" || "+str(tipo)+"\n"   
                #texto2 += str(hora)+" || "+str(parciales)+" || "+str(tipo)+"\n"     
                print(texto2)                  
            texto += "<tr>"
            texto += "<td>Total horas: </td><td> </td><td></td><td></td><td><strong>"+':'.join(str(total).split(':')[:2])+"</strong></td>"
            texto += "<tr>"
            texto += "</table>"
            print(f'trabajando: {trabajando}')
            #if str(total)=="0:00:00":
            if trabajando:
                hora_salida = datetime.strptime(str(datetime.now().hour)+":"+str(datetime.now().minute),"%H:%M")
                total = hora_salida-entrada
                texto2 += "Total horas de momento: "+':'.join(str(total).split(':')[:2])+'\n'
            else:
                texto2 += "Total horas finalizadas: "+':'.join(str(total).split(':')[:2])+'\n'
            print ("total: "+str(total))
            usu_horario = usuario_horario_port.get_by_id_user(id_trabajador)
            if usu_horario:
                horario = horario_port.get_by_id(usu_horario.id_horario)
                if horario:
                    int_dia = int(horario.horas_dia)
                    dia = timedelta(hours=int_dia)
                    if dia < total:
                        extras = total-dia
                        texto += '<p>Horas Extra: '+':'.join(str(extras).split(':')[:2])+'</p>'
                        texto2 += 'Horas Extra: '+':'.join(str(extras).split(':')[:2])+'\n'
            texto += '</body></html>'
            print(texto)
            return texto, texto2
        else:
            return None, None
    else:
        return False

def hoy(id_trabajador):
    return dia(id_trabajador)

def ultimoDiaTrabajado(id_trabajador):
    hoy = date.today()
    print(hoy)
    ayer = fichar_port.get_by_id_user_fecha_penultima(id_trabajador,hoy)
    print('hooo')
    print(f'Ayer: {ayer}')
    if ayer:
        #ayer = ayer.strftime("%d/%m/%Y")
        print (str(ayer))
        return ayer
    else:
        return False

def ayer(id_trabajador):
    fecha=ultimoDiaTrabajado(id_trabajador)
    if fecha:
        return dia(id_trabajador,fecha)
    else:
        return dia(id_trabajador)
