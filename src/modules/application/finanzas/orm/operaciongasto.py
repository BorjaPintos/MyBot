from sqlalchemy import Column, Date, Float, Text, Integer
from src.persistence.infrastructure.orm.baseentity import Base


class OperacionGasto(Base):
    __tablename__ = 'finanzas_operaciones_gasto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    cantidad = Column(Float(precision=2), nullable=False)
    descripcion = Column(Text, nullable=False)
    categoria_gasto = Column(Integer, nullable=False)
    cuenta_cargo = Column(Integer, nullable=False)
