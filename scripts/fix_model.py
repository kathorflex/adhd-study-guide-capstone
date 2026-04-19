import mlx.core as mx
import numpy as np
from mlx_lm import load
from mlx_lm.gguf import convert_to_gguf
from mlx.utils import tree_flatten
from huggingface_hub import snapshot_download
from pathlib import Path

def manual_cast_shrink():
    model_id = "meta-llama/Llama-3.2-1B-Instruct"
    adapter_path = "adapters"
    output_file = "models/adhd-buddy-final.gguf"
    
    print("🚀 Loading weights for manual casting...")
    model, tokenizer, config = load(model_id, adapter_path=adapter_path, return_config=True)
    
    print("🗜️ Converting weights to Numpy Float16 (The Sledgehammer Fix)...")
    flat_params = tree_flatten(model.parameters())
    
    weights = {}
    for k, v in flat_params:
        # We move it to numpy first to force the precision change, then back to MLX
        np_view = np.array(v).astype(np.float16)
        weights[k] = mx.array(np_view)
    
    model_dir = snapshot_download(repo_id=model_id)
    
    print(f"📦 Exporting to {output_file}...")
    convert_to_gguf(Path(model_dir), weights, config, output_file)
    print("✅ Process complete.")

if __name__ == "__main__":
    manual_cast_shrink()