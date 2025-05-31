# Multi-Agent AI System

## Overview
A modular multi-agent AI system in Python that classifies input files (PDF, JSON, Email), detects their intent, and routes them to specialized agents. The system maintains shared memory (SQLite) for traceability and agent chaining. Intent detection uses free, local Hugging Face Transformers models (no paid API required).

## Modules
- **Classifier Agent**: Orchestrates file classification and routing. Uses rule-based and Hugging Face Transformers for intent detection.
- **JSON Agent**: Handles structured JSON files, validates schema, and flags missing fields.
- **Email Agent**: Handles email content, extracts sender, intent, urgency, and thread/conversation ID.
- **PDF Agent**: Extracts structured fields (invoice number, amount, due date) from PDF files.
- **Shared Memory**: Central traceability store (SQLite-backed, persistent).

## Folder Structure
```
.
├── agents/
│   ├── classifier_agent.py
│   ├── email_agent.py
│   ├── json_agent.py
│   └── pdf_agent.py
├── memory/
│   └── shared_memory.py
├── test_inputs/
│   ├── invoice.pdf
│   ├── rfq.json
│   └── complaint_email.txt
├── main.py
├── requirements.txt
└── README.md
```

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (Installs pdfplumber, torch, transformers, and more.)
2. Run the demo:
   ```bash
   python main.py
   ```

## Features
- File format and intent classification (PDF, JSON, Email)
- Modular agent routing
- Shared memory for traceability (SQLite, persistent)
- Local, free intent detection using Hugging Face Transformers
- Test/demo script included

## Usage
- Place your test files in the `test_inputs/` directory.
- Run the demo as above. The system will:
  - Classify each file (PDF, JSON, Email)
  - Detect intent (Invoice, RFQ, Complaint, Regulation, etc.)
  - Route to the appropriate agent
  - Log all actions and extracted data in shared memory (including thread/conversation ID for emails)
- The final shared memory snapshot will be printed.

## Local Intent Detection
- The system uses a Hugging Face Transformers model for intent detection (no paid API required).
- The first run may download the model; subsequent runs are fast and local.
- You can swap in any other text-classification model from Hugging Face if desired.

## Example Output
```
[ClassifierAgent] .../invoice.pdf: format=PDF, intent=Invoice
[PDFAgent] Processed .../invoice.pdf: {'invoice_number': 'INV-2024-123', 'amount': '1,000', 'due_date': '2024-06-30'}
[ClassifierAgent] .../rfq.json: format=JSON, intent=RFQ
[JSONAgent] Processed .../rfq.json: {'missing_fields': []}
[ClassifierAgent] .../complaint_email.txt: format=Email, intent=Complaint
[EmailAgent] Processed .../complaint_email.txt: intent=Complaint, urgency=High, thread_id=Urgent Complaint Regarding Invoice

[SharedMemory Snapshot]
[{...}, {...}, ...]
```

## Optional
- Swap in other Hugging Face models for different intent detection needs.
- Add more agents or schema as needed.

---
MIT License 