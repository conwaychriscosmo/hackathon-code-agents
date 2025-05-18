import streamlit as st
from mad_agents.don_draper import run_campaign
from mad_agents.publish_to_notion import publish_campaign_to_notion
from mad_agents.publish_to_web import html_string

st.set_page_config(page_title="Don Draper AI", layout="centered")
st.title("🕴️ Don Draper, Ad Agent")

user_input = st.text_input("Describe your product or campaign idea:", placeholder="e.g. launch a zero-waste cleaning brand")

if st.button("Generate Campaign") and user_input:
    with st.spinner("Don's having a whiskey and thinking..."):
        result = run_campaign(user_input)
        st.subheader("📰 Campaign Generated")
        landing_page = html_string(result["text"], result["image_url"])
        st.html(landing_page)
        st.text(result["text"])
        
        if st.button("📤 Publish to Notion"):
            publish_campaign_to_notion(result["text"])
            st.success("Published to Notion!")
        st.download_button("download landing page", landing_page, file_name="landing_page.html")


