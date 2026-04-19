import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import ollama
import pandas as pd
from tqdm import tqdm


def generate_gold_data_local_fast():
    print("🚀 Loading original dataset...")
    df = pd.read_csv("data/train_wiki.csv")
    output_file = "data/train_wiki_gold.csv"

    gold_rows = []

    # We use a lock to safely write to our list from multiple threads at once
    lock = threading.Lock()
    completed_count = 0

    def process_row(index, complex_text, simple_text):
        prompt = f"""You are an expert tutor for students with ADHD. 
        Format the following simplified text into exactly 3 to 5 bullet points. 
        
        STRICT RULES:
        1. Start EVERY bullet point with a single relevant emoji.
        2. Bold the core concepts in each bullet.
        3. DO NOT output any introductory or concluding text. 
        4. ONLY output the bullet points.
        
        Text to format:
        {simple_text}
        """

        try:
            response = ollama.chat(
                model="llama3.2", messages=[{"role": "user", "content": prompt}]
            )
            gold_response = response["message"]["content"].strip()
            return {"complex_text": complex_text, "simple_text": gold_response}
        except Exception as e:
            print(f"\n❌ Error on row {index}: {e}")
            return None

    print(f"⚙️ Generating gold standard data for {len(df)} rows...")
    print("🔥 Using ThreadPoolExecutor to process 4 rows simultaneously!")

    # max_workers=4 aligns with our OLLAMA_NUM_PARALLEL setting
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all 2,700 tasks to the thread pool
        future_to_idx = {
            executor.submit(
                process_row, idx, row["complex_text"], row["simple_text"]
            ): idx
            for idx, row in df.iterrows()
        }

        # Use tqdm to give us a progress bar as the parallel tasks finish
        for future in tqdm(as_completed(future_to_idx), total=len(df)):
            result = future.result()
            if result:
                with lock:
                    gold_rows.append(result)
                    completed_count += 1

                    # FAULT TOLERANCE: Save every 100 rows just in case
                    if completed_count % 100 == 0:
                        pd.DataFrame(gold_rows).to_csv(output_file, index=False)

    # Final save
    pd.DataFrame(gold_rows).to_csv(output_file, index=False)
    print(f"\n✅ Finished! Multithreaded Gold dataset saved to {output_file}")


if __name__ == "__main__":
    generate_gold_data_local_fast()
