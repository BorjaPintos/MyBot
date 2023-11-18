from sqlalchemy import Column, Text, Integer

from src.persistence.infrastructure.orm.baseentity import BaseEntity


class CategoriaIngreso(BaseEntity):
    __tablename__ = 'finanzas_categorias_ingreso'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(Text, nullable=False)
    cuenta_abono_defecto = Column(Integer)
    monedero_defecto = Column(Integer)
