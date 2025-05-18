from notion_client import Client
import os

# Load your Notion secret (from environment variable or paste it here)
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "your notion token")
PAGE_ID = "1f71d3a5df2080a5a030fefdb8ff61ce"  # Can be full UUID or shortened

notion = Client(auth=NOTION_TOKEN)

def split_text_into_blocks(text):
    """
    Converts raw text into Notion paragraph blocks.
    """
    paragraphs = text.split("\n\n")
    return [{
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {"content": para}
            }]
        }
    } for para in paragraphs if para.strip()]

def publish_campaign_to_notion(campaign_text: str):
    blocks = split_text_into_blocks(campaign_text)
    response = notion.blocks.children.append(
        block_id=PAGE_ID,
        children=blocks
    )
    print("✅ Published to Notion:", response)
