"""Tests for the Jira DC view factory's conversation-creation strategy."""

from unittest.mock import AsyncMock, patch

import pytest
from integrations.jira_dc.jira_dc_view import (
    JiraDcExistingConversationView,
    JiraDcFactory,
    JiraDcNewConversationView,
)


@pytest.mark.asyncio
async def test_factory_always_creates_new_conversation(
    sample_job_context,
    sample_user_auth,
    sample_jira_dc_user,
    sample_jira_dc_workspace,
    jira_dc_conversation,
):
    """Every @openhands mention starts a fresh conversation (matches GitHub/BBDC).

    JDC used to reuse the existing conversation for (issue, user), but that path
    sends the message into a possibly-recycled sandbox and 404s ("Sorry, there was
    an unexpected error starting the job."). The factory must always return a
    JiraDcNewConversationView and must never consult the conversation-reuse lookup,
    even when a prior conversation exists for this (issue, user).
    """
    with patch('integrations.jira_dc.jira_dc_view.integration_store') as mock_store:
        # A prior conversation exists -- the old code would have reused it.
        mock_store.get_user_conversations_by_issue_id = AsyncMock(
            return_value=jira_dc_conversation
        )

        view = await JiraDcFactory.create_jira_dc_view_from_payload(
            job_context=sample_job_context,
            saas_user_auth=sample_user_auth,
            jira_dc_user=sample_jira_dc_user,
            jira_dc_workspace=sample_jira_dc_workspace,
        )

    assert isinstance(view, JiraDcNewConversationView)
    assert not isinstance(view, JiraDcExistingConversationView)
    # The reuse lookup must not be consulted at all.
    mock_store.get_user_conversations_by_issue_id.assert_not_called()
    # A fresh view starts with no conversation id (assigned at creation time).
    assert view.conversation_id == ''
    assert view.selected_repo is None
