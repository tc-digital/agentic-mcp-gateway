#!/usr/bin/env python3
"""
GitHub Analysis Demo for Agentic MCP Gateway

This demo showcases the GitHub integration capabilities, including:
1. Repository information retrieval
2. Repository search
3. Issue listing and analysis
4. Language statistics

Usage:
    python examples/github_demo.py
"""
import asyncio
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agentic_mcp_gateway.tools.github import (
    github_list_issues,
    github_repo_info,
    github_repo_languages,
    github_search_repos,
)


def print_separator(title: str = "") -> None:
    """Print a visual separator."""
    if title:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}\n")
    else:
        print(f"{'─'*70}\n")


async def demo_repo_info() -> None:
    """Demonstrate repository information retrieval."""
    print_separator("Demo 1: Repository Information")
    
    # Example: Analyze this repository
    owner = "tc-digital"
    repo = "agentic-mcp-gateway"
    
    print(f"📦 Getting information for {owner}/{repo}...")
    result = await github_repo_info(owner, repo)
    
    if result["success"]:
        info = result["result"]
        print(f"\n✅ Repository: {info['full_name']}")
        print(f"   Description: {info['description']}")
        print(f"   ⭐ Stars: {info['stars']}")
        print(f"   🍴 Forks: {info['forks']}")
        print(f"   🐛 Open Issues: {info['open_issues']}")
        print(f"   💻 Primary Language: {info['language']}")
        print(f"   🌐 URL: {info['html_url']}")
        if info['topics']:
            print(f"   🏷️  Topics: {', '.join(info['topics'])}")
    else:
        print(f"\n❌ Error: {result['error']}")
    
    print_separator()


async def demo_search_repos() -> None:
    """Demonstrate repository search."""
    print_separator("Demo 2: Repository Search")
    
    query = "machine learning python"
    print(f"🔍 Searching for repositories: '{query}'...")
    
    result = await github_search_repos(query, max_results=3)
    
    if result["success"]:
        print(f"\n✅ Found {result['details']['total_count']} total repositories")
        print(f"   Showing top {len(result['result'])} results:\n")
        
        for i, repo in enumerate(result["result"], 1):
            print(f"   {i}. {repo['full_name']}")
            print(f"      ⭐ {repo['stars']} stars | 💻 {repo['language']}")
            print(f"      {repo['description'][:80]}...")
            print(f"      🌐 {repo['html_url']}\n")
    else:
        print(f"\n❌ Error: {result['error']}")
    
    print_separator()


async def demo_list_issues() -> None:
    """Demonstrate issue listing."""
    print_separator("Demo 3: Repository Issues")
    
    # Example: List issues for a popular repository
    owner = "python"
    repo = "cpython"
    
    print(f"📋 Listing open issues for {owner}/{repo}...")
    result = await github_list_issues(owner, repo, state="open", max_results=5)
    
    if result["success"]:
        issues = result["result"]
        print(f"\n✅ Found {result['details']['count']} issues:\n")
        
        for issue in issues:
            labels = f" [{', '.join(issue['labels'])}]" if issue['labels'] else ""
            print(f"   #{issue['number']}: {issue['title']}{labels}")
            print(f"      👤 Author: {issue['author']} | 💬 {issue['comments']} comments")
            print(f"      🌐 {issue['html_url']}\n")
    else:
        print(f"\n❌ Error: {result['error']}")
    
    print_separator()


async def demo_repo_languages() -> None:
    """Demonstrate language statistics."""
    print_separator("Demo 4: Repository Languages")
    
    owner = "tc-digital"
    repo = "agentic-mcp-gateway"
    
    print(f"💻 Getting language statistics for {owner}/{repo}...")
    result = await github_repo_languages(owner, repo)
    
    if result["success"]:
        languages = result["result"]
        print(f"\n✅ Language breakdown:\n")
        
        for lang in languages:
            bar_length = int(lang['percentage'] / 2)  # Scale to max 50 chars
            bar = '█' * bar_length
            print(f"   {lang['language']:15} {lang['percentage']:5.1f}% {bar}")
        
        print(f"\n   Total: {result['details']['total_bytes']:,} bytes")
    else:
        print(f"\n❌ Error: {result['error']}")
    
    print_separator()


async def demo_workflow() -> None:
    """Demonstrate an end-to-end workflow: analyzing a repository."""
    print_separator("Demo 5: Complete Repository Analysis Workflow")
    
    owner = "openai"
    repo = "openai-python"
    
    print(f"🔬 Complete analysis of {owner}/{repo}\n")
    
    # Step 1: Get repo info
    print("Step 1: Fetching repository information...")
    info_result = await github_repo_info(owner, repo)
    if info_result["success"]:
        info = info_result["result"]
        print(f"   ✅ Repository: {info['full_name']}")
        print(f"   📝 {info['description']}")
        print(f"   ⭐ {info['stars']} stars, 🍴 {info['forks']} forks\n")
    
    # Step 2: Get languages
    print("Step 2: Analyzing programming languages...")
    lang_result = await github_repo_languages(owner, repo)
    if lang_result["success"]:
        top_lang = lang_result["result"][0]
        print(f"   ✅ Primary language: {top_lang['language']} ({top_lang['percentage']:.1f}%)\n")
    
    # Step 3: Check for issues
    print("Step 3: Checking open issues...")
    issues_result = await github_list_issues(owner, repo, state="open", max_results=3)
    if issues_result["success"]:
        print(f"   ✅ {issues_result['details']['count']} open issues found")
        if issues_result["result"]:
            print(f"   Latest: #{issues_result['result'][0]['number']} - {issues_result['result'][0]['title']}")
    
    print(f"\n🎉 Analysis complete!")
    print_separator()


async def main() -> None:
    """Run all demos."""
    print("\n" + "="*70)
    print("  🐙 Agentic MCP Gateway - GitHub Integration Demo")
    print("="*70)
    
    # Check for GitHub token
    token = os.getenv("GITHUB_TOKEN")
    if token:
        print("✅ GITHUB_TOKEN is configured (authenticated requests)")
    else:
        print("⚠️  GITHUB_TOKEN not set (rate limits apply)")
        print("   Set GITHUB_TOKEN for higher rate limits and private repo access")
    
    try:
        # Run individual demos
        await demo_repo_info()
        await asyncio.sleep(1)  # Be nice to the API
        
        await demo_search_repos()
        await asyncio.sleep(1)
        
        await demo_list_issues()
        await asyncio.sleep(1)
        
        await demo_repo_languages()
        await asyncio.sleep(1)
        
        # Run complete workflow demo
        await demo_workflow()
        
        print("\n✨ All demos completed successfully!")
        print("\n💡 Next steps:")
        print("   • Use these tools in the reasoning agent for complex workflows")
        print("   • Combine with other tools (web search, analysis, etc.)")
        print("   • Build custom workflows for code review and repository analysis")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error running demos: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
