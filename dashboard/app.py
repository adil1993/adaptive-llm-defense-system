import streamlit as st
import requests
import json
import pandas as pd

API_URL = "http://localhost:8000/analyze"

st.set_page_config(page_title="LLM Security Dashboard", layout="wide")
st.title("🔐 Adaptive LLM Defense System")

prompt = st.text_area("Enter prompt:")

if st.button("Analyze"):
    if not prompt.strip():
        st.warning("Please enter a prompt")
    else:
        with st.spinner("Analyzing..."):
            try:
                res = requests.post(API_URL, params={"prompt": prompt}, timeout=60)

                if res.status_code != 200:
                    st.error(f"API Error: {res.status_code}")
                    st.text(res.text)
                else:
                    result = res.json()

                    if result.get("status") == "blocked":
                        st.error("🚫 BLOCKED")
                    else:
                        st.success("✅ ALLOWED")

                    if result.get("normalized"):
                        st.subheader("Normalized Prompt")
                        st.write(result["normalized"])

                    st.subheader("Full Response")
                    st.json(result)

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend")

            except requests.exceptions.Timeout:
                st.error("Request timed out (backend too slow)")

            except Exception as e:
                st.error(str(e))

st.header("Attack Memory")

try:
    with open("../data/attacks.json") as f:
        data = json.load(f)

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df[["prompt"]])
        st.metric("Stored Attacks", len(df))
    else:
        st.info("No attack data yet")

except:
    st.write("No attack data yet")