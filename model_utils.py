"""
Model Utilities for TradingAgents

This module provides utility functions for creating and managing LLM models,
as well as file I/O operations for saving and reading analysis results.
"""

import os
import boto3
from botocore.config import Config
from dotenv import load_dotenv
from strands.models.openai import OpenAIModel
from strands.models import BedrockModel
from default_config import DEFAULT_CONFIG

# Load environment variables
load_dotenv()

# Claude Model IDs (duplicated from default_config for convenience)
CLAUDE_37_SONNET_MODEL_ID = 'us.anthropic.claude-3-7-sonnet-20250219-v1:0'
CLAUDE_4_SONNET_MODEL_ID = 'us.anthropic.claude-sonnet-4-20250514-v1:0'
CLAUDE_4_OPUS_MODEL_ID = 'us.anthropic.claude-opus-4-20250514-v1:0'
CLAUDE_35_HAIKU_MODEL_ID = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'
CLAUDE_35_SONNET_MODEL_ID = 'us.anthropic.claude-3-5-sonnet-20241022-v2:0'
NOVA_RPO_MODEL_ID = 'us.amazon.nova-pro-v1:0'
NOVA_LITE_MODEL_ID = 'us.amazon.nova-lite-v1:0'

# AWS Boto3 client configuration with timeouts and retries
boto_client_config = Config(
    read_timeout=1800,      # 30 minutes read timeout
    connect_timeout=900,    # 15 minutes connect timeout
    retries=dict(max_attempts=3, mode="adaptive"),
)


def get_model(provider='bedrock', model_id=CLAUDE_37_SONNET_MODEL_ID, thinking=True, 
              temperature=0.7, max_tokens=16000):
    """
    Create and return an LLM model instance based on the specified provider.
    
    Args:
        provider (str): The model provider ('bedrock' or 'openai')
        model_id (str): The specific model ID to use
        thinking (bool): Whether to enable thinking mode for supported models
        temperature (float): Sampling temperature for response generation
        max_tokens (int): Maximum tokens in the response
        
    Returns:
        Model instance (BedrockModel or OpenAIModel)
    """
    if provider == "bedrock":
        # Create AWS session with credentials
        session = boto3.Session(
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name='us-west-2'
        )
        
        # Configure thinking mode for supported models
        additional_request_fields = {}
        if thinking:
            additional_request_fields = {
                "thinking": {
                    "type": "enabled",
                    "budget_tokens": 4096,
                }
            }
        
        # Add beta features for Claude 4 models
        if model_id in [CLAUDE_4_SONNET_MODEL_ID, CLAUDE_4_OPUS_MODEL_ID]:
            additional_request_fields['anthropic_beta'] = ["interleaved-thinking-2025-05-14"]
        
        # Configure caching for supported models
        cache_tools = None
        if model_id in [CLAUDE_4_SONNET_MODEL_ID, CLAUDE_4_OPUS_MODEL_ID, 
                       CLAUDE_37_SONNET_MODEL_ID, CLAUDE_35_SONNET_MODEL_ID]:
            cache_tools = "default"
        
        # Adjust temperature for thinking models
        if model_id in [CLAUDE_4_SONNET_MODEL_ID, CLAUDE_4_OPUS_MODEL_ID, 
                       CLAUDE_37_SONNET_MODEL_ID] and thinking:
            temperature = 1.0
            
        # Disable thinking for models that don't support it
        if model_id not in [CLAUDE_4_SONNET_MODEL_ID, CLAUDE_4_OPUS_MODEL_ID, 
                           CLAUDE_37_SONNET_MODEL_ID] and thinking:
            additional_request_fields = {}
        
        return BedrockModel(
            model_id=model_id,
            boto_session=session,
            cache_tools=cache_tools,
            cache_prompt="default",
            max_tokens=max_tokens,
            temperature=temperature,
            boto_client_config=boto_client_config,
            additional_request_fields=additional_request_fields,
        )
    else:
        # Use OpenAI-compatible API
        config = DEFAULT_CONFIG
        return OpenAIModel(
            client_args={
                "api_key": os.environ.get("OPENAI_API_KEY"),
                "base_url": config["backend_url"],
            },
            model_id=config["deep_think_llm"],
            params={
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
        )


def save_as_file(text, working_dir, prefix='', file_name=''):
    """
    Save text content to a file in the specified directory structure.
    
    Args:
        text (str): Content to save
        working_dir (str): Base working directory
        prefix (str): Subdirectory prefix (usually ticker_date)
        file_name (str): Name of the file to save
    """
    # Create directory if it doesn't exist
    full_dir = os.path.join(working_dir, prefix)
    if not os.path.exists(full_dir):
        os.makedirs(full_dir, exist_ok=True)
    
    # Write content to file
    file_path = os.path.join(full_dir, file_name)
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(text)


def read_file(working_dir, prefix='', file_name=''):
    """
    Read text content from a file in the specified directory structure.
    
    Args:
        working_dir (str): Base working directory
        prefix (str): Subdirectory prefix (usually ticker_date)
        file_name (str): Name of the file to read
        
    Returns:
        str: File content
        
    Raises:
        ValueError: If the file doesn't exist
    """
    file_path = os.path.join(working_dir, prefix, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError(f"File not found: {file_path}")