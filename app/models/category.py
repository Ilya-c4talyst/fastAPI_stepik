# import os
# import sys
# sys.path.append(os.getcwd())

from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.products import Product
from app.models.rating import Rating
from app.models.review import Review
from app.models.user import User

class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = {'extend_existing': True} 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)  # New

    products = relationship("Product", back_populates="category")  # New

from sqlalchemy.schema import CreateTable
print(CreateTable(Product.__table__))
print(CreateTable(Category.__table__))
print(CreateTable(User.__table__))
print(CreateTable(Rating.__table__))
print(CreateTable(Review.__table__))