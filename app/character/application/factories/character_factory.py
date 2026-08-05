from app.auth.application.ports.character_factory import ICharacterFactory
from app.auth.domain.aggregates.user import User
from app.character.domain.aggregates.player import Player
from app.character.domain.aggregates.character import Character
from app.character.domain.ports.player_repository import IPlayerRepository
from app.character.domain.ports.character_repository import ICharacterRepository
from app.character.domain.errors.character_errors import (
    PlayerAlreadyHasCharacterError,
    UserAlreadyHasPlayerError,
)
from app.character.domain.value_objects.player_name import PlayerName

class CharacterFactory(ICharacterFactory):
    def __init__(
        self,
        player_repository: IPlayerRepository,
        character_repository: ICharacterRepository,
    ):
        self._player_repository = player_repository
        self._character_repository = character_repository

    def create_initial(self, user: User) -> tuple[Player, Character]:
        if self._player_repository.find_by_user_id(user.id):
            raise UserAlreadyHasPlayerError()

        # O nome do Player inicialmente será derivado do email
        player_name = PlayerName(user.email.value.split('@')[0])
        
        player = Player.create(user_id=user.id, name=player_name)
        self._player_repository.save(player)

        if self._character_repository.find_by_player_id(player.id):
            raise PlayerAlreadyHasCharacterError()

        character = Character.create(player_id=player.id)
        self._character_repository.save(character)
        return player, character
