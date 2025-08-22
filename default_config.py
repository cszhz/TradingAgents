"""
Default Configuration for TradingAgents

This module contains all the default configuration settings for the TradingAgents framework.
It includes LLM model configurations, API settings, debate parameters, and tool settings.
"""

import os

# Claude Model IDs for AWS Bedrock
CLAUDE_37_SONNET_MODEL_ID = 'us.anthropic.claude-3-7-sonnet-20250219-v1:0'
CLAUDE_4_SONNET_MODEL_ID = 'us.anthropic.claude-sonnet-4-20250514-v1:0'
CLAUDE_4_OPUS_MODEL_ID = 'us.anthropic.claude-opus-4-20250514-v1:0'
CLAUDE_35_HAIKU_MODEL_ID = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'
CLAUDE_35_SONNET_MODEL_ID = 'us.anthropic.claude-3-5-sonnet-20241022-v2:0'

# Amazon Nova Model IDs
NOVA_RPO_MODEL_ID = 'us.amazon.nova-pro-v1:0'
NOVA_LITE_MODEL_ID = 'us.amazon.nova-lite-v1:0'

DEFAULT_CONFIG = {
    # Directory settings
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "chromadb_path": os.path.abspath(os.path.join(os.path.dirname(__file__), "chroma")),
    "data_dir": os.path.join(os.path.dirname(__file__), "dataflows/data_cache"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    
    # Search MCP settings (tavily, exa, or other search providers)
    "search_mcp_provider": "tavily",
    "search_mcp_api_key": os.getenv("TAVILY_API_KEY", None),
    
    # LLM provider and model settings
    "llm_provider": "bedrock",  # Options: "bedrock", "openai", "anthropic"
    "deep_think_llm": CLAUDE_37_SONNET_MODEL_ID,  # Model for complex reasoning tasks
    "quick_think_llm": CLAUDE_37_SONNET_MODEL_ID,  # Model for fast responses
    "backend_url": "https://ark.cn-beijing.volces.com/api/v3/",  # Custom API endpoint
    
    # Embedding model settings
    "embedding_provider": "bedrock",  # Options: "bedrock", "openai"
    "embedding_model": "amazon.titan-embed-text-v2:0",
    "aws_region": "us-east-1",  # AWS region for Bedrock services
    
    # Agent debate and discussion settings
    "max_debate_rounds": 1,      # Maximum rounds for research team debates
    "max_risk_discuss_rounds": 1, # Maximum rounds for risk management discussions
    "max_recur_limit": 100,      # Maximum recursion limit for agent interactions
    
    # Tool and data access settings
    "online_tools": True,  # Enable real-time data fetching vs cached data
}