# Agentic MCP Gateway

A modular, agentic MCP gateway for AI-powered developer workflows. Features deep GitHub integration, pluggable tools, multi-LLM orchestration, and visible reasoning chains for complex task automation.

## 🚀 Quick Start

Get up and running in under 2 minutes!

### Option 1: Automated Setup Script (Recommended)

**Linux/macOS:**
```bash
git clone https://github.com/tc-digital/agentic-mcp-gateway.git
cd agentic-mcp-gateway
./setup.sh
```

**Windows:**
```cmd
git clone https://github.com/tc-digital/agentic-mcp-gateway.git
cd agentic-mcp-gateway
setup.bat
```

The scripts will:
- ✅ Create and activate a virtual environment
- ✅ Install all dependencies automatically
- ✅ Check your environment configuration
- ✅ Optionally start the MCP server

### Option 2: Docker (Containerized Deployment)

```bash
# Build the Docker image
docker build -t agentic-mcp-gateway .

# Run with environment variables
docker run -it --rm \
  -e OPENAI_API_KEY='your-api-key-here' \
  -e POWER_AUTOMATE_WEBHOOK_URL='your-webhook-url' \
  agentic-mcp-gateway
```

For Docker Compose, create a `docker-compose.yml`:
```yaml
version: '3.8'
services:
  mcp-server:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - POWER_AUTOMATE_WEBHOOK_URL=${POWER_AUTOMATE_WEBHOOK_URL}
    # Uncomment if you add HTTP API endpoints:
    # ports:
    #   - "8000:8000"
```

Then run: `docker-compose up`

### Option 3: Manual Installation

**Prerequisites:**
- Python 3.10 or higher
- OpenAI API key

```bash
# Clone and navigate
git clone https://github.com/tc-digital/agentic-mcp-gateway.git
cd agentic-mcp-gateway

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### Environment Variables

Set these environment variables before running:

```bash
# Required for AI-powered workflows
export OPENAI_API_KEY='sk-...'

# Optional for send_email tool
export POWER_AUTOMATE_WEBHOOK_URL='https://prod-...'

# Optional for GitHub integration
export GITHUB_TOKEN='ghp_...'
```

**Windows (cmd):**
```cmd
set OPENAI_API_KEY=sk-...
set POWER_AUTOMATE_WEBHOOK_URL=https://prod-...
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-..."
$env:POWER_AUTOMATE_WEBHOOK_URL="https://prod-..."
```

### Running the Server

**Using the startup script (Recommended for MCP clients like Claude Desktop):**
```bash
./start_mcp.sh
```
The script automatically activates the virtual environment and starts the server.

**Direct Python command:**
```bash
python -m mcp_server_alpha.server
```

**Research Example:**
```bash
python examples/research_example.py
```

**GitHub Integration Demo:**
```bash
# Set GitHub token for higher rate limits (optional)
export GITHUB_TOKEN='ghp_...'

