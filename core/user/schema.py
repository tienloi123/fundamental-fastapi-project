from pydantic import BaseModel,Field
from pydantic.generics import GenericModel
from typing import Generic,Optional,TypeVar

T = TypeVar('T')

class ResponseSchema(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None

class UserCreate(BaseModel):
    username:str
    email:str
    password:str

class UserLogin(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class ProductSchema(BaseModel):
    id: int
    name: str
    title: str
    description: str
    price: float
    stock_quantity: int

    class Config:
        orm_mode = True
class RequestProduct(BaseModel):
    parameter: ProductSchema = Field(...)
class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
