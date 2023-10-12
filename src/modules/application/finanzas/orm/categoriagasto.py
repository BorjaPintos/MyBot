from sqlalchemy import Column, Text, Integer
from src.persistence.infrastructure.orm.baseentity import Base


class CategoriaGasto(Base):
    __tablename__ = 'finanzas_categorias_gasto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(Text, nullable=False)
    cuenta_cargo_defecto = Column(Integer)
