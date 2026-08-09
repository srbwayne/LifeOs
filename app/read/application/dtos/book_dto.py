from __future__ import annotations

from dataclasses import dataclass

from app.read.domain.aggregates.book import Book


@dataclass(frozen=True)
class BookDTO:
    id: str
    title: str
    author: str
    total_pages: int
    isbn: str | None
    publisher: str | None
    edition: str | None
    cover: str | None
    genre: str | None
    language: str | None

    @classmethod
    def from_book(cls, book: Book) -> BookDTO:
        return cls(
            id=book.id.to_persistence(),
            title=book.title,
            author=book.author,
            total_pages=book.total_pages.value,
            isbn=book.isbn,
            publisher=book.publisher,
            edition=book.edition,
            cover=book.cover,
            genre=book.genre,
            language=book.language,
        )