# Run the GitHub demo
python examples/github_demo.py
```

This demo showcases:
- Repository information retrieval
- Repository search
- Issue listing and analysis
- Language statistics
- Complete workflow automation

### Troubleshooting

**Issue: "OPENAI_API_KEY not set"**
- Solution: Set the environment variable before running (see Environment Variables above)

**Issue: "Python 3.10 or higher is required"**
- Solution: Upgrade Python or use Docker

**Issue: "Module not found" errors**
- Solution: Ensure virtual environment is activated and dependencies are installed
  ```bash
  source venv/bin/activate  # or venv\Scripts\activate on Windows
  pip install -e ".[dev]"
  ```

**Issue: Docker build fails**
- Solution: Ensure Docker is installed and running, then try: `docker system prune` and rebuild

**Claude Desktop Integration Issues:**
- See [TROUBLESHOOTING_CLAUDE_DESKTOP.md](TROUBLESHOOTING_CLAUDE_DESKTOP.md)

## 📢 Migration to FastMCP (v0.2.0)

**Important Notice:** As of version 0.2.0, this project has been migrated from the legacy `mcp` package to **FastMCP**, the emerging standard for Python MCP applications. FastMCP is actively maintained and offers enhanced features and better integration with the Python MCP ecosystem.

### What Changed:
- **Dependency Update**: Replaced `mcp>=0.9.0` with `fastmcp<3` (pinned to avoid breaking changes in v3.0)
- **Server Implementation**: Refactored to use FastMCP's decorator-based tool registration
- **Simplified Architecture**: Tools are now registered with `@mcp.tool()` decorators instead of manual registration
- **Better Type Safety**: Leverages FastMCP's built-in type handling and validation

### Migration Impact:
- ✅ **All existing functionality preserved** - No changes to tool behavior or API
- ✅ **All tests passing** - Full backward compatibility maintained
- ✅ **Same installation process** - No changes required to setup scripts
- ✅ **Compatible with existing MCP clients** - Works with Claude Desktop and other MCP clients
- 📚 **Updated codebase** - Cleaner, more maintainable code following modern patterns

### For Developers:
If you're maintaining a fork or have custom modifications:
1. Update `pyproject.toml` to use `fastmcp<3` instead of `mcp>=0.9.0`
2. Refactor tool registration to use `@mcp.tool()` decorators
3. Replace `Server` with `FastMCP` instance
4. Tools should return dictionaries/objects directly (no need for `TextContent` wrapping)
5. Run tests to ensure compatibility: `pytest tests/`

For more details, see [FastMCP Documentation](https://gofastmcp.com).

## 🎯 What It Does

The Agentic MCP Gateway provides:
- **🔍 Web Search & Research** - Information gathering and analysis
- **🧮 Calculations** - Mathematical and financial computations
- **📊 Data Analysis** - Statistical analysis and pattern finding
- **📝 Summarization** - Extract key information from content
- **🌤️ Weather Forecasts** - Real-time weather data via weather.gov API
- **📧 Email Integration** - Send emails via Power Automate webhooks
- **🐙 GitHub Integration** - Repository analysis, PR management, code reviews (NEW!)
- **🤖 Autonomous Reasoning** - Multi-step task orchestration with visible reasoning chains
- **🔌 Pluggable Architecture** - Easy addition of new tools and integrations
- **💭 Traceability** - Full visibility into agent decision-making process

## 🆕 Agentic Orchestration

The **Reasoning Agent** is a meta-tool that orchestrates other MCP tools using LangGraph for autonomous planning and execution. Perfect for complex, multi-step developer workflows.

**Example**: *"Analyze this GitHub repository and suggest performance improvements"*

The agent will:
1. 🔍 Fetch repository information and structure
2. 📊 Analyze code patterns and dependencies
3. 💡 Generate specific, actionable recommendations
4. 📝 Provide implementation guidance

**📖 [Full Reasoning Agent Documentation](REASONING_AGENT.md)**

## 🏗️ Architecture

```
src/agentic_mcp_gateway/
├── models/          # Data models (Query, Result, ThoughtChain, etc.)
├── tools/           # Modular tools (search, calculator, analyzer, weather, email, github)
├── agents/          # LangGraph-based reasoning agents and orchestrators
├── orchestration/   # Workflow engine for complex task automation
├── adapters/        # Multi-channel adapters (chat, voice, API)
└── server.py        # FastMCP server implementation
```

### Key Components

#### 1. **Reasoning Agent Orchestrator** (`agents/reasoning_orchestrator.py`)
- Meta-tool that orchestrates other MCP tools using LangGraph
- Autonomous goal decomposition and task planning
- Multi-step execution with branching logic
- Step-by-step progress tracking with visible reasoning

#### 2. **Agentic Tools** (`agents/research_agent.py`)
- LangGraph-based autonomous agents
- Uses OpenAI (gpt-4o-mini by default) for reasoning
- Visible thought process and reasoning chains
- Dynamic tool orchestration based on task requirements

#### 3. **Modular Tool System** (`tools/`)
- **Web Search**: Find information on any topic (ready for real API integration)
- **Calculator**: Perform mathematical calculations
- **Data Analyzer**: Statistical analysis and pattern finding
- **Summarizer**: Extract key information from text
- **Weather Forecast**: Real-time weather forecasts using weather.gov API
- **Send Email**: Trigger Power Automate flow to send emails via webhook
- **GitHub Integration**: Repository analysis, issue/PR management, code reviews (NEW!)

#### 4. **Reasoning Chain** (`models/reasoning.py`)
- Tracks agent's thought process
- Shows observations, analysis, synthesis, and conclusions
- Helps understand how the agent reaches decisions

#### 5. **Plugin Architecture**
- Easy to add new tools and integrations
- Config-driven tool registration
- No core code changes needed for new capabilities
- See [CONTRIBUTING.md](CONTRIBUTING.md) for details

### Example Workflows

The gateway supports various agentic workflows:

```python
# Developer workflows
"Analyze the tc-digital/agentic-mcp-gateway repository and suggest improvements"
"Review PR #42 and provide feedback on code quality and security"
"Search for React performance optimization techniques and create a summary"

