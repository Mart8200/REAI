
# Dream Home Matcher 🏡

This is a Streamlit app that lets users describe their dream home in natural language and returns matching properties using AI.

## How it Works

1. Enter your dream home description.
2. The app uses GPT to extract preferences (style, features).
3. Matches are ranked based on style + features.
4. Results are displayed with images and pricing.

## Setup

- Add your OpenAI API key to Streamlit Cloud secrets:
```toml
OPENAI_API_KEY = "your-api-key"
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run dream_home_matcher.py
```
