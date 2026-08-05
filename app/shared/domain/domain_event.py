from dataclasses import dataclass, field
from datetime import datetime, timezone
from app.shared.domain.tsid import new_tsid

@dataclass(frozen=True)
class DomainEvent:
    """Classe base para Eventos de Domínio."""
    event_id: str = field(default_factory=new_tsid, init=False)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc), init=False)
