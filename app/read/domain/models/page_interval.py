from dataclasses import dataclass


@dataclass(frozen=True)
class PageInterval:
    start_page: int
    end_page: int

    def __post_init__(self) -> None:
        if isinstance(self.start_page, bool) or not isinstance(self.start_page, int):
            raise TypeError("Page interval start must be an integer.")
        if isinstance(self.end_page, bool) or not isinstance(self.end_page, int):
            raise TypeError("Page interval end must be an integer.")
        if self.start_page < 1:
            raise ValueError("Page interval start must be positive.")
        if self.end_page < self.start_page:
            raise ValueError("Page interval end must not precede start.")

    @property
    def length(self) -> int:
        return self.end_page - self.start_page + 1
