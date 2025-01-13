from datetime import datetime

from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, Text, Date
from sqlalchemy.orm import relationship


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    rating_id = Column(Integer, ForeignKey('ratings.id'))
    comment = Column(Text)
    comment_date = Column(Date(), default=datetime.today())
    is_active = Column(Boolean, default=True)

    products = relationship('Product', back_populates='reviews')
    rating = relationship('Rating', back_populates='review')