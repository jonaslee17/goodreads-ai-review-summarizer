import sqlite3
import pandas as pd

## Loading datasets from SQLite and CSV files

# Connect to the book details database
book_details_df = pd.read_csv('/Users/jonaslee/Downloads/archive/Book_Details.csv')
book_details_df.head()

# Connect to reviews database
conn_reviews = sqlite3.connect('/Users/jonaslee/Downloads/archive/book_reviews.db')
pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn_reviews)

# Load reviews data
reviews_df = pd.read_sql_query("SELECT * FROM book_reviews", conn_reviews)
reviews_df.head()

# Connect to books database
conn_books = sqlite3.connect('/Users/jonaslee/Downloads/archive/books.db')
pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn_books)

# Load books data
books_df = pd.read_sql_query("SELECT * FROM books", conn_books)
books_df.head()

## Cleaning the data

# Drop reviews without actual text
reviews_df = reviews_df.dropna(subset=['review_content'])
# Rid of leading/trailing whitespace in review_content
reviews_df['review_content'] = reviews_df['review_content'].str.strip()

# Drop rows where review content is very short (spam?)
reviews_df = reviews_df[reviews_df['review_content'].str.len() > 30]

# Drop rows without review_rating
reviews_df = reviews_df[reviews_df['review_rating'].notna()]

# Preview first 10 cleaned reviews
print(reviews_df[['review_content', 'review_rating']].head(10))

## Grouping reviews by book
