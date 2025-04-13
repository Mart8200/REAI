import streamlit as st
import pandas as pd
from openai import OpenAI

# --- Setup OpenAI client with secrets ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Extract user preferences using GPT ---
def extract_preferences(user_input):
    prompt = f"""Extract style and features from the following home preference description:

    "{user_input}"

    Return a JSON like this:
    {{
        "style": "...",
        "features": ["...", "..."]
    }}
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return eval(response.choices[0].message.content)

# --- Match Homes by Score ---
def find_matches(user_prefs, df):
    def match_score(row):
        style_score = 1 if user_prefs['style'].lower() in row['style'].lower() else 0
        feature_score = sum([1 for f in user_prefs['features'] if f in row['features']])
        return style_score * 2 + feature_score

    df['score'] = df.apply(match_score, axis=1)
    return df[df['score'] > 0].sort_values(by='score', ascending=False)

# --- Streamlit UI ---
st.set_page_config(page_title="Dream Home Matcher", layout="centered")
st.title("🏡 Dream Home Matcher")

st.markdown("Describe your dream home in natural language, and
