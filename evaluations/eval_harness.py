import textstat # pip install textstat
import json

def run_evaluation(source_text, generated_guide, ground_truth_facts=None):
    """
    Generates a 'Report Card' for a single study guide.
    """
    # 1. READABILITY ANALYSIS
    # Higher score = Easier to read. Target for B1/ADHD is 70-90.
    source_ease = textstat.flesch_reading_ease(source_text)
    output_ease = textstat.flesch_reading_ease(generated_guide)
    
    # 2. COMPLEXITY REDUCTION (Grade Level)
    source_grade = textstat.flesch_kincaid_grade(source_text)
    output_grade = textstat.flesch_kincaid_grade(generated_guide)

    # 3. STRUCTURAL COMPLIANCE (ADHD Rules)
    # Check for emojis and bolding
    has_emojis = any(char in generated_guide for char in ["🧠", "⚡", "✅", "🏛️", "📆"])
    has_bionic = "**" in generated_guide # Markdown bolding check
    
    eval_report = {
    "Readability Boost": f"+{round(output_ease - source_ease, 1)} pts",
    "Source Grade": round(source_grade, 1),
    "Output Grade": round(output_grade, 1),
    "Formatting Status": "✅ ADHD Compliant" if (has_emojis and has_bionic) else "❌ Needs Review"
}
    
    return eval_report

# Example usage for your project documentation:
source = "The industrial revolution was a pivotal era characterized by the transition to new manufacturing processes..."
guide = "🧠 **Indus**trial **Revol**ution: When **facto**ries started making things with **machi**nes."

report = run_evaluation(source, guide)
print(json.dumps(report, indent=4))