import pandas as pd
import ollama
import os

def run_baseline():
    print("🚀 Loading Test Holdout Data...")
    
    # Load just 5 rows from the test set for our initial baseline check
    df = pd.read_csv("data/test_holdout.csv").sample(n=5, random_state=42)
    
    results = []

    print("🧠 Prompting Llama 3 via Ollama...\n")
    
    for index, row in df.iterrows():
        complex_text = row['complex_text']
        
        # The strict ADHD formatting prompt we want the model to follow
        prompt = f"""You are an expert tutor for students with ADHD. 
        Summarize the following complex text. You MUST follow these strict rules:
        1. Output exactly 3 to 5 bullet points.
        2. Start every bullet point with a relevant emoji.
        3. Bold the core subject/concept in every bullet point.
        4. Do not include introductory or concluding paragraphs.

        Text to summarize:
        {complex_text}
        """

        try:
            # Call local Llama 3
            response = ollama.chat(model='llama3.2', messages=[
                {'role': 'user', 'content': prompt}
            ])
            
            ai_output = response['message']['content']
            
            results.append({
                "original_text": complex_text,
                "target_simple_text": row['simple_text'],
                "llama3_zero_shot": ai_output
            })
            
            print(f"✅ Processed row {index}...")
            
        except Exception as e:
            print(f"❌ Error on row {index}: {e}")
            # If it fails, make sure you actually pulled llama3: `ollama run llama3`
            return

    # Save the results to review them
    results_df = pd.DataFrame(results)
    os.makedirs("data/baselines", exist_ok=True)
    results_df.to_csv("data/baselines/llama3_baseline.csv", index=False)
    
    print("\n🎉 Baseline complete! Open 'data/baselines/llama3_baseline.csv' to review the outputs.")

if __name__ == "__main__":
    run_baseline()