# Data & calculations
"Calculate compound interest on $10,000 at 5% for 3 years"
"Analyze this dataset: [10, 15, 20, 25, 30] and show statistics"

# Weather & communications
"What's the weather forecast for zip code 10001?"
"Send an email to team@example.com with today's standup notes"

# Multi-step agentic tasks
"Research best practices for Python async/await and create a guide"
"Analyze repository issues labeled 'bug' and identify common patterns"
```

For Claude Desktop users, see the [Quick Start](#-quick-start) section for setup instructions.

## 💡 Usage

### Basic Workflow

```python
from agentic_mcp_gateway.agents import ResearchAgent

# Initialize agent
agent = ResearchAgent()

# Execute a task
result = await agent.research("What is quantum computing?")

print(result["response"])  # Agent's answer
print(result["reasoning_chain"])  # Thought process
```

### With Reasoning Visibility

```python
# The agent shows its reasoning
result = await agent.research("Compare Python and JavaScript")

# See how it thinks
for step in result["reasoning_chain"]:
    print(step)
# Output:
# 💭 I need to search for information about Python...
# 🔧 Using web_search tool: {'query': 'Python programming language'}
# 💭 Based on these sources, I can conclude...
```

### Interactive Mode

```python
# Maintains context across questions
state = None

questions = [
    "What is machine learning?",
    "What are the main types?",  # Remembers context
    "Which one should I learn first?"  # Continues conversation
]

for question in questions:
    result = await agent.research(question, state)
    state = result["state"]  # Preserve context
    print(result["response"])
```

## 🔧 Extending the Assistant

### Adding a New Tool

1. Create tool in `src/mcp_server_alpha/tools/`:

```python
# my_new_tool.py
async def my_tool(param: str) -> dict:
    """Tool description."""
    # Implementation
    return {"result": "..."}
```

2. Add to agent tools in `agents/tools.py`:

```python
@tool
async def my_tool_wrapper(param: str) -> str:
    """Tool for LangChain."""
    result = await my_tool(param)
    return result["result"]
```

3. Agent automatically uses it when relevant!

### Integrating Real APIs

The tools are designed to be easily upgraded:

**Web Search**: Replace mock with Google Custom Search, Bing, or DuckDuckGo API

```python
# tools/search.py
import requests

async def web_search_tool(query: str, max_results: int = 5):
    # Replace mock with real API
    response = requests.get(
        "https://api.search.com/search",
        params={"q": query, "limit": max_results}
    )
    return response.json()["results"]
```

**Weather Forecast**: Already integrated with real weather.gov API!

```python
# Query by zip code
result = await weather_forecast_tool("10001", "forecast")

