import os

CLAUDE_37_SONNET_MODEL_ID = 'us.anthropic.claude-3-7-sonnet-20250219-v1:0'
CLAUDE_4_SONNET_MODEL_ID = 'us.anthropic.claude-sonnet-4-20250514-v1:0'
CLAUDE_4_OPUS_MODEL_ID = 'us.anthropic.claude-opus-4-20250514-v1:0'
CLAUDE_35_HAIKU_MODEL_ID = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'
CLAUDE_35_SONNET_MODEL_ID = 'us.anthropic.claude-3-5-sonnet-20241022-v2:0'
NOVA_RPO_MODEL_ID = 'us.amazon.nova-pro-v1:0'
NOVA_LITE_MODEL_ID = 'us.amazon.nova-lite-v1:0'

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "chromadb_path":os.path.abspath(os.path.join(os.path.dirname(__file__), "chroma")),
    "data_dir": "./FR1-data",
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings
    "llm_provider": "bedrock",
    "deep_think_llm": CLAUDE_4_SONNET_MODEL_ID,
    "quick_think_llm": CLAUDE_4_SONNET_MODEL_ID,
    # "deep_think_llm": "doubao-seed-1-6-thinking-250615",
    #  "deep_think_llm": "doubao-seed-1-6-250615",
    # "quick_think_llm": "doubao-seed-1-6-flash-250615",
    "backend_url": "https://ark.cn-beijing.volces.com/api/v3/",
    # Embedding settings
    # "embedding_provider": "openai",
    "embedding_provider": "bedrock",
    "embedding_model": "amazon.titan-embed-text-v2:0",
    "aws_region": "us-east-1",  # AWS region for Bedrock services
    # "embedding_model":"doubao-embedding-text-240715",
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Tool settings
    "online_tools": True,
}
