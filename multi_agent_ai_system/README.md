# Multi-Agent AI System

## Overview
A modular multi-agent AI system in Python that classifies input files (PDF, JSON, Email), detects their intent, and routes them to specialized agents. The system maintains shared memory for traceability and agent chaining.

## Modules
- **Classifier Agent**: Orchestrates file classification and routing.
- **JSON Agent**: Handles structured JSON files.
- **Email Agent**: Handles email content.
- **Shared Memory**: Central traceability store (in-memory or SQLite).

## Folder Structure
```
multi_agent_ai_system/
│
├── agents/
│   ├── classifier_agent.py
│   ├── email_agent.py
│   └── json_agent.py
│
├── memory/
│   └── shared_memory.py
│
├── test_inputs/
│   ├── invoice.pdf
│   ├── rfq.json
│   └── complaint_email.txt
│
├── main.py
├── requirements.txt
└── README.md
```

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the demo:
   ```bash
   python main.py
   ```

## Features
- File format and intent classification
- Modular agent routing
- Shared memory for traceability
- Test/demo script included

## Usage
- Place your test files in the `test_inputs/` directory.
- Run the demo as above. The system will:
  - Classify each file (PDF, JSON, Email)
  - Detect intent (Invoice, RFQ, Complaint, Regulation, etc.)
  - Route to the appropriate agent
  - Log all actions and extracted data in shared memory
- The final shared memory snapshot will be printed.

## Example Output
```
[ClassifierAgent] .../invoice.pdf: format=PDF, intent=Invoice
[ClassifierAgent] .../rfq.json: format=JSON, intent=RFQ
[JSONAgent] Processed .../rfq.json: {'missing_fields': []}
[ClassifierAgent] .../complaint_email.txt: format=Email, intent=Complaint
[EmailAgent] Processed .../complaint_email.txt: intent=Complaint, urgency=High

[SharedMemory Snapshot]
[{...}, {...}, ...]
```

## Optional
- LLM-based intent detection (OpenAI GPT-4-turbo or LLaMA via Hugging Face)

---
MIT License 