# Query by coordinates  
result = await weather_forecast_tool("39.7456,-97.0892", "hourly")

# Returns structured forecast data
{
  "success": true,
  "location": {
    "latitude": 40.7484,
    "longitude": -73.9967,
    "city": "New York",
    "state": "NY"
  },
  "forecast_type": "forecast",
  "periods": [
    {
      "name": "Tonight",
      "temperature": 45,
      "temperatureUnit": "F",
      "windSpeed": "5 mph",
      "windDirection": "SW",
      "shortForecast": "Partly Cloudy",
      "detailedForecast": "Partly cloudy, with a low around 45..."
    }
  ]
}
```

**Send Email via Power Automate**: Already integrated with configurable webhook!

See the [Power Automate Integration Guide](POWER_AUTOMATE_INTEGRATION.md) for detailed setup instructions.

```python
# Configure in Claude Desktop config or as system environment variable
# Claude Desktop: ~/Library/Application Support/Claude/claude_desktop_config.json
# Add to "env" section: "POWER_AUTOMATE_WEBHOOK_URL": "https://..."

# Send email via the tool
result = await send_email_tool(
    to_email="recipient@example.com",
    subject="Meeting Summary",
    body="Here is the summary of our meeting today..."
)

# Returns structured result
{
  "success": true,
  "message": "Email sent successfully",
  "to_email": "recipient@example.com",
  "subject": "Meeting Summary"
}
```

**Important**: After configuring Claude Desktop, completely quit and restart the application.

**Troubleshooting**: If you get configuration errors, see [TROUBLESHOOTING_CLAUDE_DESKTOP.md](TROUBLESHOOTING_CLAUDE_DESKTOP.md).

For complete setup instructions, troubleshooting, and advanced configuration, see [POWER_AUTOMATE_INTEGRATION.md](POWER_AUTOMATE_INTEGRATION.md).

**Other integrations**:
- Document analysis (PDF, Word, etc.)
- Database queries
- Code execution (sandboxed)
- Image analysis
- Chart generation
- And more...

## 🎮 Example Output

```
📋 Research Query 1:
   What are the key differences between machine learning and deep learning?
----------------------------------------------------------------------

🤖 Agent Response:
   Machine learning is a broader field that includes various algorithms
   for learning from data, while deep learning is a subset that uses
   neural networks with multiple layers...

💭 Reasoning Chain:
   🔧 Using web_search tool: {'query': 'machine learning vs deep learning'}
   💭 Let me analyze these search results to identify key differences...
   💭 Based on these sources, I can conclude that the main differences are...
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mcp_server_alpha --cov-report=html

