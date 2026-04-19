import pandas as pd
import json
import os

def main():
    print("🔄 Converting CSV data to MLX JSONL format...")
    
    # Load your training data
    df = pd.read_csv("data/train_wiki_gold.csv")
    
    # We will save the formatted data here
    os.makedirs("data/mlx_data", exist_ok=True)
    
    formatted_data = []
    
    for _, row in df.iterrows():
        # Injecting the strict rules into the prompt
        system_prompt = "You are an expert tutor for students with ADHD."
        user_prompt = f"Summarize the following text using exactly 3 to 5 bullet points. Start each bullet with an emoji, and bold the core concepts.\n\nText: {row['complex_text']}"
        response = row['simple_text']
        
        # Wrapping it in standard ChatML format (highly effective for local models)
        full_text = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_prompt}<|im_end|>\n<|im_start|>assistant\n{response}<|im_end|>"
        
        formatted_data.append({"text": full_text})
        
    # MLX expects valid.jsonl and train.jsonl
    # We will use 90% for training and 10% for validation during the training loop
    split_idx = int(len(formatted_data) * 0.9)
    train_data = formatted_data[:split_idx]
    valid_data = formatted_data[split_idx:]
    
    # Save as JSONL
    with open("data/mlx_data/train.jsonl", "w") as f:
        for item in train_data:
            f.write(json.dumps(item) + "\n")
            
    with open("data/mlx_data/valid.jsonl", "w") as f:
        for item in valid_data:
            f.write(json.dumps(item) + "\n")
            
    print(f"✅ Created data/mlx_data/train.jsonl ({len(train_data)} rows)")
    print(f"✅ Created data/mlx_data/valid.jsonl ({len(valid_data)} rows)")

if __name__ == "__main__":
    main()