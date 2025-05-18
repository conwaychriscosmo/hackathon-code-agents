from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.tools import tool


import os
from typing import Dict
from PIL import Image
import requests
from io import BytesIO
from arize.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor
ARIZE_SPACE_ID = os.getenv("SPACE_ID", "your space id")
ARIZE_API_KEY = os.getenv("ARIZE_API_KEY", "your arize apie key")
ARIZE_PROJECT_NAME = os.getenv("PROJECT_NAME", "Don Draper")

#arize :)
tracer_provider = register(
    space_id = ARIZE_SPACE_ID, # in app space settings page
    api_key = ARIZE_API_KEY, # in app space settings page
    project_name = ARIZE_PROJECT_NAME, # name this to whatever you would like
)
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

# Step 1: Load LLM
llm = ChatOpenAI(temperature=0.7)


# ---- PROMPTS ----

brief_template = PromptTemplate.from_template("""
You are a creative marketing strategist. Based on the campaign brief below, generate a structured marketing campaign with the following clearly labeled sections:

### Landing page copy:
- Headline:
- Subhead:
- Features: (bullet points)
- Call to Action (CTA):

### Ad copy:
Provide 3 ad variants suitable for Facebook and Instagram. Each should include:
- Hook
- Description
- Call to Action

### Email sequence:
Create a 3-part email sequence:
- Email 1: Subject, Body
- Email 2: Subject, Body
- Email 3: Subject, Body

Make sure each section begins with the exact heading so it can be parsed programmatically.

Brief:
{brief}
""")

image_prompt_template = PromptTemplate.from_template("""
Summarize this marketing campaign into a single visual scene description for AI image generation:

{campaign_assets}

Return only a concise description suitable for DALL·E (e.g., "A robot helping a lawyer in a modern office, photorealistic").
""")

# ---- TOOLS ----

@tool
def generate_campaign_assets(brief: str):
    """Generates full campaign content from a marketing brief."""
    prompt = brief_template.format(brief=brief)
    return llm.predict(prompt)

@tool
def generate_image_prompt(campaign_assets: str):
    """Creates a visual description for an AI image based on marketing assets."""
    prompt = image_prompt_template.format(campaign_assets=campaign_assets)
    return llm.predict(prompt)

@tool
def generate_image(prompt: str) -> str:
    """Generates an image URL from a DALL·E prompt."""
    dalle_url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json"
    }
    json_data = {
        "prompt": prompt,
        "n": 1,
        "size": "512x512"
    }
    response = requests.post(dalle_url, headers=headers, json=json_data)
    image_url = response.json()["data"][0]["url"]
    return image_url

# ---- AGENT SETUP ----

tools = [
    Tool(name="GenerateCampaignAssets", func=generate_campaign_assets, description="Create a marketing campaign."),
    Tool(name="GenerateImagePrompt", func=generate_image_prompt, description="Create a visual scene description."),
    Tool(name="GenerateImage", func=generate_image, description="Generate a campaign image."),
]

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# ---- RUN FULL CAMPAIGN ----

def run_campaign(prompt: str):
    print("⚡ Generating Campaign...")
    campaign_assets = generate_campaign_assets.invoke(prompt)

    print("\n📣 Marketing Copy:\n", campaign_assets)

    image_prompt = generate_image_prompt.invoke(campaign_assets)
    print("\n🎨 Image Prompt:\n", image_prompt)

    image_url = generate_image.invoke(image_prompt)
    print("\n🖼️ Image URL:\n", image_url)

    return {
        "text": campaign_assets,
        "image_prompt": image_prompt,
        "image_url": image_url
    }