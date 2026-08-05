class DomainError(Exception):
    """Classe base para exceções de domínio."""
    
    @property
    def message(self) -> str:
        return "Um erro de domínio ocorreu."

    def __str__(self) -> str:
        return self.message
