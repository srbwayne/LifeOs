from fastapi import APIRouter, Depends, HTTPException, status

from app.composition_root import get_current_user_id
from app.read.application.commands.create_book import (
    CreateBookCommand,
    CreateBookCommandHandler,
)
from app.read.application.commands.create_reading_session import (
    CreateReadingSessionCommand,
    CreateReadingSessionCommandHandler,
)
from app.read.application.dtos.book_dto import BookDTO
from app.read.application.dtos.reading_progress_dto import ReadingProgressDTO
from app.read.application.dtos.reading_session_dto import ReadingSessionDTO
from app.read.application.queries.get_reading_progress import (
    GetReadingProgressQuery,
    GetReadingProgressQueryHandler,
)
from app.read.application.queries.list_my_books import (
    ListMyBooksQuery,
    ListMyBooksQueryHandler,
)
from app.read.dependencies import (
    get_create_book_handler,
    get_create_reading_session_handler,
    get_list_my_books_handler,
    get_reading_progress_handler,
)
from app.read.domain.value_objects.book_id import BookId
from app.read.presentation.api.fastapi.schemas import (
    BookResponse,
    CreateBookRequest,
    CreateReadingSessionRequest,
    ReadingProgressResponse,
    ReadingSessionResponse,
)
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


def _to_reading_session_response(session: ReadingSessionDTO) -> ReadingSessionResponse:
    return ReadingSessionResponse(
        id=session.id,
        book_id=session.book_id,
        start_page=session.start_page,
        end_page=session.end_page,
        pages_read=session.pages_read,
        started_at=session.started_at,
        ended_at=session.ended_at,
        notes=session.notes,
    )


def _to_reading_progress_response(progress: ReadingProgressDTO) -> ReadingProgressResponse:
    return ReadingProgressResponse(
        book_id=progress.book_id,
        total_pages=progress.total_pages,
        unique_pages_read=progress.unique_pages_read,
        highest_page_reached=progress.highest_page_reached,
        percentage=float(progress.percentage),
        completed=progress.completed,
    )


def _parse_book_id(value: str) -> BookId:
    try:
        return BookId.from_value(value)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid book ID.",
        ) from exc


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


@router.post(
    "/{book_id}/reading-sessions",
    response_model=ReadingSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_reading_session(
    book_id: str,
    request: CreateReadingSessionRequest,
    user_id: UserId = Depends(get_current_user_id),
    handler: CreateReadingSessionCommandHandler = Depends(get_create_reading_session_handler),
) -> ReadingSessionResponse:
    session = handler(
        CreateReadingSessionCommand(
            owner_id=user_id,
            book_id=_parse_book_id(book_id),
            start_page=request.start_page,
            end_page=request.end_page,
            started_at=request.started_at,
            ended_at=request.ended_at,
            notes=request.notes,
        )
    )
    return _to_reading_session_response(session)


@router.get(
    "/{book_id}/progress",
    response_model=ReadingProgressResponse,
)
def get_reading_progress(
    book_id: str,
    user_id: UserId = Depends(get_current_user_id),
    handler: GetReadingProgressQueryHandler = Depends(get_reading_progress_handler),
) -> ReadingProgressResponse:
    progress = handler(
        GetReadingProgressQuery(
            owner_id=user_id,
            book_id=_parse_book_id(book_id),
        )
    )
    return _to_reading_progress_response(progress)
