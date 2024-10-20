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
            {"name": "Create Book", "link": "/books/create"},
            {"name": "All Members", "link": "/members"},
            {"name": "Create Member", "link": "/members/create"},
            {"name": "Loan Book", "link": "/library/loan"},
            {"name": "Return Book", "link": "/library/return"},
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


@app.get("/books/{book_id}/edit", response_class=HTMLResponse)
async def edit_book(request: Request, book_id: int) -> Any:
    data = {
        "app_name": "LibMS",
        "request": request,
        "member_id": book_id,
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
async def all_members(request: Request) -> Any:
    data = {
        "app_name": "LibMS",
        "request": request,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/api/v1/members/")
        if response.status_code == 200:
            data["members"] = response.json()
            return templates.TemplateResponse("members.html", context=data)
    return templates.TemplateResponse("error.html", context=data)


@app.get("/members/create", response_class=HTMLResponse)
async def create_member(request: Request) -> Any:
    data = {
        "app_name": "LibMS",
        "request": request,
    }

    return templates.TemplateResponse("member_create.html", context=data)


@app.get("/members/{member_id}/edit", response_class=HTMLResponse)
async def edit_member(request: Request, member_id: int) -> Any:
    data = {
        "app_name": "LibMS",
        "request": request,
        "member_id": member_id,
    }

    return templates.TemplateResponse("member_edit.html", context=data)


@app.get("/members/{member_id}", response_class=HTMLResponse)
async def single_member(request: Request, member_id: int) -> Any:
    data = {
        "app_name": "LibMS",
        "request": request,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/api/v1/members/{member_id}")
        if response.status_code == 200:
            data["members"] = [response.json()]
            return templates.TemplateResponse("members.html", context=data)
    return templates.TemplateResponse("error.html", context=data)


@app.get("/library/loan", response_class=HTMLResponse)
async def loan_book(request: Request) -> Any:
    data = {
        "app_name": "LibMS",
        "request": request,
    }

    return templates.TemplateResponse("loan_book.html", context=data)


@app.get("/library/return", response_class=HTMLResponse)
async def return_book(request: Request) -> Any:
    data = {
        "app_name": "LibMS",
        "request": request,
    }

    return templates.TemplateResponse("return_book.html", context=data)
