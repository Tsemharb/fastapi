from typing import Optional
import os
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv

load_dotenv()

while True:
    try:
        host = os.getenv('HOST')
        database = os.getenv('DB')
        user = os.getenv('USER')
        password = os.getenv('PASSWORD')

        # workaround
        host = 'localhost'
        database = 'FastAPIIntro'
        user = 'postgres'
        password = '0923'

        conn = psycopg2.connect(host=host, database=database,
                                user=user, password=password,
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful!")
        break
    except Exception as error:
        print("Connecting to Database failed")
        print("Error: ", error)
        time.sleep(5)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "first post", "content": "content of first post", "id": 1},
            {"title": "second post", "content": "content of second post", "id": 2}]

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    cursor.execute("""
                        SElECT * 
                        FROM posts
                   """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""
                        INSERT INTO posts (title, content, published) 
                        VALUES (%s, %s, %s) RETURNING *
                   """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    cursor.execute("""
                    SELECT * 
                    FROM posts 
                    WHERE id = %s
                """, (str(id),))
    post = cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""
                        DELETE FROM posts
                        WHERE id = %s RETURNING *
                   """, (str(id),))
    deleted = cursor.fetchone()
    conn.commit()

    if deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""
                        UPDATE posts 
                        SET title = %s, content = %s, published = %s
                        WHERE id = %s
                        RETURNING *
                    """, (post.title, post.content, post.published, str(id)))
    updated = cursor.fetchone()
    conn.commit()
    if updated:
        return {"data": updated}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
