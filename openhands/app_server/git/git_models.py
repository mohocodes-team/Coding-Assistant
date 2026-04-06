"""Git-related models for V1 API pagination responses."""

from pydantic import BaseModel

from openhands.integrations.service_types import Repository


class InstallationPage(BaseModel):
    """Paginated response for installations.

    Attributes:
        items: List of installation IDs.
        next_page_id: ID for the next page, or None if there are no more pages.
    """

    items: list[str]
    next_page_id: str | None = None


class RepositoryPage(BaseModel):
    """Paginated response for repositories.

    Attributes:
        items: List of repositories in the current page.
        next_page_id: ID for the next page, or None if there are no more pages.
    """

    items: list[Repository]
    next_page_id: str | None = None
