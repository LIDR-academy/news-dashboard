"""Update personal note use case."""

from typing import Optional

from src.application.ports.news_repository import NewsRepository
from src.domain.entities.news_item import NewsItem
from src.domain.exceptions.news_exceptions import (
    NewsNotFoundException,
    UnauthorizedNewsAccessException,
)


class UpdatePersonalNoteUseCase:
    """Use case for updating or clearing a news item's personal note."""

    def __init__(self, news_repository: NewsRepository):
        """Initialize with news repository.

        Args:
            news_repository: The news repository
        """
        self.news_repository = news_repository

    async def execute(self, news_id: str, user_id: str, note: Optional[str]) -> NewsItem:
        """Update or clear the personal note.

        Args:
            news_id: The news item ID
            user_id: The user performing the change
            note: New note content; if None, clears the note

        Returns:
            Updated news item
        """
        # Load and authorize
        news_item = await self.news_repository.get_by_id(news_id)
        if not news_item:
            raise NewsNotFoundException(news_id)
        if news_item.user_id != user_id:
            raise UnauthorizedNewsAccessException(user_id, news_id)

        # Apply change at domain level to enforce validation
        if note is None:
            news_item.clear_personal_note()
        else:
            news_item.update_personal_note(note)

        # Persist through dedicated repository method to ensure atomicity/filters
        return await self.news_repository.update_personal_note(
            news_id=news_id, user_id=user_id, note=news_item.personal_note
        )


