import pandas as pd
from transformers import pipeline
from tqdm import tqdm

books_with_reviews = pd.read_csv('/Users/jonaslee/Desktop/Goodreads_AI_Review_Summarizer/reviews_grouped_per_book.csv')

# Testing first 100
books_with_reviews = books_with_reviews.head(100)

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_reviews(review_list):
    combined = " ".join(review_list)
    # Bart has 1024 token limit
    return summarizer(combined[:1024])[0]['summary_text']

# Progress bar
summaries = []
for reviews in tqdm(books_with_reviews['review_content'].apply(eval), desc="Summarizing Reviews"):
    summary = summarize_reviews(reviews)
    summaries.append(summary)

# Apply summarizer
books_with_reviews['summary'] = summaries

# New csv
books_with_reviews.to_csv("books_with_summaries_first_100.csv", index=False)
print("Summarization complete. Check 'books_with_summaries_first_100.csv' for results.")
