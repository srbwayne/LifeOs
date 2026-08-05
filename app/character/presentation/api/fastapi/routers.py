from fastapi import APIRouter, Depends

from app.composition_root import get_current_user_id
from app.shared.domain.identifiers.user_id import UserId
from app.character.application.queries.get_character import (
    GetCharacterQuery,
    GetCharacterQueryHandler,
)
from app.character.application.queries.get_character_profile import (
    GetCharacterProfileQuery,
    GetCharacterProfileQueryHandler,
)
from app.character.dependencies import (
    get_character_profile_query_handler,
    get_character_query_handler,
)
from app.character.presentation.api.fastapi.schemas import (
    CharacterProfileSchema,
    CharacterSchema,
)


router = APIRouter(prefix="/character", tags=["Character"])


@router.get("", response_model=CharacterSchema)
def get_character(
    user_id: UserId = Depends(get_current_user_id),
    handler: GetCharacterQueryHandler = Depends(get_character_query_handler),
):
    return handler(GetCharacterQuery(user_id=user_id))


@router.get("/profile", response_model=CharacterProfileSchema)
def get_character_profile(
    user_id: UserId = Depends(get_current_user_id),
    handler: GetCharacterProfileQueryHandler = Depends(
        get_character_profile_query_handler
    ),
):
    return handler(GetCharacterProfileQuery(user_id=user_id))
