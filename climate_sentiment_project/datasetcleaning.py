import pandas as pd
import re

# === 1. Load dataset with correct encoding (without errors arg) ===
df = pd.read_csv("twitter_sentiment_data.csv", encoding="utf-8")

# === 2. Define a clean text function ===
def clean_tweet(text):
    if pd.isnull(text):
        return ""
    text = str(text).lower()                      # lowercase
    text = re.sub(r'http\S+|www\S+', '', text)    # remove links
    text = re.sub(r'@\w+', '', text)              # remove mentions
    text = re.sub(r'#', '', text)                 # remove hashtag symbol
    text = re.sub(r'rt[\s]+', '', text)           # remove RT
    text = re.sub(r'[^\w\s]', '', text)           # remove punctuation & emojis
    text = re.sub(r'\s+', ' ', text).strip()      # remove extra spaces
    return text

# === 3. Apply cleaning to message column ===
df["clean_message"] = df["message"].apply(clean_tweet)

# === 4. Display cleaned tweets with sentiment ===
print("Sample cleaned tweets:")
print(df[["sentiment", "clean_message"]].head(10))

# === 5. Fix tweetid column issue ===
df["tweetid"] = df["tweetid"].astype(str)

# === 6. Save cleaned dataset ===
df.to_csv("twitter_sentiment_data_clean.csv", index=False, encoding="utf-8")

print("\n✅ Cleaning done! New file saved as 'twitter_sentiment_data_clean.csv'")
