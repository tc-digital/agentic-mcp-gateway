# Contributing to Agentic MCP Gateway

Thank you for your interest in contributing! This guide will help you add new tools, features, and improvements to the gateway.

## 🏗️ Architecture Overview

The Agentic MCP Gateway uses a modular, plugin-style architecture:

```
src/agentic_mcp_gateway/
├── tools/           # Individual tool implementations
├── agents/          # Reasoning agents and orchestrators
├── models/          # Data models and schemas
├── orchestration/   # Workflow coordination
├── adapters/        # Interface adapters
└── server.py        # FastMCP server and tool registration
```

## 🔌 Adding a New Tool

Adding a tool is straightforward - no core changes needed!

### 1. Create the Tool Implementation

Create a new file in `src/agentic_mcp_gateway/tools/`:

```python
# src/agentic_mcp_gateway/tools/my_tool.py
"""My awesome tool for doing X."""
from typing import Any


async def my_tool(param1: str, param2: int = 10) -> dict[str, Any]:
    """
    Does something awesome.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2 (default: 10)
        
    Returns:
        Dictionary with results
    """
    # Your implementation here
    result = f"Processed {param1} with value {param2}"
    
    return {
        "success": True,
        "result": result,
        "details": {"param1": param1, "param2": param2}
    }
```

### 2. Register in the MCP Server

Add your tool to `src/agentic_mcp_gateway/server.py`:

```python
from .tools.my_tool import my_tool as my_tool_impl

@mcp.tool()
async def my_tool(param1: str, param2: int = 10) -> dict[str, Any]:
    """Does something awesome.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2 (default: 10)
        
    Returns:
        Dictionary with results
    """
    result = await my_tool_impl(param1=param1, param2=param2)
    return result
```

### 3. Add Tests

Create tests in `tests/unit/test_tools.py`:

```python
@pytest.mark.asyncio
async def test_my_tool():
    """Test my_tool basic functionality."""
    result = await my_tool_impl("test", 20)
    
    assert result["success"] is True
    assert "test" in result["result"]
    assert result["details"]["param2"] == 20
```

### 4. Update Documentation

Add your tool to the README.md tool list:

```markdown
- **My Tool**: Does something awesome
```

That's it! Your tool is now available to all agents and workflows.

## 🤖 Making Tools Agent-Compatible

For tools to work with the reasoning agent, add them to `agents/tools.py`:

```python
from langchain.tools import tool
from ..tools.my_tool import my_tool as my_tool_impl

@tool
async def my_tool_wrapper(param1: str, param2: int = 10) -> str:
    """Does something awesome. Use when you need to X."""
    result = await my_tool_impl(param1, param2)
    return str(result["result"])
```

## 📝 Tool Development Guidelines

### Best Practices

1. **Type Hints**: Use type hints for all parameters and return values
2. **Docstrings**: Include clear docstrings with Args and Returns sections
3. **Error Handling**: Return structured errors, don't raise exceptions
4. **Async**: Use `async def` for I/O operations
5. **Testing**: Write unit tests for all code paths

### Return Format

Tools should return dictionaries with consistent structure:

```python
{
    "success": True,  # or False
    "result": "...",  # Main result
    "error": "...",   # Error message if success=False
    "details": {}     # Additional metadata
}
```

### Example Patterns

**API Integration:**
```python
async def api_tool(query: str) -> dict[str, Any]:
    """Call external API."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.example.com/v1?q={query}")
            data = response.json()
            
        return {
            "success": True,
            "result": data["results"],
            "details": {"query": query, "count": len(data["results"])}
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "details": {"query": query}
        }
```

**Data Processing:**
```python
async def process_tool(data: list[int]) -> dict[str, Any]:
    """Process data."""
    result = sum(data) / len(data)
    
    return {
        "success": True,
        "result": result,
        "details": {
            "count": len(data),
            "min": min(data),
            "max": max(data)
        }
    }
```

## 🧪 Testing

### Run Tests

```bash
# All tests
pytest tests/

# Specific test file
pytest tests/unit/test_tools.py

# With coverage
pytest --cov=agentic_mcp_gateway --cov-report=html
```

### Test Structure

```python
import pytest
from agentic_mcp_gateway.tools.my_tool import my_tool

@pytest.mark.asyncio
async def test_my_tool_success():
    """Test successful execution."""
    result = await my_tool("input")
    assert result["success"] is True

@pytest.mark.asyncio
async def test_my_tool_error():
    """Test error handling."""
    result = await my_tool("")
    assert result["success"] is False
    assert "error" in result
```

## 🎨 Code Style

We use Ruff for linting and formatting:

```bash
# Check code style
ruff check src/

# Format code
ruff format src/

# Type checking
mypy src/
```

### Style Guidelines

- Line length: 100 characters
- Use double quotes for strings
- Follow PEP 8 conventions
- Use descriptive variable names
- Add comments for complex logic

## 🔍 Integration Examples

### GitHub API Integration

```python
# tools/github.py
import httpx
import os

async def github_repo_info(owner: str, repo: str) -> dict[str, Any]:
    """Get GitHub repository information."""
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}",
            headers=headers
        )
        
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"GitHub API error: {response.status_code}"
            }
            
        data = response.json()
        return {
            "success": True,
            "result": {
                "name": data["name"],
                "description": data["description"],
                "stars": data["stargazers_count"],
                "language": data["language"]
            }
        }
```

### Database Integration

```python
# tools/database.py
from sqlmodel import select, Session
from ..models.data import Record

async def query_database(query: str) -> dict[str, Any]:
    """Query the database."""
    with Session(engine) as session:
        results = session.exec(select(Record).where(Record.field == query))
        records = [r.dict() for r in results]
        
    return {
        "success": True,
        "result": records,
        "details": {"count": len(records)}
    }
```

## 🚀 Submitting Changes

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/my-tool`
3. **Make** your changes
4. **Test** thoroughly: `pytest tests/`
5. **Lint** your code: `ruff check src/`
6. **Commit** with clear messages: `git commit -m "Add: My awesome tool"`
7. **Push** to your fork: `git push origin feature/my-tool`
8. **Open** a Pull Request

### Commit Message Format

```
Type: Brief description

Longer explanation if needed.

- Change 1
- Change 2
```

Types: `Add`, `Fix`, `Update`, `Remove`, `Refactor`, `Docs`, `Test`

## 📚 Resources

- [FastMCP Documentation](https://gofastmcp.com)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [MCP Protocol Specification](https://modelcontextprotocol.io)

## 💬 Getting Help

- Open an [Issue](https://github.com/tc-digital/agentic-mcp-gateway/issues) for bugs
- Start a [Discussion](https://github.com/tc-digital/agentic-mcp-gateway/discussions) for questions
- Check existing issues and PRs before creating new ones

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Happy Contributing! 🎉**
