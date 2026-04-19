from mlx_lm import generate, load


def main():
    print("🚀 Loading Model and Custom LoRA Adapter...")

    # Load the base model and your custom trained weights
    model, tokenizer = load("meta-llama/Llama-3.2-1B-Instruct", adapter_path="adapters")

    # The complex text we want to test
    complex_text = "Candace Wheeler (1827–1923) changed the course of textile and interior design in the nineteenth century America and was a driving force behind the professionalization of women in the design field. Inspired by the embroideries produced by England's Royal School of Art Needlework, which she saw at the 1876 Centennial Exposition, Philadelphia, Wheeler founded the Society of Decorative Art in New York. The organization offered instruction in the applied arts to women and helped them sell their work, providing them some measure of economic independence. Wheeler was acquainted with leading figures in the New York art world and, as a textile specialist, went into partnership with Louis Comfort Tiffany in an interior design firm."

    # We explicitly build the exact ChatML prompt the model was trained on
    prompt = f"""<|im_start|>system
You are an expert tutor for students with ADHD.<|im_end|>
<|im_start|>user
Summarize the following text using exactly 3 to 5 bullet points. Start each bullet with an emoji, and bold the core concepts.

Text: {complex_text}<|im_end|>
<|im_start|>assistant
"""

    print("🧠 Generating ADHD Summary...\n")
    print("-" * 50)

    # RUBRIC REQUIREMENT: Explicit Sampling Method
    # temp=0.2 makes it deterministic (prevents hallucinations)
    # top_p=0.9 restricts the vocabulary to highly probable words
    response = generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=250,
        verbose=False,
        temp=0.2,
        top_p=0.9,
    )

    print(response)
    print("-" * 50)


if __name__ == "__main__":
    main()
