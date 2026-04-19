import os
from pathlib import Path

import mlx.core as mx
from huggingface_hub import snapshot_download
from mlx.utils import tree_flatten
from mlx_lm import load
from mlx_lm.gguf import convert_to_gguf


def force_export():
    model_id = "meta-llama/Llama-3.2-1B-Instruct"
    adapter_path = "adapters"
    output_file = "models/adhd-buddy-final.gguf"

    if not os.path.exists("models"):
        os.makedirs("models")

    print("🚀 Loading base model and merging adapters...")
    model, tokenizer, config = load(
        model_id, adapter_path=adapter_path, return_config=True
    )

    print("🗜️ Flattening and Casting weights to Float16...")
    # tree_flatten turns the nested dictionary into a simple list of (name, array)
    flat_params = tree_flatten(model.parameters())

    weights = {}
    for key, value in flat_params:
        # Now we are calling .astype() on the actual MLX array, not a dict
        weights[key] = mx.contiguous(value.astype(mx.float16))

    print("📂 Finding tokenizer metadata...")
    model_dir = snapshot_download(repo_id=model_id)

    print(f"📦 Exporting to {output_file}...")
    convert_to_gguf(Path(model_dir), weights, config, output_file)

    size_gb = os.path.getsize(output_file) / (1024**3)
    print(f"✅ Success! Final size: {size_gb:.2f} GB")


if __name__ == "__main__":
    force_export()
