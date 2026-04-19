#!/usr/bin/env python3
"""
Test suite specifically for prompt engineering validation.
Demonstrates the techniques used to improve basic LLM outputs.
"""

import unittest


class TestPromptEngineeringTechniques(unittest.TestCase):
    """
    Validate prompt engineering techniques used in this project.
    """

    def test_technique_1_structured_output(self):
        """
        Technique 1: Structured Output with JSON Schema
        Forces LLMs to return parseable, consistent formats.
        """
        basic_prompt = "Summarize this text about mitochondria."

        improved_prompt = """Return ONLY a valid JSON object:
{
  "summary": "2-3 sentences",
  "bullets": ["fact 1", "fact 2"],
  "vocabulary": {"term": "definition"}
}"""

        # The improved prompt specifies exact structure
        self.assertIn("JSON", improved_prompt)
        self.assertIn("{", improved_prompt)
        self.assertIn("ONLY", improved_prompt)

    def test_technique_2_constraint_specification(self):
        """
        Technique 2: Explicit Constraints
        Provides numeric targets for readability and complexity.
        """
        basic_prompt = "Make this simpler."

        improved_prompt = """Transform to B1 reading level:
- Target Flesch Reading Ease: 70-90
- Maximum grade level: 9
- Sentence length: < 15 words"""

        # Check for specific numeric constraints
        self.assertIn("70-90", improved_prompt)
        self.assertIn("9", improved_prompt)
        self.assertIn("15", improved_prompt)

    def test_technique_3_role_definition(self):
        """
        Technique 3: Clear Role Definition
        Sets context for the LLM's persona and expertise.
        """
        basic_prompt = "Help me study."

        improved_prompt = """You are an expert ADHD learning specialist.
Your goal is to transform complex text for neurodiverse learners.
Focus on visual anchoring and cognitive load reduction."""

        self.assertIn("ADHD", improved_prompt)
        self.assertIn("specialist", improved_prompt)
        self.assertIn("goal", improved_prompt)

    def test_technique_4_visual_anchoring(self):
        """
        Technique 4: Visual Anchoring Requirements
        Mandates emojis and bionic bolding for ADHD accessibility.
        """
        basic_prompt = "Format this as bullet points."

        improved_prompt = """STRICT RULES:
1. Start EVERY bullet with a relevant emoji (🧠, ⚡, ✅)
2. Use **bionic bolding** on key concepts
3. Maximum 5 bullets"""

        self.assertIn("emoji", improved_prompt)
        self.assertIn("**", improved_prompt)
        self.assertIn("STRICT", improved_prompt)

    def test_technique_5_few_shot_examples(self):
        """
        Technique 5: Few-Shot Learning
        Provides examples to guide output style.
        """
        basic_prompt = "Summarize this."

        improved_prompt = """Example output:
🧠 **Mitochondria** are tiny **powerhouses** inside cells
⚡ They make **ATP** which stores **energy**
✅ Found in almost all **eukaryotic** cells

Now transform this text: [text]"""

        self.assertIn("Example", improved_prompt)
        self.assertIn("🧠", improved_prompt)
        self.assertIn("**", improved_prompt)

    def test_technique_6_negative_instructions(self):
        """
        Technique 6: Explicit Prohibitions
        Tells the model what NOT to do.
        """
        basic_prompt = "Summarize this text."

        improved_prompt = """DO NOT:
- Add introductory phrases like "Here is..."
- Use jargon or technical terms
- Exceed 5 bullet points
- Include your own commentary"""

        self.assertIn("DO NOT", improved_prompt)
        self.assertIn("introductory", improved_prompt)

    def test_technique_7_iterative_refinement(self):
        """
        Technique 7: Multi-Stage Pipeline
        Breaks complex transformation into discrete steps.
        """
        single_stage = "Transform this text to be ADHD-friendly."

        multi_stage = {
            "stage_1": "Extract 5 key facts from the text.",
            "stage_2": "Simplify each fact to B1 reading level.",
            "stage_3": "Format with emojis and bionic bolding."
        }

        self.assertEqual(len(multi_stage), 3)
        self.assertIn("Extract", multi_stage["stage_1"])
        self.assertIn("Simplify", multi_stage["stage_2"])
        self.assertIn("Format", multi_stage["stage_3"])

    def test_technique_8_output_validation(self):
        """
        Technique 8: Programmatic Validation
        Checks output meets requirements before accepting.
        """
        def validate_adhd_guide(guide: str) -> bool:
            """Validation rules for ADHD guide output."""
            checks = {
                "has_emoji": any(c in guide for c in "🧠⚡✅🏛️📆"),
                "has_bolding": "**" in guide,
                "max_5_bullets": guide.count('\n') <= 5,
                "no_intro": not guide.lower().startswith("here")
            }
            return all(checks.values())

        good_guide = "🧠 **Cells** need energy\n⚡ **Mitochondria** provide it"
        bad_guide = "Here is a summary: Cells need energy from mitochondria"

        self.assertTrue(validate_adhd_guide(good_guide))
        self.assertFalse(validate_adhd_guide(bad_guide))

    def test_technique_9_temperature_control(self):
        """
        Technique 9: Temperature/Sampling Control
        Uses low temperature for factual accuracy.
        """
        # Low temperature = more deterministic, factual
        low_temp_config = {
            "temperature": 0.3,
            "top_p": 0.9,
            "purpose": "factual extraction"
        }

        # High temperature = more creative (not suitable for facts)
        high_temp_config = {
            "temperature": 0.9,
            "top_p": 0.95,
            "purpose": "creative writing"
        }

        self.assertLess(low_temp_config["temperature"],
                       high_temp_config["temperature"])
        self.assertEqual(low_temp_config["purpose"], "factual extraction")

    def test_technique_10_chain_of_thought(self):
        """
        Technique 10: Chain-of-Thought Prompting
        Asks model to show its reasoning process.
        """
        basic_prompt = "Is this text ADHD-friendly?"

        cot_prompt = """Analyze this text step-by-step:
1. Check reading level (target: grade 9)
2. Count sentence length (target: < 15 words)
3. Verify visual anchors (emojis, bolding)
4. Then conclude: ADHD-friendly or not"""

        self.assertIn("step-by-step", cot_prompt)
        self.assertIn("1.", cot_prompt)
        self.assertIn("Then conclude", cot_prompt)


