from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import User
from dependencies import get_db
from .schema import UserCreate, UserLogin, Token,RequestProduct,Response,ResponseSchema
from . import crud


user_router = APIRouter()


@user_router.post('/signup')
def signup(user_data: UserCreate, db:Session = Depends(get_db)):
    user = User(username=user_data.username, email=user_data.email)
    user.password=user.hashed_password(user_data.password)
    db.add(user)
    db.commit()
    return{
        "message": "User has been created"
    }
@user_router.post('/login')
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if user is None or not user.verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, default="Invalide Credentials")
    token = user.generate_token()
    return Token(access_token=token,token_type='bearer')
pro_router = APIRouter()

@pro_router.post("/create")
async def create_product_service(request: RequestProduct, db: Session = Depends(get_db)):
    crud.create_product(db, product=request.parameter)
    return Response(status="Ok", code="200", message="product created successfully", result={}).dict(exclude_none=True)



@pro_router.get("/")
async def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _products = crud.get_product(db, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_products)

@pro_router.patch("/update")
async def update_product(request: RequestProduct, db: Session = Depends(get_db)):
    _product = crud.update_product(
        db,
        product_id=request.parameter.id,
        product=request.parameter
    )
    return Response(
        status="Ok",
        code="200",
        message="Success update data",
        result=_product
    ).dict(exclude_none=True)



@pro_router.delete("/delete")
async def delete_product(request: RequestProduct,  db: Session = Depends(get_db)):
    crud.remove_product(db, product_id=request.parameter.id)
    return ResponseSchema(code="200", status="Ok", message="Success delete data", result={})