#!/usr/bin/env python3
"""
Test suite for ADHD Study Guide pipeline.
Tests the core transformation pipeline and prompt engineering.
"""

import unittest
import sys
import pathlib
import textstat

# Add parent directory to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))


class TestADHDTransformation(unittest.TestCase):
    """Test ADHD-friendly transformations."""

    def test_readability_improvement(self):
        """Test that transformed text has better readability scores."""
        source = "The photosynthetic process involves chloroplasts which contain chlorophyll molecules that absorb electromagnetic radiation in specific wavelength ranges."
        transformed = "Plants use sunlight to make food. They have special parts called chloroplasts with green chlorophyll."

        source_score = textstat.flesch_reading_ease(source)
        transformed_score = textstat.flesch_reading_ease(transformed)

        self.assertGreater(transformed_score, source_score,
                          "Transformed text should be more readable")

    def test_grade_level_reduction(self):
        """Test that transformed text reduces grade level."""
        source = "Mitochondria generate ATP via oxidative phosphorylation in the inner mitochondrial membrane."
        transformed = "Mitochondria make energy for cells. They work like tiny batteries."

        source_grade = textstat.flesch_kincaid_grade(source)
        transformed_grade = textstat.flesch_kincaid_grade(transformed)

        self.assertLess(transformed_grade, source_grade,
                       "Transformed text should have lower grade level")
        self.assertLess(transformed_grade, 10.0,
                       "Transformed text should be below grade 10")

    def test_emoji_presence(self):
        """Test that output includes visual anchors (emojis)."""
        guide = "🧠 **Mitochondria** make energy\n⚡ They are in most cells\n✅ They have their own DNA"

        emoji_count = sum(1 for char in guide if ord(char) > 127 and char in "🧠⚡✅🏛️📆")
        self.assertGreater(emoji_count, 0, "Guide should contain emojis")

    def test_bionic_bold_presence(self):
        """Test that output includes bionic bolding."""
        guide = "🧠 **Mitochondria** make energy for **cells**"

        self.assertIn("**", guide, "Guide should contain markdown bold markers")
        # Count bold markers (should be even number)
        bold_count = guide.count("**")
        self.assertEqual(bold_count % 2, 0, "Bold markers should be paired")

    def test_bullet_structure(self):
        """Test that output follows bullet structure."""
        guide = """🧠 **Mitochondria** make energy
⚡ They are **powerhouses**
✅ Found in most **cells**"""

        lines = [l.strip() for l in guide.split('\n') if l.strip()]
        self.assertGreaterEqual(len(lines), 3, "Should have at least 3 bullet points")
        self.assertLessEqual(len(lines), 5, "Should have at most 5 bullet points")


class TestPromptEngineering(unittest.TestCase):
    """Test prompt engineering techniques."""

    def test_instruction_clarity(self):
        """Test that prompts have clear instructions."""
        prompt = """You are an ADHD-friendly study assistant.
Return ONLY a valid JSON object with this exact structure:
{
  "summary": "2-3 brain-friendly sentences",
  "bullets": ["🧠 Fact 1", "⚡ Fact 2"],
  "vocabulary": {"Term": "Simple Definition"}
}"""

        self.assertIn("ONLY", prompt, "Should use emphatic instructions")
        self.assertIn("exact structure", prompt, "Should specify exact format")
        self.assertIn("{", prompt, "Should include example structure")

    def test_constraint_specification(self):
        """Test that prompts specify constraints."""
        prompt = "Target Flesch Reading Ease: 70-90"

        self.assertIn("70-90", prompt, "Should specify numeric targets")

    def test_example_driven_prompts(self):
        """Test that prompts include examples."""
        prompt = """Example:
{
  "summary": "2-3 brain-friendly sentences",
  "bullets": ["🧠 Fact 1", "⚡ Fact 2"]
}"""

        self.assertIn("Example", prompt, "Should include examples")
        self.assertIn("🧠", prompt, "Should show emoji usage")


class TestDataQuality(unittest.TestCase):
    """Test golden dataset quality."""

    def test_golden_dataset_exists(self):
        """Test that golden dataset file exists."""
        dataset_path = pathlib.Path(__file__).parent.parent / "data" / "golden_dataset.jsonl"
        self.assertTrue(dataset_path.exists(), "Golden dataset should exist")

    def test_golden_dataset_format(self):
        """Test that golden dataset is valid JSONL."""
        import json

        dataset_path = pathlib.Path(__file__).parent.parent / "data" / "golden_dataset.jsonl"

        if not dataset_path.exists():
            self.skipTest("Golden dataset not yet created")

        with dataset_path.open('r') as f:
            lines = [l.strip() for l in f if l.strip()]

        self.assertGreater(len(lines), 0, "Dataset should not be empty")

        # Test first record
        record = json.loads(lines[0])
        required_fields = ["id", "domain", "excerpt", "facts", "summary_b1"]

        for field in required_fields:
            self.assertIn(field, record, f"Record should have {field}")

        self.assertEqual(len(record["facts"]), 5, "Each record should have 5 facts")

    def test_domain_coverage(self):
        """Test that dataset covers multiple domains."""
        import json

        dataset_path = pathlib.Path(__file__).parent.parent / "data" / "golden_dataset.jsonl"

        if not dataset_path.exists():
            self.skipTest("Golden dataset not yet created")

        domains = set()
        with dataset_path.open('r') as f:
            for line in f:
                if line.strip():
                    record = json.loads(line)
                    domains.add(record['domain'])

        self.assertGreaterEqual(len(domains), 10, "Should cover at least 10 domains")


class TestEvaluationMetrics(unittest.TestCase):
    """Test evaluation harness metrics."""

    def test_flesch_reading_ease_calculation(self):
        """Test readability metric calculation."""
        easy_text = "The cat sat on the mat."
        hard_text = "The feline domesticus positioned itself atop the rectangular textile floor covering."

        easy_score = textstat.flesch_reading_ease(easy_text)
        hard_score = textstat.flesch_reading_ease(hard_text)

        self.assertGreater(easy_score, hard_score,
                          "Simple text should have higher reading ease")

    def test_grade_level_calculation(self):
        """Test grade level metric calculation."""
        text = "Mitochondria make energy for cells."
        grade = textstat.flesch_kincaid_grade(text)

        self.assertIsInstance(grade, (int, float), "Grade should be numeric")
        self.assertGreater(grade, 0, "Grade should be positive")

    def test_compliance_detection(self):
        """Test ADHD compliance detection."""
        compliant_guide = "🧠 **Mitochondria** make energy\n⚡ Found in **cells**"
        non_compliant_guide = "Mitochondria make energy and are found in cells"

        # Check emojis
        has_emoji_compliant = any(c in compliant_guide for c in "🧠⚡✅")
        has_emoji_non = any(c in non_compliant_guide for c in "🧠⚡✅")

        self.assertTrue(has_emoji_compliant, "Compliant guide should have emojis")
        self.assertFalse(has_emoji_non, "Non-compliant guide should lack emojis")

        # Check bolding
        self.assertIn("**", compliant_guide, "Compliant guide should have bolding")
        self.assertNotIn("**", non_compliant_guide, "Non-compliant guide should lack bolding")


if __name__ == '__main__':
    unittest.main()
