from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from core.user.models import User
from .schema import CreateUpdatePost
from .models import Post



post_router = APIRouter()

@post_router.post('/post')
def create_post(post_data: CreateUpdatePost, db:Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = Post(title=post_data.title, content=post_data.content, author_id = user.id)
    db.add(post)
    db.commit()
    return{
        "data": post_data
    }
@post_router.get('/posts')
def list_post(db:Session = Depends(get_db), user: User = Depends(get_current_user)):
    posts = db.query(Post).all()
    return{
        "data": [post.__dict__ for post in posts]
    }

@post_router.get('/post/{post_id}')
def view_post(post_id:str, db:Session= Depends(get_db), user: User=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return{
        "data": post.__dict__
    }

