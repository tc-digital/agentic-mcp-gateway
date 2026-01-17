"""Tests for research tools."""
import os
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from agentic_mcp_gateway.tools import (
    analyze_data_tool,
    calculate_tool,
    send_email_tool,
    summarize_tool,
    weather_forecast_tool,
    web_search_tool,
)


@pytest.mark.asyncio
async def test_web_search():
    """Test web search tool."""
    results = await web_search_tool("test query", max_results=3)

    assert len(results) == 3
    assert all("title" in r for r in results)
    assert all("url" in r for r in results)
    assert all("snippet" in r for r in results)


@pytest.mark.asyncio
async def test_summarize():
    """Test summarization tool."""
    text = "This is a long text that needs to be summarized. " * 50
    result = await summarize_tool(text, max_length=100)

    assert "summary" in result
    assert "original_length" in result
    assert result["original_length"] > result["summary_length"]


@pytest.mark.asyncio
async def test_calculate_success():
    """Test calculator with valid expression."""
    result = await calculate_tool("2 + 2")

    assert result["success"] is True
    assert result["result"] == 4


@pytest.mark.asyncio
async def test_calculate_error():
    """Test calculator with invalid expression."""
    result = await calculate_tool("invalid")

    assert result["success"] is False
    assert result["error"] is not None


@pytest.mark.asyncio
async def test_analyze_numeric_data():
    """Test data analysis with numeric data."""
    data = [10, 20, 30, 40, 50]
    result = await analyze_data_tool(data, "statistical")

    assert "insights" in result
    assert len(result["insights"]) > 0
    assert any("Mean" in insight for insight in result["insights"])


@pytest.mark.asyncio
async def test_analyze_empty_data():
    """Test data analysis with empty data."""
    result = await analyze_data_tool([], "statistical")

    assert "error" in result


@pytest.mark.asyncio
async def test_weather_forecast_with_coordinates():
    """Test weather forecast with lat,lon coordinates."""
    # Using coordinates for Kansas (central US)
    result = await weather_forecast_tool("39.7456,-97.0892", "forecast")

    # Should succeed with real API
    if result.get("success"):
        assert "location" in result
        assert "periods" in result
        assert len(result["periods"]) > 0
        # Check first period has expected fields
        first_period = result["periods"][0]
        assert "temperature" in first_period
        assert "shortForecast" in first_period
    else:
        # If it fails, it should have an error message
        assert "error" in result


@pytest.mark.asyncio
async def test_weather_forecast_invalid_location():
    """Test weather forecast with invalid location format."""
    result = await weather_forecast_tool("invalid", "forecast")

    assert result["success"] is False
    assert "error" in result


@pytest.mark.asyncio
async def test_weather_forecast_invalid_coordinates():
    """Test weather forecast with malformed coordinates."""
    # Test with missing coordinate part
    result = await weather_forecast_tool("39.7456", "forecast")
    assert result["success"] is False
    assert "error" in result

    # Test with non-numeric coordinates
    result = await weather_forecast_tool("abc,def", "forecast")
    assert result["success"] is False
    assert "error" in result

    # Test with out of range coordinates
    result = await weather_forecast_tool("999,-999", "forecast")
    assert result["success"] is False
    assert "error" in result


@pytest.mark.asyncio
async def test_send_email_missing_webhook_url():
    """Test send_email tool when webhook URL is not configured."""
    # Ensure POWER_AUTOMATE_WEBHOOK_URL is not set
    with patch.dict(os.environ, {}, clear=True):
        result = await send_email_tool(
            to_email="test@example.com",
            subject="Test Subject",
            body="Test body content",
        )

        assert result["success"] is False
        assert "not configured" in result["error"]


@pytest.mark.asyncio
async def test_send_email_invalid_email():
    """Test send_email tool with invalid email addresses."""
    with patch.dict(os.environ, {"POWER_AUTOMATE_WEBHOOK_URL": "https://example.com/webhook"}):
        # Test with missing @
        result = await send_email_tool(
            to_email="invalid-email",
            subject="Test Subject",
            body="Test body",
        )
        assert result["success"] is False
        assert "Invalid email format" in result["error"]

        # Test with empty email
        result = await send_email_tool(
            to_email="",
            subject="Test Subject",
            body="Test body",
        )
        assert result["success"] is False
        assert "Invalid email format" in result["error"]

        # Test with missing domain
        result = await send_email_tool(
            to_email="test@",
            subject="Test Subject",
            body="Test body",
        )
        assert result["success"] is False
        assert "Invalid email format" in result["error"]


