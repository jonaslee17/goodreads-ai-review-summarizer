# goodreads-ai-review-summarizer

This project uses a pretrained NLP model to generate summaries for books based on user reviews from Goodreads. It includes scripts for data ingestion, preprocessing, and applying the summarization model.

## How It Works

The workflow is divided into two main stages: data preparation and summarization.

### 1. Data Ingestion and Preprocessing

The `Data_Ingestion_and_Preprocessing.py` script handles the initial data pipeline:

- **Loads Data**: Ingests book details from a CSV file and book/review data from SQLite databases.
- **Cleans Data**:
    - Removes reviews that have no text content.
    - Strips leading/trailing whitespace from reviews.
    - Discards very short reviews (less than 30 characters).
    - Drops entries without a review rating.
- **Groups Reviews**: Groups all text reviews by their corresponding `book_id`.
- **Merges & Exports**: Merges the grouped reviews with book details and saves the combined dataset to `reviews_grouped_per_book.csv`.

### 2. Review Summarization

The `Review_Summarizer.py` script performs the AI-powered summarization:

- **Loads Processed Data**: Reads the `reviews_grouped_per_book.csv` file created in the previous step.
- **Initializes Model**: Sets up a summarization pipeline using the `sshleifer/distilbart-cnn-12-6` model from the Hugging Face Transformers library.
- **Generates Summaries**: For each book:
    - It combines the list of individual reviews into a single text block.
    - To accommodate the model's 1024-token limit, it truncates the combined text if necessary.
    - The model generates a concise summary of the concatenated reviews.
- **Exports Results**: The script appends the generated summary to each book's data and saves the final output to `books_with_summaries_first_100.csv`. A progress bar is displayed during this process.

## Files

-   `Data_Ingestion_and_Preprocessing.py`: Script to load, clean, and merge data from various sources.
-   `Review_Summarizer.py`: Script to generate summaries from the preprocessed reviews.
-   `reviews_grouped_per_book.csv`: An intermediate CSV file containing book details and a corresponding list of all its reviews. This file is tracked using Git LFS.

## Setup and Usage

### Prerequisites

You will need Python and the following libraries installed:

-   pandas
-   transformers
-   torch (or tensorflow, depending on your transformers installation)
-   tqdm

You can install them using pip:
```bash
pip install pandas transformers torch tqdm
```

You also need the source data files. The scripts use hardcoded local paths (e.g., `/Users/jonaslee/Downloads/archive/...`). **You must modify these paths in both Python scripts to point to the location of your data files.**

### Running the Scripts

1.  **Prepare the Data**:
    Run the data preprocessing script to generate the grouped reviews file.
    ```bash
    python Data_Ingestion_and_Preprocessing.py
    ```
    This will create `reviews_grouped_per_book.csv`.

2.  **Generate Summaries**:
    Run the summarization script.
    ```bash
    python Review_Summarizer.py
    ```
    This will process the first 100 books from the input file and create `books_with_summaries_first_100.csv` containing the new summaries. You can modify the script to process more books.
