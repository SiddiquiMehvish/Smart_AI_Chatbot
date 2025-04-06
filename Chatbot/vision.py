from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
import io

# Load API key from environment
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ GOOGLE_API_KEY is missing. Please check your configuration.")
else:
    genai.configure(api_key=api_key)


# Function to process image and generate AI response
def get_gemini_response(input_text, image):
    model = genai.GenerativeModel('gemini-1.5-flash')

    try:
        # Convert image to bytes if uploaded
        image_data = None
        if image:
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_data = image_bytes.getvalue()
            image = Image.open(io.BytesIO(image_data))  # Convert bytes back to image format

        # Generate response
        with st.spinner("⏳ AI is analyzing the Query... Please wait."):
            if input_text and image_data:
                response = model.generate_content([input_text, image])
            elif image_data:
                response = model.generate_content(image)
            else:
                response = model.generate_content(input_text)

        return response.text if hasattr(response, "text") else str(response)

    except Exception as e:
        return f"❌ Error: {str(e)}"


# --- STREAMLIT UI ---
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for professional background and layout
st.markdown(
    """
    <style>
        body {
            background-color: #e8f0f2;
            font-family: Arial, sans-serif;
        }
        .sidebar .sidebar-content {
            background-color: #2c3e50;
            color: white;
        }
        .sidebar .sidebar-content a {
            color: #1abc9c;
        }
        .stButton>button {
            background-color: #1abc9c;
            color: white;
            border-radius: 10px;
            width: 100%;
            padding: 10px;
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 🤖 AI Chatbot")
    st.image("ai.jpg", width=50)
    st.markdown("### 🚀 Unlock AI-Powered Insights")
    st.markdown("- 🤖 **Smart AI Chatbot**")
    st.markdown("- 📷 **Upload an image**")
    st.markdown("- 💬 **Enter a description (optional)**")
    st.markdown("- 🚀 **Click 'Analyze'**")
    st.markdown("- 🧠 **View AI-generated insights**")
    st.write("---")
    st.markdown("💡 **Powered by Google's Gemini AI**")

# --- MAIN LAYOUT ---
st.title("🤖 AI Chatbot")
st.markdown("Chat with AI and analyze images effortlessly.")

# Create columns for refined layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📂 Upload an Image")
    uploaded_file = st.file_uploader("Choose an image:", type=["jpg", "jpeg", "png"])
    image = None
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="📷 Uploaded Image", use_column_width=True, output_format="PNG")

with col2:
    st.markdown("### 💬 Provide a Text Prompt (Optional)")
    input_text = st.text_area("Describe what you want AI to analyze", height=120)

# Centered Analyze Button with Full Width
st.markdown("<br>", unsafe_allow_html=True)
analyze_button = st.button("🚀 Search Query", use_container_width=True)

if analyze_button:
    if not api_key:
        st.error("⚠️ API Key is missing. Please configure it.")
    elif not uploaded_file and not input_text:
        st.warning("⚠️ Please upload an image or provide a text prompt.")
    else:
        response = get_gemini_response(input_text, image)
        st.success("✅ AI Analysis Complete!")
        st.subheader("🔍 AI-Generated Insights:")
        st.write(response)