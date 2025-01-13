from datetime import datetime

from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, Text, Date
from sqlalchemy.orm import relationship


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, index=True)
    grade = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    is_active = Column(Boolean, default=True)

    review = relationship('Review', back_populates='rating')