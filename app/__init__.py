import logging
from typing import Any
from fastapi import FastAPI, Request
import httpx
from app import api

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.include_router(api.router)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> Any:
    data = {
        "app_name": "LibMS",
        "request": request,
        "options": [
            {"name": "All Books", "link": "/books"},
            {"name": "Members", "link": "/members"},
            {"name": "Library", "link": "/library"},
        ],
    }

    logging.error(api.v1.books.router.url_path_for("get_books"))
    return templates.TemplateResponse("index.html", context=data)


@app.get("/books", response_class=HTMLResponse)
async def all_books(request: Request) -> Any:
    data = {
        "app_name": "LibMS",
        "request": request,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/api/v1/books/")
        if response.status_code == 200:
            data["books"] = response.json()
            return templates.TemplateResponse("books.html", context=data)

    return templates.TemplateResponse("error.html", context=data)


@app.get("/books/create", response_class=HTMLResponse)
async def create_book(request: Request) -> Any:
    data = {
        "app_name": "LibMS",
        "request": request,
    }

    return templates.TemplateResponse("book_create.html", context=data)


@app.get("books/edit/{book_id}", response_class=HTMLResponse)
async def edit_book(request: Request, book_id: int) -> Any:
    data = {
        "app_name": "LibMS",
        "request": request,
        "id": book_id,
    }

    return templates.TemplateResponse("book_edit.html", context=data)


@app.get("/books/{book_id}", response_class=HTMLResponse)
async def single_book(request: Request, book_id: int) -> Any:
    data = {
        "app_name": "LibMS",
        "request": request,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/api/v1/books/{book_id}")
        if response.status_code == 200:
            data["books"] = [response.json()]
            return templates.TemplateResponse("books.html", context=data)

    return templates.TemplateResponse("error.html", context=data)


@app.get("/members", response_class=HTMLResponse)
async def members(request: Request) -> Any:
    data = {
        "app_name": "LibMS",
        "request": request,
    }

    return templates.TemplateResponse("members.html", context=data)


@app.get("/library", response_class=HTMLResponse)
async def library(request: Request) -> Any:
    data = {
        "app_name": "LibMS",
        "request": request,
    }

    return templates.TemplateResponse("members.html", context=data)
