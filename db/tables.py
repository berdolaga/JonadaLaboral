# db/tables.py

# Proyecto desarrollado como parte del Trabajo de Fin de Grado (TFG)
# Curso de Adaptación al Grado en Ingeniería Informática - UNIR
# Autor: [Alberto Toledo Escrihuela]
# Año: 2025

from unicodedata import numeric
from sqlalchemy import create_engine, Numeric, Column, Integer, String, Boolean, Date, BLOB, Time, Text, ForeignKey, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from config import config

print('Cargando Servicios BD...')

# Usando SQLite
engine = create_engine(config.DATABASE_URL)#, echo=True) #, echo=True para ver las sql generadas asi controlar la depuracion

@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

Base = declarative_base()

class UserDB(Base):
    __tablename__ = 'usuarios'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    id_telegram = Column(Integer, nullable=False)    
    nombre = Column(String)
    apellidos = Column(String)
    dni = Column(String)
    n_ss = Column(String)
    mail = Column(String)
    telefono = Column(String)
    trabajando = Column(Integer, nullable=True, default=0)
    pausado = Column(Integer, nullable=True, default=0)
    menu = Column(String)
    eteclat = Column(String)
    id_usuario_temp = Column(Integer, nullable=True)
    id_horario_temp = Column(Integer, nullable=True)
    administrador = Column(Boolean, nullable=True, default=False)
    baja = Column(Integer, default=0)

class EmpresaDB(Base):
    __tablename__ = 'empresa'

    id_empresa = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    direccion = Column(String, nullable=True)
    localidad = Column(String, nullable=True)
    provincia = Column(String, nullable=True)
    mail = Column(String, nullable=True)
    CIF = Column(String, nullable=True)
    CP = Column(Integer, nullable=True)

class FichajeDB(Base):
    __tablename__ = 'fichaje'

    id_fichaje = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario= Column(Integer, nullable=False)    
    fecha = Column(Date)
    hora_entrada = Column(String)
    hora_salida = Column(String)
    pausa = Column(Integer, default=0, nullable=True)


class HorarioDB(Base):
    __tablename__ = 'horario'

    id_horario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    inicio = Column(String)
    fin = Column(String)
    horas_dia = Column(Integer, default=0)
    

class Usuario_HorarioDB(Base):
    __tablename__ = 'usuario_horario'

    id_usuario_horario = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer)
    id_horario = Column(Integer)
    

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()

print('Servicio para SQLite iniciado')

## resto de bases de datos si fuera necesario

print('Servicios BD cargados.')
