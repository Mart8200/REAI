import streamlit as st
import pandas as pd
import openai
import json

# --- Setup ---
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # New client setup

# --- Sample Preference Extraction ---
def extract_preferences(user_input):
    prompt = f"""Extract style and features from the following home preference description:

    "{user_input}"

    Return a JSON like this:
    {{
        "style": "...",
        "features": ["...", "..."]
    }}
    """
    response = client.chat.completions.create(  # Updated API call
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        return json.loads(response.choices[0].message.content)  # Updated response access
    except json.JSONDecodeError:
        st.error("Failed to parse AI response. Please try again.")
        return {"style": "", "features": []}

# --- Match Homes by Score ---
def find_matches(user_prefs, df):
    def match_score(row):
        style_score = 1 if user_prefs['style'].lower() in row['style'].lower() else 0
        row_features = row['features'].split('|')  # Split string into list
        feature_score = sum([1 for f in user_prefs['features'] if f in row_features])
        return style_score * 2 + feature_score

    df['score'] = df.apply(match_score, axis=1)
    return df[df['score'] > 0].sort_values(by='score', ascending=False)

# --- Streamlit UI ---
st.set_page_config(page_title="Dream Home Matcher", layout="centered")

# Add custom CSS to change background color to purple
st.markdown(
    """
    <style>
    .stApp {
        background-color: #800080;  /* Purple background */
        color: white;  /* Ensure text is readable */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🏡 Dream Home Matcher")
st.markdown("Describe your dream home in natural language, and we'll find matches just for you.")

# Ensure the text input field is visible with a placeholder
user_input = st.text_input(
    label="What does your dream house look like?",
    placeholder="e.g., A modern villa with a pool and mountain view",
    key="dream_home_input"
)

# Sample listing data (replace with real data or API call)
sample_data = pd.DataFrame([
    {
        'id': 1,
        'title': 'Modern Glass Villa',
        'style': 'minimalist',
        'features': 'glass walls|pool|mountain view',
        'location': 'Colorado',
        'price': 850000,
        'image': 'https://via.placeholder.com/400x300.png?text=Modern+Glass+Villa'
    },
    {
        'id': 2,
        'title': 'Beachside Cottage',
        'style': 'coastal',
        'features': 'patio|beachfront|skylight',
        'location': 'California',
        'price': 720000,
        'image': 'https://via.placeholder.com/400x300.png?text=Beachside+Cottage'
    },
    {
        'id': 3,
        'title': 'Charming Farmhouse',
        'style': 'cottage',
        'features': 'fireplace|garden|wood beams',
        'location': 'Texas',
        'price': 600000,
        'image': 'https://via.placeholder.com/400x300.png?text=Charming+Farmhouse'
    }
])

if user_input:
    with st.spinner("Analyzing your preferences with AI..."):
        try:
            prefs = extract_preferences(user_input)
            st.markdown(f"**Interpreted Preferences:** Style = `{prefs['style']}` | Features = `{', '.join(prefs['features'])}`")
            matches = find_matches(prefs, sample_data)

            if not matches.empty:
                st.subheader("🏠 Top Matching Homes")
                for _, row in matches.iterrows():
                    st.markdown(f"### {row['title']} — ${row['price']:,}")
                    st.write(f"**Style:** {row['style']}")
                    st.write(f"**Features:** {row['features']}")
                    st.image(row['image'])
                    st.markdown("---
