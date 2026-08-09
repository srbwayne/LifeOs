from app.read.domain.aggregates.book import Book
from app.read.domain.value_objects.book_id import BookId
from app.read.domain.value_objects.total_pages import TotalPages
from app.read.infrastructure.persistence.mappers.book_mapper import BookMapper
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.shared.domain.identifiers.user_id import UserId


def test_mapper_converts_all_book_fields_to_persistence() -> None:
    book = Book.create(
        owner_id=UserId.new(),
        title="Book",
        author="Author",
        total_pages=300,
        isbn="isbn",
        publisher="publisher",
        edition="edition",
        cover="cover",
        genre="genre",
        language="language",
    )

    model = BookMapper.to_persistence(book)

    assert model.id == book.id.to_persistence()
    assert model.user_id == book.owner_id.to_persistence()
    assert model.title == book.title
    assert model.author == book.author
    assert model.total_pages == book.total_pages.value
    assert model.isbn == book.isbn
    assert model.publisher == book.publisher
    assert model.edition == book.edition
    assert model.cover == book.cover
    assert model.genre == book.genre
    assert model.language == book.language


def test_mapper_preserves_absent_optional_fields() -> None:
    book = Book.create(UserId.new(), "Book", "Author", 100)

    model = BookMapper.to_persistence(book)
    restored = BookMapper.to_domain(model)

    assert restored.isbn is None
    assert restored.publisher is None
    assert restored.edition is None
    assert restored.cover is None
    assert restored.genre is None
    assert restored.language is None


def test_mapper_restores_identity_owner_total_pages_and_no_events() -> None:
    book_id = BookId.new()
    owner_id = UserId.new()
    model = BookModel(
        id=book_id.to_persistence(),
        user_id=owner_id.to_persistence(),
        title="Restored Book",
        author="Restored Author",
        total_pages=250,
        isbn="isbn",
        publisher="publisher",
        edition="edition",
        cover="cover",
        genre="genre",
        language="language",
    )

    restored = BookMapper.to_domain(model)

    assert restored.id == book_id
    assert restored.owner_id == owner_id
    assert restored.total_pages == TotalPages(250)
    assert restored.isbn == "isbn"
    assert restored.publisher == "publisher"
    assert restored.edition == "edition"
    assert restored.cover == "cover"
    assert restored.genre == "genre"
    assert restored.language == "language"
    assert restored.domain_events == []
