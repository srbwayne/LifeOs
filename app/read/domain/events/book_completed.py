from dataclasses import dataclass
from datetime import datetime

from app.read.domain.value_objects.book_completion_id import BookCompletionId
from app.read.domain.value_objects.book_id import BookId
from app.shared.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class BookCompleted(DomainEvent):
    completion_id: BookCompletionId
    book_id: BookId
    completed_at: datetime
