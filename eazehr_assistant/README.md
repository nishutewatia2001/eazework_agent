# EazeHR Assistant Demo

A lightweight HR copilot demo showing how to combine RAG over policy PDFs, dummy HR data, and a long-term memory store into a single prompt for an LLM.

## Features
- FAISS-based retrieval over three HR policy PDFs
- Dummy "Eazework" API with two hardcoded demo users
- SQLite-backed long-term memory for per-user preferences
- Working-memory builder that combines HR data, preferences, and policy snippets
- Simple CLI to view the assembled prompt and a fake LLM response

## Repository structure
```
eazehr_assistant/
  README.md
  requirements.txt
  data/
    policies/
      leave_policy.pdf
      payslip_explained.pdf
      employee_handbook.pdf
  src/
    config.py
    ingest_policies.py
    faiss_store.py
    eazework_dummy.py
    memory_db.py
    working_memory.py
    demo_cli.py
```

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Download three PDFs and place them in `data/policies/` with these exact filenames:
   - `leave_policy.pdf`
   - `payslip_explained.pdf`
   - `employee_handbook.pdf`
3. Build the FAISS index and metadata:
   ```bash
   python -m src.ingest_policies
   ```
4. Run the demo CLI:
   ```bash
   python -m src.demo_cli --user_id U001 --question "I am planning to resign, can I encash my earned leaves?"
   ```

## How it works
- **Policy ingestion & retrieval**: `ingest_policies.py` extracts text from the PDFs, chunks it, embeds it with Sentence Transformers, and stores embeddings in a FAISS index with JSON metadata. `faiss_store.PoliciesRetriever` loads the index to fetch the most relevant chunks for a query.
- **Dummy HR data**: `eazework_dummy.py` exposes a few helper functions over two hardcoded users, including summaries, manager chain info, and payslip data.
- **Long-term memory**: `memory_db.py` maintains per-user preferences in SQLite (seeded with preferred tone and language). The DB is initialized automatically when building working memory.
- **Working memory**: `working_memory.build_working_memory` merges the user query, HR data, long-term memory, and RAG snippets into a single dictionary. `format_working_memory_as_prompt` turns it into a human-readable prompt.
- **CLI demo**: `demo_cli.py` ties everything together, printing the full prompt and a fake LLM answer stub.

## Notes
- No real LLM calls are made; `call_llm` simply returns a placeholder string so you can inspect the assembled prompt.
- Ensure the PDFs are present before running `ingest_policies.py`; otherwise the script will raise an error.
