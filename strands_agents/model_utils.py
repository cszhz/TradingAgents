from dotenv import load_dotenv
from default_config import DEFAULT_CONFIG
import boto3
import os
from botocore.config import Config
from strands.models.openai import OpenAIModel
from strands.models import BedrockModel
load_dotenv()

CLAUDE_37_SONNET_MODEL_ID = 'us.anthropic.claude-3-7-sonnet-20250219-v1:0'
CLAUDE_4_SONNET_MODEL_ID = 'us.anthropic.claude-sonnet-4-20250514-v1:0'
CLAUDE_4_OPUS_MODEL_ID = 'us.anthropic.claude-opus-4-20250514-v1:0'
CLAUDE_35_HAIKU_MODEL_ID = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'
CLAUDE_35_SONNET_MODEL_ID = 'us.anthropic.claude-3-5-sonnet-20241022-v2:0'
NOVA_RPO_MODEL_ID = 'us.amazon.nova-pro-v1:0'
NOVA_LITE_MODEL_ID = 'us.amazon.nova-lite-v1:0'

boto_client_config=Config(
            read_timeout=1800,
            connect_timeout=900,
            retries=dict(max_attempts=3, mode="adaptive"),
            )

def get_model(provider='bedrock',model_id=CLAUDE_37_SONNET_MODEL_ID,thinking=True,temperature=0.7,max_tokens=16000):
    if provider == "bedrock":
        session = boto3.Session(
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name='us-west-2'
        )
        additional_request_fields = {
            "thinking": {
                "type":"enabled" if thinking else 'disabled',
                "budget_tokens": 4096,
            }
        } if thinking else {}
        if model_id in [CLAUDE_4_SONNET_MODEL_ID,CLAUDE_4_OPUS_MODEL_ID]:
            additional_request_fields['anthropic_beta'] = ["interleaved-thinking-2025-05-14"]
        if model_id in [CLAUDE_4_SONNET_MODEL_ID,CLAUDE_4_OPUS_MODEL_ID,CLAUDE_37_SONNET_MODEL_ID,CLAUDE_35_SONNET_MODEL_ID]:
            cache_tools = "default"
        else:
            cache_tools = None
        if model_id in [CLAUDE_4_SONNET_MODEL_ID,CLAUDE_4_OPUS_MODEL_ID,CLAUDE_37_SONNET_MODEL_ID] and thinking:
            temperature = 1.0
            
        if model_id not in [CLAUDE_4_SONNET_MODEL_ID,CLAUDE_4_OPUS_MODEL_ID,CLAUDE_37_SONNET_MODEL_ID] and thinking:
            additional_request_fields = {}
        return BedrockModel(
                    model_id=model_id,
                    boto_session=session,
                    cache_tools=cache_tools,
                    cache_prompt="default",
                    max_tokens=max_tokens,
                    temperature=temperature,
                    boto_client_config = boto_client_config,
                    additional_request_fields=additional_request_fields,
                )
    else:
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
    