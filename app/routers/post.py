from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import utils

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# @router.get("/", response_model=list[schemas.PostResponse])
@router.get("/", response_model=list[schemas.PostResponsewithVotes])
def get_posts(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0,
              search: Optional[str] = ""):

    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip)
    postswithVotes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return postswithVotes


# @router.get("/{id}", response_model=schemas.PostResponse)
@router.get("/{id}", response_model=schemas.PostResponsewithVotes)
def get_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id ==
                                        id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id: {id} is not found")

    postwithVotes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(models.Post.id == id).group_by(models.Post.id).first()

    return postwithVotes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    print(current_user.email)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id: {id} is not found")
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform this action")
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    print(current_user.email)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id: {id} is not found")
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform this action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
