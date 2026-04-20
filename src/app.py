import json
import os
import re  # Added for cleaning JSON backticks
import uuid

import chromadb
import streamlit as st
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
CHROMA_DATA_PATH = "./chroma_data"
COLLECTION_NAME = "adhd_study_guides"
# Force gemini if preferred, otherwise read from env
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

# --- PROVIDER INITIALIZATION ---
anthropic_client = None
bedrock_client = None
gemini_client = None
gemini_model = None

if LLM_PROVIDER == "gemini":
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    # Use env var or default to stable 1.5 Flash
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    if not GEMINI_API_KEY:
        st.error("⚠️ Please set your GEMINI_API_KEY in the .env file")
        st.stop()

    try:
        # Initialize the new Gemini client
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        gemini_model = GEMINI_MODEL
    except Exception as e:
        st.error(f"⚠️ Failed to initialize Gemini: {str(e)}")
        st.stop()
# (Rest of your Anthropic/Bedrock init code stays the same...)

# --- DB INITIALIZATION ---
client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
embedding_func = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_or_create_collection(
    name=COLLECTION_NAME, embedding_function=embedding_func
)


# --- UTILITY: CLEAN JSON ---
def clean_json_string(text):
    """Removes markdown code blocks if the model accidentally includes them."""
    return re.sub(r"```json\n?|```", "", text).strip()


# --- LLM FUNCTION ---
def call_llm_api(text):
    prompt = f"""You are an ADHD-friendly study assistant. Analyze the text and create a study guide.

    REQUIREMENTS:
    - Use **markdown bold** on key concepts in every bullet
    - Start each bullet with an emoji (🧠, ⚡, ✅)
    - Keep sentences short and clear (under 15 words)

    Return ONLY a valid JSON object with this exact structure (no additional text):
    {{
      "summary": "2-3 brain-friendly sentences",
      "bullets": ["🧠 **Key** concept here", "⚡ Another **important** point", "✅ Final **key** fact"],
      "vocabulary": {{"Term": "Simple Definition"}}
    }}

    Text to analyze:
    {text}"""

    try:
        if LLM_PROVIDER == "gemini":
            # Use the new Gemini API
            response = gemini_client.models.generate_content(
                model=gemini_model,
                contents=prompt,
                config={
                    "temperature": 0.3,
                    "max_output_tokens": 2048,
                    "response_mime_type": "application/json",
                },
            )
            response_text = clean_json_string(response.text)

            # Debug: Show what we received (optional - remove in production)
            with st.expander("Debug: Raw Response"):
                st.code(response_text)

            # Try to parse the JSON
            try:
                guide = json.loads(response_text)

                # Validate ADHD requirements
                has_bolding = any("**" in bullet for bullet in guide.get("bullets", []))
                has_emojis = any(
                    any(emoji in bullet for emoji in "🧠⚡✅🏛️📆")
                    for bullet in guide.get("bullets", [])
                )

                if not has_bolding:
                    st.warning("⚠️ Output missing bionic bolding - regenerate for better accessibility")
                if not has_emojis:
                    st.warning("⚠️ Output missing emoji anchors - regenerate for better accessibility")

                return guide
            except json.JSONDecodeError as json_err:
                st.error(f"JSON Parse Error: {str(json_err)}")
                st.code(response_text)
                # Return a fallback
                return {
                    "summary": "Error: Received invalid JSON from model",
                    "bullets": ["⚠️ Could not parse response"],
                    "vocabulary": {},
                }

        # (Your existing Bedrock/Anthropic logic follows...)

    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return {
            "summary": f"Technical Error: {str(e)}",
            "bullets": ["⚠️ Could not generate guide"],
            "vocabulary": {},
        }


# --- UI LAYOUT ---
st.set_page_config(page_title="ADHD Study Buddy", page_icon="🧠")
st.title("🧠 ADHD Study Buddy")
if LLM_PROVIDER == "gemini":
    st.caption(f"Currently using: {GEMINI_MODEL.upper()}")
else:
    st.caption(f"Currently using: {LLM_PROVIDER.upper()}")

user_input = st.text_area(
    "Paste your textbook text here:",
    height=200,
    placeholder="E.g. A long paragraph about Photosynthesis...",
)

if st.button("Generate Study Guide", use_container_width=True):
    if not user_input.strip():
        st.warning("Input is empty!")
    else:
        with st.spinner("Brainstorming..."):
            # 1. SEARCH CACHE
            results = collection.query(query_texts=[user_input], n_results=1)

            if results["ids"][0] and results["distances"][0][0] < 0.35:
                st.success("🎯 Found a similar topic in your notes!")
                study_guide = json.loads(results["metadatas"][0][0]["guide_json"])
            else:
                # 2. GENERATE
                study_guide = call_llm_api(user_input)
                # 3. CACHE
                collection.add(
                    documents=[user_input],
                    metadatas=[{"guide_json": json.dumps(study_guide)}],
                    ids=[str(uuid.uuid4())],
                )

        # 4. DISPLAY
        st.subheader("Your Study Guide")
        st.info(study_guide["summary"])

        # Columns for ADHD-friendly scannability
        col1, col2 = st.columns([2, 1])
        with col1:
            for bullet in study_guide["bullets"]:
                st.write(bullet)
        with col2:
            st.write("**Keywords**")
            for term, defn in study_guide["vocabulary"].items():
                st.caption(f"**{term}**: {defn}")

# --- SIDEBAR ---
with st.sidebar:
    st.title("Settings")
    st.metric("Total Guides Saved", collection.count())
    if st.button("Clear History"):
        client.delete_collection(COLLECTION_NAME)
        st.rerun()
