from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session 
from .. import models, schemas, oauth2
from ..database import get_db
from typing import Optional, List
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)



#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, 
              search: Optional[str] = "" ): #limit param for quering/pagination
    print(search)
    #posts=db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    #   1. Search = "LIKE", 2. Limit = "LIMIT" 3. Skip = "Offset"
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts #fastapi serializes an array to return json


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, 
    #                        content = post.content, 
    #                        published = post.published)
    #print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #SQL: returning *
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, 
             db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)): #fastpi makes typecasting a validator and converts datatype
    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    #print(post.owner_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Not authorized to perform requested action")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if (post := post_query.first()) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} DNE")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return  Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):  
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if (postq := post_query.first()) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} DNE")
    if postq.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
