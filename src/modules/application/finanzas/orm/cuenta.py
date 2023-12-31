from sqlalchemy import Column, Text, Float, Integer
from sqlalchemy.orm import column_property

from src.persistence.infrastructure.orm.baseentity import BaseEntity


class Cuenta(BaseEntity):
    __tablename__ = 'finanzas_cuentas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Text, nullable=False)
    cantidad_base = Column(Float(precision=2), nullable=False)
    diferencia = Column(Float(precision=2), server_default="0.00", nullable=False)
    total = column_property(cantidad_base+diferencia)
    ponderacion = Column(Integer)
