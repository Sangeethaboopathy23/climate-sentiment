import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Page settings
st.set_page_config(page_title="Climate Policy Sentiment", layout="wide")
st.title("🌍 Climate Change Policy — Tweet Sentiment Dashboard")

# Map numeric labels
label_map = {1: "Positive", 0: "Neutral", -1: "Negative"}

# 🔹 Load dataset automatically (no manual upload)
df = pd.read_csv("twitter_sentiment_data_clean.csv")
df["Sentiment"] = df["sentiment"].map(label_map)

# Sidebar filters
st.sidebar.header("Filters")
keyword = st.sidebar.text_input("Keyword filter (optional)", "")
sentiment_choice = st.sidebar.multiselect(
    "Choose Sentiments", ["Positive", "Neutral", "Negative"], 
    default=["Positive", "Neutral", "Negative"]
)

# Apply filters
if keyword:
    df = df[df["clean_message"].str.contains(keyword, case=False, na=False)]
df = df[df["Sentiment"].isin(sentiment_choice)]

# Summary metrics
st.subheader("📊 Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tweets", len(df))
col2.metric("Positive", (df["Sentiment"] == "Positive").sum())
col3.metric("Neutral", (df["Sentiment"] == "Neutral").sum())
col4.metric("Negative", (df["Sentiment"] == "Negative").sum())

# Pie chart
st.subheader("📊 Sentiment Distribution")
counts = df["Sentiment"].value_counts()
fig, ax = plt.subplots()
ax.pie(counts, labels=counts.index, autopct="%1.1f%%")
st.pyplot(fig)

# Bar chart
st.subheader("📊 Sentiment Counts (Bar Chart)")
st.bar_chart(counts)

# Word Cloud
st.subheader("☁ Word Cloud")
text = " ".join(df["clean_message"].astype(str))
wc = WordCloud(width=900, height=400, background_color="white").generate(text)
st.image(wc.to_array(), use_column_width=True)

# Table
st.subheader("📑 Sample Tweets")
st.dataframe(df[["clean_message", "Sentiment"]].head(50))

# Download option
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇ Download Processed CSV for Power BI",
    csv,
    "climate_sentiment_processed.csv",
    "text/csv"
)

  
