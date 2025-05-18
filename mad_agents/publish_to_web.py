import os
from jinja2 import Template

# Template for a simple, elegant landing page
LANDING_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <style>
        body { font-family: sans-serif; max-width: 700px; margin: auto; padding: 40px; line-height: 1.6; }
        h1 { font-size: 2.5em; }
        img { max-width: 100%; border-radius: 12px; margin-top: 20px; }
        .cta { background-color: #0070f3; color: white; padding: 12px 20px; border: none; border-radius: 8px; font-size: 1.2em; text-decoration: none; }
    </style>
</head>
<body>
    <h1>{{ headline }}</h1>
    <h3>{{ subhead }}</h3>

    {% if image_url %}
    <img src="{{ image_url }}" alt="Campaign Image">
    {% endif %}

    <h2>Features:</h2>
    <ul>
        {% for feature in features %}
        <li>{{ feature }}</li>
        {% endfor %}
    </ul>

    <a class="cta" href="#">Try It Free for 7 Days</a>

    <h3 style="margin-top: 60px;">Sample Ad Copy:</h3>
    {% for ad in ads %}
    <p><em>{{ ad }}</em></p>
    {% endfor %}
</body>
</html>
"""
def extract_section(text, start_key, end_key):
    """Safely extract text between two markers."""
    try:
        lower_text = text.lower()
        start_index = lower_text.index(start_key.lower()) + len(start_key)
        end_index = lower_text.index(end_key.lower(), start_index)
        return text[start_index:end_index].strip()
    except ValueError:
        print(f"⚠️ Section markers not found: '{start_key}' → '{end_key}'")
        return ""
def publish_to_web(campaign_text, image_url, output_path="generated_landing_page.html"):
    headline_block = extract_section(campaign_text, "Landing page copy:", "Ad copy:")
    ad_block = extract_section(campaign_text, "Ad copy:", "Email sequence:")

    if not headline_block:
        raise ValueError("Missing or malformed 'Landing page copy' section.")
    if not ad_block:
        raise ValueError("Missing or malformed 'Ad copy' section.")

    # Parse headline and features
    lines = [line.strip() for line in headline_block.splitlines() if line.strip()]
    title = lines[0]
    subhead = lines[1] if len(lines) > 1 else ""
    features = [line.strip("-• ") for line in lines[2:] if line.startswith(("-", "•"))]

    # Parse ads
    ads = [line.strip("-• ") for line in ad_block.splitlines() if line.strip()]

    # Render HTML
    template = Template(LANDING_PAGE_TEMPLATE)
    html = template.render(
        title=title,
        headline=title,
        subhead=subhead,
        features=features,
        ads=ads,
        image_url=image_url
    )

    with open(output_path, "w") as f:
        f.write(html)

    print(f"✅ Landing page written to {output_path}")
