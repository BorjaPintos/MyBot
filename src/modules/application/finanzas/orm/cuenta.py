from sqlalchemy import Column, Text, Float, Integer

from src.persistence.infrastructure.orm.baseentity import Base


class Cuenta(Base):
    __tablename__ = 'finanzas_cuentas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Text, nullable=False)
    cantidad_base = Column(Float(precision=2))
    ponderacion = Column(Integer)
