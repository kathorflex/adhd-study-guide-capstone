#!/usr/bin/env python3
"""
Evaluation script for ADHD Study Guide models.
Loads the golden dataset and evaluates model outputs against ground truth.
"""

import json
import pathlib
import sys
from typing import Dict, List

from dotenv import load_dotenv
from eval_harness import run_evaluation

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path to import from src
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))


def load_golden_dataset(jsonl_path: pathlib.Path) -> List[Dict]:
    """Load the golden dataset from JSONL file."""
    records = []
    with jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def generate_study_guide(excerpt: str, provider: str = "local") -> str:
    """
    Generate a study guide from an excerpt.

    Args:
        excerpt: The source text to convert
        provider: "local" for GGUF models, "gemini" for Gemini API, "anthropic" for Claude

    Returns:
        Generated study guide text
    """
    if provider == "local":
        # TODO: Add MLX or llama.cpp inference here
        # For now, return a placeholder
        return f"🧠 **Study Guide**\n\n⚡ This is a placeholder for local model inference.\n\n{excerpt[:100]}..."

    elif provider == "gemini":
        # Use Gemini API (requires GEMINI_API_KEY in env)
        import os

        from google import genai

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")

        client = genai.Client(api_key=api_key)

        prompt = f"""Transform this text into an ADHD-friendly study guide at B1 reading level.

Requirements:
- Use emojis (🧠, ⚡, ✅, 🏛️, 📆) for visual anchoring
- Use **bionic bolding** on key syllables
- Keep sentences short and clear
- Target Flesch Reading Ease: 70-90
- Include the 5 key facts

Text to transform:
{excerpt}"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "temperature": 0.3,
                "max_output_tokens": 1024,
            },
        )
        return response.text

    elif provider == "anthropic":
        # Use Claude API
        import os

        from anthropic import Anthropic

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment")

        client = Anthropic(api_key=api_key)

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0.3,
            system="You are an ADHD-friendly study guide generator. Transform complex text into B1-level guides with emojis and bionic bolding.",
            messages=[
                {
                    "role": "user",
                    "content": f"Transform this into an ADHD study guide:\n\n{excerpt}",
                }
            ],
        )
        return message.content[0].text

    else:
        raise ValueError(f"Unknown provider: {provider}")


def evaluate_dataset(
    dataset: List[Dict], provider: str = "local", output_path: pathlib.Path = None
) -> Dict:
    """
    Evaluate all examples in the dataset.

    Returns:
        Summary statistics and detailed results
    """
    results = []

    print(f"\n🔍 Evaluating {len(dataset)} examples using provider: {provider}\n")

    for i, record in enumerate(dataset, 1):
        print(f"[{i}/{len(dataset)}] Evaluating {record['id']}...", end=" ")

        try:
            # Generate study guide
            generated_guide = generate_study_guide(record["excerpt"], provider)

            # Evaluate
            eval_report = run_evaluation(
                source_text=record["excerpt"],
                generated_guide=generated_guide,
                ground_truth_facts=record["facts"],
            )

            result = {
                "id": record["id"],
                "domain": record["domain"],
                "generated_guide": generated_guide,
                "evaluation": eval_report,
                "ground_truth_summary": record["summary_b1"],
                "ground_truth_facts": record["facts"],
            }

            results.append(result)
            print("✅")

        except Exception as e:
            print(f"❌ Error: {e}")
            results.append(
                {"id": record["id"], "domain": record["domain"], "error": str(e)}
            )

    # Calculate summary statistics
    successful = [r for r in results if "evaluation" in r]

    if successful:
        avg_readability = sum(
            float(
                r["evaluation"]["Readability Boost"]
                .replace("+", "")
                .replace(" pts", "")
            )
            for r in successful
        ) / len(successful)

        avg_output_grade = sum(
            r["evaluation"]["Output Grade"] for r in successful
        ) / len(successful)

        compliant_count = sum(
            1
            for r in successful
            if r["evaluation"]["Formatting Status"] == "✅ ADHD Compliant"
        )

        summary = {
            "total_examples": len(dataset),
            "successful_evaluations": len(successful),
            "avg_readability_boost": round(avg_readability, 1),
            "avg_output_grade": round(avg_output_grade, 1),
            "adhd_compliance_rate": f"{compliant_count}/{len(successful)} ({round(100 * compliant_count / len(successful), 1)}%)",
            "provider": provider,
        }
    else:
        summary = {
            "total_examples": len(dataset),
            "successful_evaluations": 0,
            "error": "No successful evaluations",
        }

    # Save results if output path provided
    if output_path:
        output_data = {"summary": summary, "detailed_results": results}
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Results saved to: {output_path}")

    return {"summary": summary, "results": results}


def print_summary(summary: Dict):
    """Pretty print the evaluation summary."""
    print("\n" + "=" * 60)
    print("📊 EVALUATION SUMMARY")
    print("=" * 60)
    for key, value in summary.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate ADHD Study Guide models")
    parser.add_argument(
        "--dataset",
        type=pathlib.Path,
        default=pathlib.Path(__file__).parent.parent / "data" / "golden_dataset.jsonl",
        help="Path to golden dataset JSONL file",
    )
    parser.add_argument(
        "--provider",
        choices=["local", "gemini", "anthropic"],
        default="local",
        help="LLM provider to use for generation",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path(__file__).parent / "results.json",
        help="Path to save evaluation results",
    )

    args = parser.parse_args()

    # Load dataset
    print(f"📂 Loading dataset from: {args.dataset}")
    dataset = load_golden_dataset(args.dataset)
    print(f"✅ Loaded {len(dataset)} examples")

    # Run evaluation
    eval_results = evaluate_dataset(
        dataset=dataset, provider=args.provider, output_path=args.output
    )

    # Print summary
    print_summary(eval_results["summary"])
