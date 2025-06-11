# application/user_servicio_inicializar.py

# Proyecto desarrollado como parte del Trabajo de Fin de Grado (TFG)
# Curso de Adaptación al Grado en Ingeniería Informática - UNIR
# Autor: [Alberto Toledo Escrihuela]
# Año: 2025

from ports.usuario_ports import UserPort
from ports.empresa_ports import EmpresaPort
from ports.horario_ports import HorarioPort
from ports.usuario_horario_ports import UsuarioHorarioPort
from ports.fichaje_ports import FichajePort

from ports.teclado_ports import TecladoPort

from adapters.user_adapter import UserAdapter
from adapters.empresa_adapter import EmpresaAdapter
from adapters.horarios_adapter import HorarioAdapter
from adapters.usuario_horario_adapter import UsuarioHorarioAdapter
from adapters.fichaje_adapter import FichajeAdapter

from adapters.teclado_adapter import TecladoAdapter


user_repositorio = UserAdapter()
empresa_repositorio = EmpresaAdapter()
horario_repositorio = HorarioAdapter()
usuario_horario_repositorio = UsuarioHorarioAdapter()
fichaje_repositorio = FichajeAdapter()

teclado_repositorio = TecladoAdapter()

user_port = UserPort(user_repositorio)
empresa_port = EmpresaPort(empresa_repositorio)
horario_port = HorarioPort(horario_repositorio)
usuario_horario_port = UsuarioHorarioPort(usuario_horario_repositorio)
fichar_port = FichajePort(fichaje_repositorio)

teclado_port = TecladoPort(teclado_repositorio)