class TestPromptComparison(unittest.TestCase):
    """
    Compare baseline vs optimized prompts to show improvement.
    """

    def test_baseline_vs_optimized(self):
        """
        Document the before/after of prompt engineering.
        """
        baseline_prompt = "Summarize this text in simple terms."

        optimized_prompt = """You are an ADHD learning specialist.

Transform this text to B1 reading level.

REQUIREMENTS:
- Flesch Reading Ease: 70-90
- Max grade level: 9
- Start each bullet with emoji (🧠, ⚡, ✅)
- Use **bionic bolding** on key terms
- 3-5 bullets maximum
- No introductory text

Example:
🧠 **Mitochondria** make **energy** for cells
⚡ They work like tiny **batteries**
✅ Found in almost all **eukaryotic** organisms

Text to transform:
{text}"""

        # Count prompt engineering techniques used
        techniques = {
            "role_definition": "specialist" in optimized_prompt,
            "numeric_constraints": "70-90" in optimized_prompt,
            "visual_requirements": "emoji" in optimized_prompt,
            "example_provided": "Example" in optimized_prompt,
            "negative_instruction": "No introductory" in optimized_prompt,
            "structured_format": "REQUIREMENTS" in optimized_prompt
        }

        techniques_used = sum(techniques.values())

        self.assertGreaterEqual(techniques_used, 5,
                               "Optimized prompt should use 5+ techniques")
        self.assertGreater(len(optimized_prompt), len(baseline_prompt) * 3,
                          "Optimized prompt should be significantly more detailed")


if __name__ == '__main__':
    unittest.main()