@pytest.mark.asyncio
async def test_send_email_invalid_subject():
    """Test send_email tool with invalid subject."""
    with patch.dict(os.environ, {"POWER_AUTOMATE_WEBHOOK_URL": "https://example.com/webhook"}):
        # Test with empty subject
        result = await send_email_tool(
            to_email="test@example.com",
            subject="",
            body="Test body",
        )
        assert result["success"] is False
        assert "subject cannot be empty" in result["error"]

        # Test with subject exceeding max length
        long_subject = "x" * 501
        result = await send_email_tool(
            to_email="test@example.com",
            subject=long_subject,
            body="Test body",
        )
        assert result["success"] is False
        assert "exceeds maximum length" in result["error"]


@pytest.mark.asyncio
async def test_send_email_invalid_body():
    """Test send_email tool with invalid body."""
    with patch.dict(os.environ, {"POWER_AUTOMATE_WEBHOOK_URL": "https://example.com/webhook"}):
        # Test with empty body
        result = await send_email_tool(
            to_email="test@example.com",
            subject="Test Subject",
            body="",
        )
        assert result["success"] is False
        assert "body cannot be empty" in result["error"]

        # Test with body exceeding max length
        long_body = "x" * 50001
        result = await send_email_tool(
            to_email="test@example.com",
            subject="Test Subject",
            body=long_body,
        )
        assert result["success"] is False
        assert "exceeds maximum length" in result["error"]


@pytest.mark.asyncio
async def test_send_email_success():
    """Test send_email tool with valid inputs and successful webhook call."""
    webhook_url = "https://example.com/webhook"

    # Mock httpx.AsyncClient
    with patch.dict(os.environ, {"POWER_AUTOMATE_WEBHOOK_URL": webhook_url}):
        with patch("agentic_mcp_gateway.tools.send_email.httpx.AsyncClient") as mock_client_class:
            # Setup mock response
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.raise_for_status = AsyncMock()

            # Setup mock client
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock()
            mock_client_class.return_value = mock_client

            result = await send_email_tool(
                to_email="test@example.com",
                subject="Test Subject",
                body="This is a test email body.",
            )

            assert result["success"] is True
            assert result["message"] == "Email sent successfully"
            assert result["to_email"] == "test@example.com"
            assert result["subject"] == "Test Subject"

            # Verify the webhook was called correctly
            mock_client.post.assert_called_once()
            call_args = mock_client.post.call_args
            assert call_args[0][0] == webhook_url
            assert call_args[1]["json"]["to_email"] == "test@example.com"
            assert call_args[1]["json"]["subject"] == "Test Subject"
            assert call_args[1]["json"]["body"] == "This is a test email body."


@pytest.mark.asyncio
async def test_send_email_webhook_http_error():
    """Test send_email tool when webhook returns HTTP error."""
    webhook_url = "https://example.com/webhook"

    with patch.dict(os.environ, {"POWER_AUTOMATE_WEBHOOK_URL": webhook_url}):
        with patch("agentic_mcp_gateway.tools.send_email.httpx.AsyncClient") as mock_client_class:
            # Setup mock response with error
            mock_response = AsyncMock()
            mock_response.status_code = 400
            mock_response.text = "Bad Request"

            # Create a mock request
            mock_request = AsyncMock()

            # Setup mock to raise HTTPStatusError
            http_error = httpx.HTTPStatusError(
                "Bad Request",
                request=mock_request,
                response=mock_response
            )

            # Setup mock client
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(side_effect=http_error)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await send_email_tool(
                to_email="test@example.com",
                subject="Test Subject",
                body="Test body",
            )

            assert result["success"] is False
            assert "webhook error" in result["error"]
            assert "400" in result["error"]


@pytest.mark.asyncio
async def test_send_email_network_error():
    """Test send_email tool when network error occurs."""
    webhook_url = "https://example.com/webhook"

    with patch.dict(os.environ, {"POWER_AUTOMATE_WEBHOOK_URL": webhook_url}):
        with patch("agentic_mcp_gateway.tools.send_email.httpx.AsyncClient") as mock_client_class:
            # Setup mock to raise RequestError
            network_error = httpx.RequestError("Connection refused")

            # Setup mock client
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(side_effect=network_error)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            result = await send_email_tool(
                to_email="test@example.com",
                subject="Test Subject",
                body="Test body",
            )

            assert result["success"] is False
            assert "Network error" in result["error"]


# ============================================================================
# GitHub Tool Tests
# ============================================================================
# Tests for GitHub integration tools including repository info, search,
# issues listing, and language statistics.


