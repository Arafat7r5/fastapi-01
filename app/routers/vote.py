from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .. import models, schemas, oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import utils

router = APIRouter(
    prefix="/votes",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(data: schemas.Vote, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == data.post_id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id: {data.post_id} is not found")

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == data.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (data.vote_dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {data.post_id}")
        new_vote = models.Vote(post_id=data.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        db.delete(found_vote)
        db.commit()
        return {"message": "successfully deleted vote"}
