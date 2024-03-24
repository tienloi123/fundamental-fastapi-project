from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import User
from core.user.order.order import create_order
from dependencies import get_db
from .schema import UserCreate, UserLogin, Token,RequestProduct,Response,ResponseSchema,OrderCreateSchema
from . import crud
from core.user.payment import PaymentRepo


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

order_router = APIRouter()

@order_router.post("/orders/")
async def create_order_route(order_data: OrderCreateSchema, db: Session = Depends(get_db)):
    try:
        order = create_order(db, user_id=order_data.user_id, product_id=order_data.product_id, quantity=order_data.quantity)
        PaymentRepo.update_payment_status(db, order.id, "pending")
        return {"message": "Order created successfully", "order": order}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))