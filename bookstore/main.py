from typing import Literal, Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
import random
import json
import os

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


router = FastAPI()

class Book(BaseModel):
    name: str
    price: float
    genre: Literal['Horror', 'Romance', 'Fiction', 'Fantasy', 'Cooking']
    author: str
    book_id: Optional[str] = uuid4().hex

book_file = "book.json"

book_database = []



if os.path.exists(book_file):
    with open(book_file, 'r') as f:
        book_database = json.load(f)


@router.get("/")
async def home():
    return "Welcome to the bookstore"


@router.get("/list-books")
async def list_books():
    return {"Book" : book_database}


@router.get("/list-books-by-index/{index}")
async def list_books_by_id(index:int):

    try:
        return {"Book" : book_database[index]}
    except:
        raise HTTPException(404, "Index not found")
    

@router.get("/list-books-random")
async def list_books_random():

    return {"Book" : random.choice(book_database)}

@router.post("/create-books/")
async def create_books(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    book_database.append(json_book)
    with open (book_file, 'w') as f:
        json.dump(book_database, f)

    return {"Added book: " , book.name}

@router.delete("/delete-books/{index}")
async def delete_books(index:int):

    book_database.pop(index)

    return {"Deleted book: ", book_database.pop(index)}

@router.put("/update-books/{index}")
async def update_books(book: Book):

    book_database[book.book_id] = book.name

    return {"Updated book: ", "this book: {book_database[book.book_id]} was updated."}
