# Importa a classe da biblioteca com um alias para evitar colisão de nomes
from argon2 import PasswordHasher as Argon2LibraryHasher
from argon2.exceptions import VerifyMismatchError

from app.auth.domain.ports.password_hasher import IPasswordHasher
from app.auth.domain.value_objects.hashed_password import HashedPassword

class Argon2PasswordHasher(IPasswordHasher):
    """Um adapter que implementa a interface IPasswordHasher usando a biblioteca argon2-cffi."""
    def __init__(self):
        # Instancia a classe da biblioteca, não a si mesma
        self._ph = Argon2LibraryHasher()

    def hash(self, password: str) -> HashedPassword:
        """Gera o hash de uma senha em texto puro."""
        hashed_value = self._ph.hash(password)
        return HashedPassword(value=hashed_value)

    def verify(self, password: str, hashed_password: HashedPassword) -> bool:
        """Verifica se uma senha em texto puro corresponde a um hash."""
        try:
            self._ph.verify(hashed_password.value, password)
            return True
        except VerifyMismatchError:
            return False
