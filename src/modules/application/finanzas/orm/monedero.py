from sqlalchemy import Column, Text, Integer, Float
from sqlalchemy.orm import column_property

from src.persistence.infrastructure.orm.baseentity import BaseEntity


class Monedero(BaseEntity):
    __tablename__ = 'finanzas_monederos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Text, nullable=False)
    cantidad_base = Column(Float(precision=2), nullable=False)
    diferencia = Column(Float(precision=2), server_default="0.00", nullable=False)
    total = column_property(cantidad_base + diferencia)

