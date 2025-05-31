import os
import datetime
from memory.shared_memory import SharedMemory
from agents.json_agent import JSONAgent
from agents.email_agent import EmailAgent
from agents.pdf_agent import PDFAgent
import pdfplumber
import transformers
import torch

class ClassifierAgent:
    def __init__(self, shared_memory: SharedMemory):
        self.shared_memory = shared_memory
        self.json_agent = JSONAgent(shared_memory)
        self.email_agent = EmailAgent(shared_memory)
        self.pdf_agent = PDFAgent(shared_memory)
        self.intent_model = transformers.pipeline(
            "text-classification",
            model="bhadresh-savani/distilbert-base-uncased-emotion",
            top_k=None
        )

    def classify_format(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return 'PDF'
        elif ext == '.json':
            return 'JSON'
        elif ext == '.txt':
            return 'Email'
        else:
            return 'Unknown'

    def detect_intent(self, content: str, file_format: str) -> str:
        # Rule-based first
        lowered = content.lower()
        if 'invoice' in lowered:
            return 'Invoice'
        elif 'rfq' in lowered:
            return 'RFQ'
        elif 'complaint' in lowered:
            return 'Complaint'
        elif 'regulation' in lowered:
            return 'Regulation'
        # Hugging Face fallback
        try:
            result = self.intent_model(content[:512])
            if isinstance(result, list) and len(result) > 0:
                label = result[0][0]['label'] if isinstance(result[0], list) else result[0]['label']
                return label
        except Exception as e:
            print(f"[HF intent detection failed]: {e}")
        return 'Unknown'

    def log_and_route(self, file_path: str, thread_id=None):
        file_format = self.classify_format(file_path)
        if file_format == 'PDF':
            with pdfplumber.open(file_path) as pdf:
                content = " ".join(page.extract_text() or '' for page in pdf.pages)
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        intent = self.detect_intent(content, file_format)
        timestamp = datetime.datetime.now().isoformat()
        log_entry = {
            'source': file_path,
            'file_format': file_format,
            'timestamp': timestamp,
            'intent': intent,
            'thread_id': thread_id
        }
        self.shared_memory.log(log_entry)
        if file_format == 'JSON':
            self.json_agent.process(content, file_path, thread_id=thread_id)
        elif file_format == 'Email':
            self.email_agent.process(content, file_path, thread_id=thread_id)
        elif file_format == 'PDF':
            self.pdf_agent.process(content, file_path, thread_id=thread_id)
        print(f"[ClassifierAgent] {file_path}: format={file_format}, intent={intent}")
        return log_entry 