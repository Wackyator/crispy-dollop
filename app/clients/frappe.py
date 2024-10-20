import logging

import httpx

from app import models


class FrappeClient:
    url = "https://frappe.io/api/method/frappe-library"

    @classmethod
    async def get_book_data(cls, **kwargs) -> list[models.FrappeAPIResponse]:
        params = kwargs
        async with httpx.AsyncClient() as client:
            response = await client.get(cls.url, params=params)
            if response.status_code == 200:
                books_json = response.json()["message"]
                books: list[models.FrappeAPIResponse] = []
                for book in books_json:
                    try:
                        books.append(models.FrappeAPIResponse(**book))
                    except Exception:
                        logging.error(f"Ignore entry with bookID: {book["bookID"]}")
                return books
            raise Exception(
                f"Failed to get books data from frappe API with HTTP status_code: {response.status_code}"
            )
