import streamlit as st
from openai import OpenAI
from datetime import datetime

st.set_page_config(page_title="RE Manifest AI", page_icon="🏠", layout="centered")

st.title("🏠 RE Manifest AI")
st.markdown("**Real Estate Agents Only** — Turn any listing note or market update into 10–20 ready-to-post posts that get leads.")

st.success("✅ **Super easy to use** — just paste your OpenAI key once (takes 20 seconds)")

with st.sidebar:
    st.header("How to use (takes 20 seconds)")
    st.write("1. Get your free OpenAI key here:")
    st.markdown("[🔗 Get Free OpenAI Key](https://platform.openai.com/api-keys)")
    st.write("2. Paste it below 👇")
    
    api_key = st.text_input("Your OpenAI API Key", type="password", value="")
    
    st.caption("New users get free credits. It costs almost nothing to use.")

    st.divider()
    st.header("Settings")
    num_posts = st.slider("Number of posts", 5, 25, 12)
    platform = st.selectbox("Platform", ["LinkedIn", "Facebook Groups", "Both"], index=0)

client = OpenAI(api_key=api_key) if api_key else None

def generate_posts(raw_text, num_posts, platform):
    if not client:
        return "Please add your OpenAI API key in the sidebar to generate posts."
    
    prompt = f"""
    You are a top real estate marketing expert. Write engaging, lead-generating posts for agents.

    Tone: Professional, friendly, local expert — never pushy.
    Rules:
    - Strong hook (question, stat, story)
    - Max 3-4 emojis
    - Short paragraphs
    - End with soft CTA (DM me, comment, share if looking)
    - Optimized for {platform}

    Generate exactly {num_posts} unique posts from this raw input:
    {raw_text}
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=5000
    )
    return response.choices[0].message.content

raw_input = st.text_area("Paste your raw listing notes, market update, or ideas here:", height=220,
                         placeholder="Just listed 3bed in Downtown... or Rates dropped 0.25% this week...")

if st.button("🚀 Generate Lead-Generating Posts", type="primary", use_container_width=True):
    if not raw_input:
        st.error("Paste your listing notes first")
    elif not api_key:
        st.error("Please add your OpenAI API key in the sidebar 👈")
    else:
        with st.spinner("Generating your posts..."):
            result = generate_posts(raw_input, num_posts, platform)
            st.success("✅ Here are your posts — copy & post them!")
            st.markdown(result)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            st.download_button("📥 Download as TXT", data=result, file_name=f"re_manifest_{timestamp}.txt", mime="text/plain")

st.caption("RE Manifest AI • 100% free for you • No monthly fees")