# Run specific tests
pytest tests/unit/test_agent.py
```

## 🛠️ Tech Stack

- **LangGraph**: Workflow orchestration and agent framework
- **LangChain**: Tool integration and LLM interfaces
- **OpenAI**: GPT-4o-mini for reasoning (or any OpenAI model)
- **Pydantic**: Type-safe models and validation
- **Python 3.10+**: Modern async/await patterns

## 🔐 Configuration

### Environment Variables

The following environment variables configure the server:

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | Your OpenAI API key for GPT models |
| `POWER_AUTOMATE_WEBHOOK_URL` | ⚠️ Optional | Power Automate webhook URL for send_email tool |

**Setting Environment Variables:**

**Linux/macOS (bash/zsh):**
```bash
export OPENAI_API_KEY='sk-...'
export POWER_AUTOMATE_WEBHOOK_URL='https://prod-...'
```

**Windows (cmd):**
```cmd
set OPENAI_API_KEY=sk-...
set POWER_AUTOMATE_WEBHOOK_URL=https://prod-...
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-..."
$env:POWER_AUTOMATE_WEBHOOK_URL="https://prod-..."
```

**Docker:**
```bash
docker run -e OPENAI_API_KEY='sk-...' -e POWER_AUTOMATE_WEBHOOK_URL='https://...' -e GITHUB_TOKEN='ghp_...' agentic-mcp-gateway
```

**Claude Desktop Configuration:**

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

**Option 1: Using the dynamic startup script (Recommended)**

```json
{
  "mcpServers": {
    "agentic-mcp-gateway": {
      "command": "/absolute/path/to/agentic-mcp-gateway/start_mcp.sh",
      "env": {
        "OPENAI_API_KEY": "sk-...",
        "POWER_AUTOMATE_WEBHOOK_URL": "https://...",
        "GITHUB_TOKEN": "ghp_..."
      }
    }
  }
}
```

Replace `/absolute/path/to/agentic-mcp-gateway/start_mcp.sh` with the actual path:
- **Linux/macOS**: `/home/username/agentic-mcp-gateway/start_mcp.sh`
- **Windows**: `C:/Users/username/agentic-mcp-gateway/start_mcp.sh` (use forward slashes)

The `start_mcp.sh` script automatically:
- Detects its location
- Activates the virtual environment
- Starts the MCP server

**Option 2: Direct Python command**

```json
{
  "mcpServers": {
    "agentic-mcp-gateway": {
      "command": "python",
      "args": ["-m", "agentic_mcp_gateway.server"],
      "env": {
        "OPENAI_API_KEY": "sk-...",
        "POWER_AUTOMATE_WEBHOOK_URL": "https://...",
        "GITHUB_TOKEN": "ghp_..."
      }
    }
  }
}
```

Note: This requires the virtual environment to be activated or dependencies installed globally.

**Important**: After configuring Claude Desktop, completely quit and restart the application.

### Agent Parameters

```python
ResearchAgent(
    model="gpt-4o-mini",  # or "gpt-4o", "gpt-4-turbo"
    temperature=0.7,      # 0.0-1.0, higher = more creative
    api_key="sk-..."      # or use env var
)
```

## 🌟 Features

### Current
- ✅ **Agentic orchestration** with LangGraph for complex multi-step workflows
- ✅ **GitHub integration** for repository analysis and code review
- ✅ **Modular tool system** with plugin architecture
- ✅ **Multi-LLM support** via OpenAI (GPT-4o, GPT-4o-mini)
- ✅ **Reasoning visibility** with step-by-step execution tracking
- ✅ **Web search** capabilities (ready for API integration)
- ✅ **Data analysis** and statistical operations
- ✅ **Weather forecasts** via weather.gov API
- ✅ **Email integration** via Power Automate webhooks
- ✅ **Context-aware** conversations with state management

### Roadmap
- 🔄 Enhanced GitHub workflows (automated PR reviews, issue triage)
- 📄 Document analysis (PDF, Word, markdown parsing)
- 💾 Memory/RAG for long-term knowledge retention
- 🎨 Code visualization and diagram generation
- 🌊 Streaming progress updates
- 🔗 Additional integrations (Jira, Slack, databases)
- 🌐 Web UI for interactive workflows
- 🧪 Advanced testing and validation tools

## 🤝 Contributing

We welcome contributions! The modular architecture makes it easy to add new tools and features.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-tool`)
3. Add your tool or enhancement
4. Write tests for your changes
5. Submit a pull request

### Adding a New Tool

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions on:
- Tool architecture and patterns
- Plugin registration
- Testing requirements
- Code style guidelines

### Development Setup

```bash
# Clone and install
git clone https://github.com/tc-digital/agentic-mcp-gateway.git
cd agentic-mcp-gateway
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run linter
ruff check src/
```

## 📄 License

Proprietary - TC Digital

## 💬 Support

- Open an issue for bugs or questions
- Check examples/ directory for more usage patterns
- See docs/ for detailed documentation

---

**Built with ❤️ using LangGraph and OpenAI**

*Thanks for reading along - showcasing the power of modular, agentic architecture!*
