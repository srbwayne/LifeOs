from __future__ import annotations

from dataclasses import dataclass

from app.read.domain.errors.book_errors import (
    InvalidBookAuthorError,
    InvalidBookTitleError,
)
from app.read.domain.value_objects.book_id import BookId
from app.read.domain.value_objects.total_pages import TotalPages
from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.identifiers.user_id import UserId


@dataclass(eq=False)
class Book(AggregateRoot):
    id: BookId
    owner_id: UserId
    title: str
    author: str
    total_pages: TotalPages
    isbn: str | None = None
    publisher: str | None = None
    edition: str | None = None
    cover: str | None = None
    genre: str | None = None
    language: str | None = None

    @classmethod
    def create(
        cls,
        owner_id: UserId,
        title: str,
        author: str,
        total_pages: int,
        isbn: str | None = None,
        publisher: str | None = None,
        edition: str | None = None,
        cover: str | None = None,
        genre: str | None = None,
        language: str | None = None,
    ) -> Book:
        return cls._build(
            id=BookId.new(),
            owner_id=owner_id,
            title=title,
            author=author,
            total_pages=TotalPages(total_pages),
            isbn=isbn,
            publisher=publisher,
            edition=edition,
            cover=cover,
            genre=genre,
            language=language,
        )

    @classmethod
    def restore(
        cls,
        id: BookId,
        owner_id: UserId,
        title: str,
        author: str,
        total_pages: TotalPages,
        isbn: str | None = None,
        publisher: str | None = None,
        edition: str | None = None,
        cover: str | None = None,
        genre: str | None = None,
        language: str | None = None,
    ) -> Book:
        if not isinstance(id, BookId):
            raise TypeError("Book ID must be a BookId.")
        if not isinstance(total_pages, TotalPages):
            raise TypeError("Book total pages must be a TotalPages.")
        return cls._build(
            id=id,
            owner_id=owner_id,
            title=title,
            author=author,
            total_pages=total_pages,
            isbn=isbn,
            publisher=publisher,
            edition=edition,
            cover=cover,
            genre=genre,
            language=language,
        )

    @classmethod
    def _build(
        cls,
        id: BookId,
        owner_id: UserId,
        title: str,
        author: str,
        total_pages: TotalPages,
        isbn: str | None,
        publisher: str | None,
        edition: str | None,
        cover: str | None,
        genre: str | None,
        language: str | None,
    ) -> Book:
        if not isinstance(owner_id, UserId):
            raise TypeError("Book owner must be a UserId.")
        return cls(
            id=id,
            owner_id=owner_id,
            title=cls._normalize_title(title),
            author=cls._normalize_author(author),
            total_pages=total_pages,
            isbn=cls._normalize_optional(isbn, "isbn"),
            publisher=cls._normalize_optional(publisher, "publisher"),
            edition=cls._normalize_optional(edition, "edition"),
            cover=cls._normalize_optional(cover, "cover"),
            genre=cls._normalize_optional(genre, "genre"),
            language=cls._normalize_optional(language, "language"),
        )

    @staticmethod
    def _normalize_title(value: str) -> str:
        if not isinstance(value, str) or not (normalized := value.strip()):
            raise InvalidBookTitleError()
        return normalized

    @staticmethod
    def _normalize_author(value: str) -> str:
        if not isinstance(value, str) or not (normalized := value.strip()):
            raise InvalidBookAuthorError()
        return normalized

    @staticmethod
    def _normalize_optional(value: str | None, field_name: str) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError(f"Book {field_name} must be a string or None.")
        return value.strip() or None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        raise TypeError("unhashable type: 'Book'")
