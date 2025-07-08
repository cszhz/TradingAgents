from strands import Agent
from strands.telemetry import StrandsTelemetry
from strands_tools import current_time

import os,base64

from dotenv import load_dotenv
load_dotenv()

from dataflows.interface import get_stock_news_openai
from dataflows.googlenews_utils import getNewsData

# print (get_stock_news_openai("AMZN","2025-07-08"))

print(getNewsData("NVIDIA's stock","2025-07-01","2025-07-02"))