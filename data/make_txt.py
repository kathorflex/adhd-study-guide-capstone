from pathlib import Path

# Data mapping based on your manifest structure
data_to_generate = {
    "raw/astronomy/black_holes.txt": "A black hole is a region of spacetime where gravity is so strong that nothing can escape. The boundary is called the event horizon. At the center lies a singularity of infinite density. They are formed from the remnants of massive stars after supernova explosions. Supermassive black holes exist at the centers of most galaxies.",
    "raw/sociology/social_stratification.txt": "Social stratification categorizes people into a hierarchy based on wealth, status, and power. Four main systems include slavery, caste, estate, and class. Social mobility is the ability to move between layers. Functionalism suggests stratification is necessary for society to function, while conflict theory argues it benefits the rich.",
    "raw/art/impressionism.txt": "Impressionism began in 19th-century France with artists like Monet and Renoir. It is characterized by small, thin, visible brush strokes and an emphasis on the accurate depiction of light. Subjects are often ordinary, everyday scenes. The movement was initially rejected by the traditional art establishment.",
    "raw/environmental_science/greenhouse_effect.txt": "The greenhouse effect is the process by which radiation from the atmosphere warms a planet's surface. Greenhouse gases include CO2, methane, and water vapor. Human activity has increased gas concentrations, leading to global warming. The process mimics how glass traps heat in a greenhouse.",
    "raw/philosophy/socratic_method.txt": "The Socratic method is a form of cooperative argumentative dialogue using asking and answering questions to stimulate critical thinking. The goal is to draw out underlying assumptions and contradictions. It is named after the Greek philosopher Socrates and is used in modern law schools.",
    "raw/finance/compound_interest.txt": "Compound interest is interest calculated on the initial principal and the accumulated interest. It is often called 'interest on interest.' The frequency of compounding affects the final amount. It allows savings to grow exponentially over long periods. The 'Rule of 72' estimates doubling time.",
    "raw/business/swot.txt": "SWOT stands for Strengths, Weaknesses, Opportunities, and Threats. Strengths and Weaknesses are internal factors, while Opportunities and Threats are external. It is a strategic planning tool used to match internal capabilities to the external environment.",
    "raw/music/rhythm_meter.txt": "Rhythm is the placement of sounds in time. Meter is the regular pattern of strong and weak beats. Common time (4/4) is the most frequent meter in Western music. Syncopation involves placing accents on unexpected beats. Tempo determines the speed of the underlying pulse.",
    "raw/medicine/immune_system.txt": "The immune system is a network of biological processes that protects an organism from diseases. It distinguishes 'self' from 'non-self' pathogens. Innate immunity is the first line of defense, while adaptive immunity creates a 'memory' of specific threats using B and T cells.",
    "raw/government/separation_powers.txt": "Separation of powers divides government into Legislative, Executive, and Judicial branches to prevent any one branch from becoming too powerful. This 'Checks and Balances' structure was central to the U.S. Constitution and inspired by Enlightenment thinkers.",
    "raw/engineering/simple_machines.txt": "Simple machines change the direction or magnitude of a force. The six classical machines are the lever, wheel and axle, pulley, inclined plane, wedge, and screw. Mechanical advantage is the ratio of output force to input force. They follow the law of conservation of energy.",
    "raw/ethics/utilitarianism.txt": "Utilitarianism is a theory of morality that advocates actions that foster happiness, often summarized as 'the greatest good for the greatest number.' It was developed by Jeremy Bentham and John Stuart Mill and is a form of consequentialism.",
}


def create_files():
    for filepath, content in data_to_generate.items():
        # Ensure directory exists
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write the text file
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            print(f"✅ Created: {filepath}")


if __name__ == "__main__":
    create_files()
    print("\n🚀 All 12 new raw files generated successfully!")
