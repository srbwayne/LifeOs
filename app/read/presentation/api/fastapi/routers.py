from fastapi import APIRouter, Depends, status

from app.composition_root import get_current_user_id
from app.read.application.commands.create_book import (
    CreateBookCommand,
    CreateBookCommandHandler,
)
from app.read.application.dtos.book_dto import BookDTO
from app.read.application.queries.list_my_books import (
    ListMyBooksQuery,
    ListMyBooksQueryHandler,
)
from app.read.dependencies import get_create_book_handler, get_list_my_books_handler
from app.read.presentation.api.fastapi.schemas import BookResponse, CreateBookRequest
from app.shared.domain.identifiers.user_id import UserId

router = APIRouter(prefix="/books", tags=["Reading Library"])


def _to_response(book: BookDTO) -> BookResponse:
    return BookResponse(
        id=book.id,
        title=book.title,
        author=book.author,
        total_pages=book.total_pages,
        isbn=book.isbn,
        publisher=book.publisher,
        edition=book.edition,
        cover=book.cover,
        genre=book.genre,
        language=book.language,
    )


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    request: CreateBookRequest,
    user_id: UserId = Depends(get_current_user_id),
    handler: CreateBookCommandHandler = Depends(get_create_book_handler),
) -> BookResponse:
    book = handler(
        CreateBookCommand(
            owner_id=user_id,
            title=request.title,
            author=request.author,
            total_pages=request.total_pages,
            isbn=request.isbn,
            publisher=request.publisher,
            edition=request.edition,
            cover=request.cover,
            genre=request.genre,
            language=request.language,
        )
    )
    return _to_response(book)


@router.get("", response_model=list[BookResponse])
def list_my_books(
    user_id: UserId = Depends(get_current_user_id),
    handler: ListMyBooksQueryHandler = Depends(get_list_my_books_handler),
) -> list[BookResponse]:
    books = handler(ListMyBooksQuery(owner_id=user_id))
    return [_to_response(book) for book in books]
