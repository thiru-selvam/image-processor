from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, text, Text
from sqlalchemy.orm import relationship

from .database import Base


class Request(Base):
    __tablename__ = 'requests'
    id = Column(name='id', type_=String, primary_key=True, index=True)
    status = Column(name='status', type_=String, default='pending')
    created_on = Column(name='created_at', type_=DateTime(timezone=True), server_default=text('Now()'))
    updated_on = Column(name='updated_at', type_=DateTime(timezone=True),
                        server_default=text('Now()'), server_onupdate=text('Now()'))
    products = relationship('Product', back_populates='request')


class Product(Base):
    __tablename__ = 'products'
    id = Column(name='id', type_=Integer, primary_key=True, index=True, nullable=False)
    requests_id = Column(ForeignKey(column='requests.id', ondelete="CASCADE"), name='user_uid', type_=String,
                         nullable=False)
    product_name = Column(name='product_name', type_=String, index=True)
    images = relationship('Image', back_populates='product')
    request = relationship('Request', back_populates='products')


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    img_data = Column(name='processed_img_data', type_=Text, index=True)
    # input_url = Column(String, index=True)
    # output_url = Column(String, nullable=True, index=True)
    status = Column(String, default='pending')
    product = relationship('Product', back_populates='images')
