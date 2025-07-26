import pandas as pd
from transformers import pipeline

books_with_reviews = pd.read_csv('/Users/jonaslee/Desktop/Goodreads_AI_Review_Summarizer/reviews_grouped_per_book.csv')
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_reviews(review_list):
    combined = " ".join(review_list)
    # Bart has 1024 token limit
    return summarizer(combined[:1024])[0]['summary_text']

# Apply summarizer
books_with_reviews['summary'] = books_with_reviews['review_content'].apply(eval).apply(summarize_reviews)

# New csv
books_with_reviews.to_csv("books_with_summaries.csv", index=False)
