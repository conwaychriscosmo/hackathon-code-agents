import streamlit as st
from mad_agents.don_draper import run_campaign
from mad_agents.publish_to_notion import publish_campaign_to_notion

st.set_page_config(page_title="Don Draper AI", layout="centered")
st.title("🕴️ Don Draper, Ad Agent")

user_input = st.text_input("Describe your product or campaign idea:", placeholder="e.g. launch a zero-waste cleaning brand")

if st.button("Generate Campaign") and user_input:
    with st.spinner("Don's having a whiskey and thinking..."):
        result = run_campaign(user_input)
        st.subheader("📰 Campaign Generated")
        st.text(result["text"])
        
        if st.button("📤 Publish to Notion"):
            publish_campaign_to_notion(result["text"])
            st.success("Published to Notion!")

