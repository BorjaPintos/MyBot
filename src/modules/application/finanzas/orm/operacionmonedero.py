from sqlalchemy import Column, Date, Float, Text, Integer
from src.persistence.infrastructure.orm.baseentity import BaseEntity


class OperacionMonederoo(BaseEntity):
    __tablename__ = 'finanzas_operaciones_monedero'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    cantidad = Column(Float(precision=2), nullable=False)
    descripcion = Column(Text, nullable=False)
    monedero_origen = Column(Integer, nullable=False)
    monedero_destino = Column(Integer, nullable=False)