@pytest.mark.asyncio
async def test_github_repo_info_success():
    """Test GitHub repo info with successful API response."""
    from agentic_mcp_gateway.tools.github import github_repo_info
    
    mock_response_data = {
        "name": "test-repo",
        "full_name": "test-owner/test-repo",
        "description": "A test repository",
        "owner": {"login": "test-owner"},
        "stargazers_count": 100,
        "forks_count": 20,
        "open_issues_count": 5,
        "language": "Python",
        "default_branch": "main",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-12-01T00:00:00Z",
        "topics": ["test", "python"],
        "license": {"name": "MIT"},
        "homepage": "https://example.com",
        "html_url": "https://github.com/test-owner/test-repo"
    }
    
    with patch("agentic_mcp_gateway.tools.github.httpx.AsyncClient") as mock_client_class:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()
        mock_client_class.return_value = mock_client
        
        result = await github_repo_info("test-owner", "test-repo")
        
        assert result["success"] is True
        assert result["result"]["name"] == "test-repo"
        assert result["result"]["stars"] == 100
        assert result["result"]["language"] == "Python"


@pytest.mark.asyncio
async def test_github_repo_info_not_found():
    """Test GitHub repo info with 404 response."""
    from agentic_mcp_gateway.tools.github import github_repo_info
    
    with patch("agentic_mcp_gateway.tools.github.httpx.AsyncClient") as mock_client_class:
        mock_response = AsyncMock()
        mock_response.status_code = 404
        
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()
        mock_client_class.return_value = mock_client
        
        result = await github_repo_info("nonexistent", "repo")
        
        assert result["success"] is False
        assert "not found" in result["error"]


@pytest.mark.asyncio
async def test_github_search_repos_success():
    """Test GitHub repository search."""
    from agentic_mcp_gateway.tools.github import github_search_repos
    
    mock_response_data = {
        "total_count": 100,
        "items": [
            {
                "name": "repo1",
                "full_name": "owner1/repo1",
                "description": "Description 1",
                "stargazers_count": 50,
                "language": "Python",
                "html_url": "https://github.com/owner1/repo1"
            },
            {
                "name": "repo2",
                "full_name": "owner2/repo2",
                "description": "Description 2",
                "stargazers_count": 30,
                "language": "JavaScript",
                "html_url": "https://github.com/owner2/repo2"
            }
        ]
    }
    
    with patch("agentic_mcp_gateway.tools.github.httpx.AsyncClient") as mock_client_class:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()
        mock_client_class.return_value = mock_client
        
        result = await github_search_repos("test query", max_results=2)
        
        assert result["success"] is True
        assert len(result["result"]) == 2
        assert result["result"][0]["name"] == "repo1"
        assert result["details"]["total_count"] == 100


@pytest.mark.asyncio
async def test_github_list_issues_success():
    """Test listing GitHub issues."""
    from agentic_mcp_gateway.tools.github import github_list_issues
    
    mock_response_data = [
        {
            "number": 1,
            "title": "Bug report",
            "state": "open",
            "user": {"login": "user1"},
            "labels": [{"name": "bug"}],
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
            "comments": 5,
            "html_url": "https://github.com/owner/repo/issues/1"
        },
        {
            "number": 2,
            "title": "Feature request",
            "state": "open",
            "user": {"login": "user2"},
            "labels": [{"name": "enhancement"}],
            "created_at": "2023-01-03T00:00:00Z",
            "updated_at": "2023-01-04T00:00:00Z",
            "comments": 2,
            "html_url": "https://github.com/owner/repo/issues/2"
        }
    ]
    
    with patch("agentic_mcp_gateway.tools.github.httpx.AsyncClient") as mock_client_class:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()
        mock_client_class.return_value = mock_client
        
        result = await github_list_issues("owner", "repo", state="open")
        
        assert result["success"] is True
        assert len(result["result"]) == 2
        assert result["result"][0]["title"] == "Bug report"
        assert result["details"]["count"] == 2


@pytest.mark.asyncio
async def test_github_repo_languages_success():
    """Test getting repository languages."""
    from agentic_mcp_gateway.tools.github import github_repo_languages
    
    mock_response_data = {
        "Python": 50000,
        "JavaScript": 30000,
        "HTML": 20000
    }
    
    with patch("agentic_mcp_gateway.tools.github.httpx.AsyncClient") as mock_client_class:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()
        mock_client_class.return_value = mock_client
        
        result = await github_repo_languages("owner", "repo")
        
        assert result["success"] is True
        assert len(result["result"]) == 3
        assert result["result"][0]["language"] == "Python"
        assert result["result"][0]["percentage"] == 50.0
        assert result["details"]["total_bytes"] == 100000
