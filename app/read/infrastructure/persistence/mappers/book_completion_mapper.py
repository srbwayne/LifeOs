from app.read.domain.aggregates.book_completion import BookCompletion
from app.read.domain.value_objects.book_completion_id import BookCompletionId
from app.read.domain.value_objects.book_id import BookId
from app.read.infrastructure.persistence.datetime import canonicalize_utc_datetime
from app.read.infrastructure.persistence.models.book_completion_model import (
    BookCompletionModel,
)


class BookCompletionMapper:
    @staticmethod
    def to_domain(model: BookCompletionModel) -> BookCompletion:
        return BookCompletion.restore(
            id=BookCompletionId.from_value(model.id),
            book_id=BookId.from_value(model.book_id),
            completed_at=canonicalize_utc_datetime(model.completed_at),
        )

    @staticmethod
    def to_persistence(completion: BookCompletion) -> BookCompletionModel:
        return BookCompletionModel(
            id=completion.id.to_persistence(),
            book_id=completion.book_id.to_persistence(),
            completed_at=completion.completed_at,
        )
