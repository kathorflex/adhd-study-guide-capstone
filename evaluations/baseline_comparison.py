#!/usr/bin/env python3
"""
Baseline comparison: Demonstrate prompt engineering improvements.

Compares:
1. Basic LLM (no prompt engineering)
2. Optimized LLM (with prompt engineering techniques)

Shows measurable improvement in:
- Readability (Flesch Reading Ease)
- Grade level (Flesch-Kincaid)
- ADHD compliance (emojis, bolding, structure)
"""

import sys
import pathlib
import json
import textstat
from typing import Dict, List
from dotenv import load_dotenv

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

load_dotenv()


def basic_prompt(text: str) -> str:
    """Basic prompt - minimal prompt engineering."""
    return f"Summarize this text in simple terms:\n\n{text}"


def optimized_prompt(text: str) -> str:
    """Optimized prompt - full prompt engineering techniques."""
    return f"""You are an ADHD learning specialist with expertise in neurodivergent education.

Transform this academic text into an ADHD-friendly study guide.

STRICT REQUIREMENTS:
1. Reading Level: B1 (Flesch Reading Ease 70-90, Grade Level < 10)
2. Visual Anchoring: Start EVERY bullet with emoji (🧠, ⚡, ✅, 🏛️, 📆)
3. Bionic Bolding: Use **markdown bold** on key concepts and syllables
4. Structure: Exactly 3-5 bullet points, each < 15 words
5. Vocabulary: Define 2-3 technical terms in simple language
6. NO introductory text like "Here is..." - jump straight to bullets

Example Output:
🧠 **Mito**chondria are tiny **power** plants in cells
⚡ They make **ATP** which stores **energy** for the body
✅ Found in almost all living **organisms**

Vocabulary:
- ATP: The energy molecule cells use
- Mitochondria: Powerhouse organelle

Text to transform:
{text}

Return JSON:
{{
  "summary": "2-3 accessible sentences",
  "bullets": ["🧠 bullet 1", "⚡ bullet 2", "✅ bullet 3"],
  "vocabulary": {{"term": "simple definition"}}
}}"""


def generate_with_llm(prompt: str, provider: str = "gemini") -> str:
    """Generate response using specified LLM provider."""
    if provider == "gemini":
        from google import genai
        import os

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "temperature": 0.3,
                "max_output_tokens": 1024,
            }
        )
        return response.text

    elif provider == "anthropic":
        from anthropic import Anthropic
        import os

        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    else:
        raise ValueError(f"Unknown provider: {provider}")


def evaluate_output(text: str) -> Dict:
    """Evaluate output quality."""
    return {
        "readability_score": round(textstat.flesch_reading_ease(text), 1),
        "grade_level": round(textstat.flesch_kincaid_grade(text), 1),
        "has_emojis": any(c in text for c in "🧠⚡✅🏛️📆"),
        "has_bolding": "**" in text,
        "bullet_count": len([l for l in text.split('\n') if l.strip().startswith(('🧠', '⚡', '✅', '-', '*'))]),
        "word_count": len(text.split()),
    }


def run_comparison(test_excerpts: List[Dict], provider: str = "gemini"):
    """Run baseline vs optimized comparison."""

    results = []

    print(f"\n{'='*70}")
    print("BASELINE VS OPTIMIZED PROMPT ENGINEERING COMPARISON")
    print(f"{'='*70}\n")

    for i, item in enumerate(test_excerpts, 1):
        print(f"[{i}/{len(test_excerpts)}] Testing: {item['id']} ({item['domain']})")

        excerpt = item['excerpt'][:500]  # Limit length for speed

        # Generate with basic prompt
        print("  - Running baseline (basic prompt)...", end=" ")
        basic_output = generate_with_llm(basic_prompt(excerpt), provider)
        basic_metrics = evaluate_output(basic_output)
        print("✓")

        # Generate with optimized prompt
        print("  - Running optimized (engineered prompt)...", end=" ")
        optimized_output = generate_with_llm(optimized_prompt(excerpt), provider)
        optimized_metrics = evaluate_output(optimized_output)
        print("✓")

        # Calculate improvements
        readability_gain = optimized_metrics['readability_score'] - basic_metrics['readability_score']
        grade_reduction = basic_metrics['grade_level'] - optimized_metrics['grade_level']

        result = {
            "id": item['id'],
            "domain": item['domain'],
            "baseline": {
                "output": basic_output[:200] + "...",
                "metrics": basic_metrics
            },
            "optimized": {
                "output": optimized_output[:200] + "...",
                "metrics": optimized_metrics
            },
            "improvements": {
                "readability_gain": round(readability_gain, 1),
                "grade_reduction": round(grade_reduction, 1),
                "emoji_added": optimized_metrics['has_emojis'] and not basic_metrics['has_emojis'],
                "bolding_added": optimized_metrics['has_bolding'] and not basic_metrics['has_bolding']
            }
        }

        results.append(result)

        print(f"  ✅ Readability: +{readability_gain:.1f} | Grade: -{grade_reduction:.1f}")

    # Calculate aggregate statistics
    avg_readability_gain = sum(r['improvements']['readability_gain'] for r in results) / len(results)
    avg_grade_reduction = sum(r['improvements']['grade_reduction'] for r in results) / len(results)
    emoji_improvement = sum(r['improvements']['emoji_added'] for r in results) / len(results) * 100
    bolding_improvement = sum(r['improvements']['bolding_added'] for r in results) / len(results) * 100

    summary = {
        "total_examples": len(results),
        "avg_readability_gain": round(avg_readability_gain, 1),
        "avg_grade_reduction": round(avg_grade_reduction, 1),
        "emoji_improvement_rate": f"{emoji_improvement:.0f}%",
        "bolding_improvement_rate": f"{bolding_improvement:.0f}%",
        "provider": provider
    }

    print(f"\n{'='*70}")
    print("SUMMARY: PROMPT ENGINEERING IMPACT")
    print(f"{'='*70}")
    print(f"Avg Readability Gain: +{summary['avg_readability_gain']} points")
    print(f"Avg Grade Level Reduction: -{summary['avg_grade_reduction']} grades")
    print(f"Visual Anchoring Added: {summary['emoji_improvement_rate']} of examples")
    print(f"Bionic Bolding Added: {summary['bolding_improvement_rate']} of examples")
    print(f"{'='*70}\n")

    return {"summary": summary, "detailed_results": results}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run baseline vs optimized comparison")
    parser.add_argument(
        '--provider',
        choices=['gemini', 'anthropic'],
        default='gemini',
        help='LLM provider'
    )
    parser.add_argument(
        '--samples',
        type=int,
        default=5,
        help='Number of samples to test'
    )
    parser.add_argument(
        '--output',
        type=pathlib.Path,
        default=pathlib.Path(__file__).parent / 'comparison_results.json',
        help='Output file for results'
    )

    args = parser.parse_args()

    # Load sample data
    dataset_path = pathlib.Path(__file__).parent.parent / 'data' / 'golden_dataset.jsonl'

    if not dataset_path.exists():
        print(f"❌ Error: {dataset_path} not found!")
        print("   Run: python data/create_golden_dataset.py first")
        sys.exit(1)

    # Load first N samples
    test_data = []
    with dataset_path.open('r') as f:
        for i, line in enumerate(f):
            if i >= args.samples:
                break
            if line.strip():
                test_data.append(json.loads(line))

    print(f"Loaded {len(test_data)} test examples")

    # Run comparison
    results = run_comparison(test_data, args.provider)

    # Save results
    with args.output.open('w') as f:
        json.dump(results, f, indent=2)

    print(f"📄 Detailed results saved to: {args.output}")
