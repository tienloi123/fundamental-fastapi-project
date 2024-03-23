from sqlalchemy import Column, Float, ForeignKey, Integer, String, Boolean, DateTime
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from sqlalchemy.dialects.postgresql import UUID
from config import get_settings
import uuid
import jwt
from sqlalchemy.sql import func
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    payments = relationship("Payment", back_populates="user")
    orders = relationship("Order", back_populates="user")
    

    def hashed_password(self, password: str):
        return pwd_context.hash(password)
    
    def verify_password(self, password: str,hashed_password):
        return pwd_context.verify(password,hashed_password )
    
    def generate_token(self):
        expiration = datetime.utcnow() + timedelta(hours=24)
        payload = {
            "sub": str(self.id),
            "exp": expiration
        }
        return jwt.encode(payload,f"{get_settings().SECRET_KEY}",algorithm="HS256")

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)
    orders = relationship("Order", back_populates="product")

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    amount = Column(Float)
    status = Column(String)
    payment_method = Column(String)

    user = relationship("User", back_populates="payments")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    total_price = Column(Float)
    order_date = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")