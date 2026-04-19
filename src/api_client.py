import anthropic # or google.generativeai

def generate_study_buddy_response(text):
    # STEP 1: Fact Extraction (The Grounding)
    # This keeps your Hallucination Rate low
    facts = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        system="Extract atomic facts with source quotes in JSON.",
        messages=[{"role": "user", "content": text}]
    )

    # STEP 2: The Stylist (The ADHD Value-Add)
    # This creates the +15 point Readability Boost
    final_guide = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        system="Transform these facts into a B1-level ADHD study guide with emojis and bolding.",
        messages=[{"role": "user", "content": facts.content}]
    )

    return final_guide.content