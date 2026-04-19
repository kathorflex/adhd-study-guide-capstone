# 🧠 ADHD Study Buddy: Accessibility-First LLM Pipeline

A specialized RAG (Retrieval-Augmented Generation) pipeline designed to transform dense academic text into neurodiverse-friendly study guides. This project moves beyond generic summarization by implementing a **3-Stage Transformation Engine** verified against a **30-domain Golden Dataset**.

## 🛠️ Engineering Highlights
* **3-Stage Modular Pipeline:** Separates Factual Auditing, ADHD Styling, and Lexical Simplification to ensure 100% groundedness and a <10.0 Grade Level.
* **Semantic Caching:** Uses **ChromaDB** to index and retrieve previously generated guides, reducing API latency and cost.
* **Model Agnostic:** Built to support **AWS Bedrock (Claude 3.5)**, **Google Gemini 1.5 Flash**, and local **Ollama** deployments.
* **Verified Reliability:** Audited using an automated evaluation harness with **LLM-as-a-Judge** (Gemini Pro) to ensure zero hallucinations.

---

## 📊 Evaluation Results (30-Domain Batch)
The pipeline was tested across 30 academic subjects, from Quantum Physics to Contract Law.

| Metric | Baseline (Raw) | Optimized (Output) | Result |
| :--- | :--- | :--- | :--- |
| **Flesch-Kincaid Grade** | 17.5 (Graduate) | **9.2 (Junior High)** | **-8.3 Grade Drop** |
| **Fact Retention** | 5.0 / 5.0 | 4.9 / 5.0 | **98% Accuracy** |
| **ADHD Compliance** | 0% | 100% | **Verified** |

---

## 🚀 Quick Start (Local Setup)

### 1. Environment Setup
Clone the repo and install dependencies:
```bash
git clone https://github.com/your-username/adhd-study-buddy.git
cd adhd-study-buddy
pip install -r requirements.txt
```

### 2. Configure Credentials
Create a `.env` file in the root directory:
```text
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
GEMINI_API_KEY=your_key
```

### 3. Ingest the Knowledge Base
Populate your local Vector DB from the manifest:
```bash
python scripts/generate_raw_files.py
python scripts/create_golden_dataset.py
```

### 4. Launch the App
```bash
streamlit run app.py
```

---

## 📂 Project Structure
* `app.py`: Streamlit UI & Orchestration.
* `manifest.csv`: The 30-row "Gold Standard" dataset.
* `src/`: Core logic for the 3-stage LLM prompts.
* `data/raw/`: Original textbook excerpts used for testing.
* `evaluations/`: The automated `eval_harness` and performance reports.

---

## 🎓 Capstone Context
**Problem:** Standard AI summaries often produce "walls of text" that trigger cognitive overwhelm in ADHD learners.
**Solution:** A deterministic pipeline that enforces visual anchoring (Bionic Bold), structural limits (3-bullet rule), and lexical simplification (Grade 9 limit).