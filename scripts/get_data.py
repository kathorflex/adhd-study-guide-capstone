import os

import pandas as pd
from datasets import load_dataset
from sklearn.model_selection import train_test_split


def main():
    print("🚀 Downloading 'simple-wiki' dataset from Sentence-Transformers...")

    # This dataset is highly reliable and actively maintained
    dataset = load_dataset("sentence-transformers/simple-wiki", split="train[:5000]")

    # Convert to a Pandas DataFrame
    df = pd.DataFrame(dataset)

    # The sentence-transformers dataset uses 'text' and 'simplified' as columns
    print("🧹 Cleaning and formatting the data...")
    clean_df = pd.DataFrame(
        {"complex_text": df["text"], "simple_text": df["simplified"]}
    )

    # Drop any rows where either column is empty
    clean_df = clean_df.dropna()

    # Filter out sentences that are too short to ensure we get good data
    clean_df = clean_df[clean_df["complex_text"].str.len() > 100]

    # --- THE TRAIN / TEST SPLIT ---
    print("✂️ Splitting data into Training (80%) and Holdout Test (20%)...")
    train_df, test_df = train_test_split(clean_df, test_size=0.2, random_state=42)

    # Save to CSV files
    os.makedirs("data", exist_ok=True)
    train_df.to_csv("data/train_wiki.csv", index=False)
    test_df.to_csv("data/test_holdout.csv", index=False)

    print("✅ Success!")
    print(f"Training rows: {len(train_df)}")
    print(f"Holdout Test rows: {len(test_df)}")
    print("Check the 'data/' folder for your CSV files.")


if __name__ == "__main__":
    main()
