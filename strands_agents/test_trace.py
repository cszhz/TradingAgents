from strands import Agent
from strands.telemetry import StrandsTelemetry
from strands_tools import current_time

import os,base64

from dotenv import load_dotenv
load_dotenv()

public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
langfuse_endpoint =  os.environ.get("LANGFUSE_HOST")
# Set up endpoint
if public_key and secret_key and langfuse_endpoint:
    print("-------------------start trace-------------------")
    otel_endpoint = langfuse_endpoint + "/api/public/otel"
    auth_token = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = otel_endpoint
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {auth_token}"
    strands_telemetry = StrandsTelemetry()
    strands_telemetry.setup_otlp_exporter()     # Send traces to OTLP endpoint
    strands_telemetry.setup_console_exporter()  # Print traces to console
    
agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    system_prompt="You are a helpful AI assistant",
    tools=[current_time]
)

print(agent("what is current time in beijing"))

