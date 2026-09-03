import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered"
)

# Custom CSS for clean UI styling
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags instantly.")

# Sidebar for API Key input
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Groq API Key:", type="password")
    st.caption("Get a free key from [Groq Console](https://console.groq.com/).")

# Main Input Form
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox(
            "Platform",
            ["LinkedIn", "Instagram", "Twitter / X", "Facebook", "Blog Post"]
        )
        content_type = st.selectbox(
            "Content Type",
            ["Educational", "Promotional", "Storytelling", "Opinion / Thought Leadership", "Announcement"]
        )
        
    with col2:
        tone = st.selectbox(
            "Tone",
            ["Professional", "Casual & Friendly", "Persuasive", "Witty & Humorous", "Inspirational"]
        )
        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Developers, Small Business Owners, Gen Z"
        )

    topic = st.text_area(
        "Topic / Key Points",
        placeholder="e.g., 5 key benefits of using AI for workflow automation in 2026",
        height=100
    )

    submit = st.form_submit_button("🚀 Generate Content")

# Helper function to generate content
def generate_post(api_key, platform, content_type, tone, target_audience, topic):
    client = Groq(api_key=api_key)
    
    system_prompt = f"""
    You are an expert social media strategist and content generator. 
    Create a complete post strictly tailored to these specs:
    - Platform: {platform}
    - Content Type: {content_type}
    - Tone: {tone}
    - Target Audience: {target_audience if target_audience else 'General Audience'}
    
    Formatting rules:
    1. Include hook, main body, and clear Call to Action (CTA).
    2. Ensure character counts and structure match {platform}'s best practices.
    3. Include a section for relevant, high-traffic hashtags at the end.
    """

    user_prompt = f"Topic details: {topic}"

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content

# Processing logic
if submit:
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar to proceed.")
    elif not topic.strip():
        st.warning("Please enter a topic or key points for your post.")
    else:
        with st.spinner("Crafting your content..."):
            try:
                result = generate_post(api_key, platform, content_type, tone, target_audience, topic)
                st.success("Generated Successfully!")
                st.subheader("📌 Generated Content")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error generating content: {e}")
