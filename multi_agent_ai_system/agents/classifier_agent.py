import os
import datetime
from ..memory.shared_memory import SharedMemory
from .json_agent import JSONAgent
from .email_agent import EmailAgent
import pdfplumber

class ClassifierAgent:
    def __init__(self, shared_memory: SharedMemory):
        self.shared_memory = shared_memory
        self.json_agent = JSONAgent(shared_memory)
        self.email_agent = EmailAgent(shared_memory)

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
        # Placeholder: Replace with rule-based or LLM-based logic
        if 'invoice' in content.lower():
            return 'Invoice'
        elif 'rfq' in content.lower():
            return 'RFQ'
        elif 'complaint' in content.lower():
            return 'Complaint'
        elif 'regulation' in content.lower():
            return 'Regulation'
        else:
            return 'Unknown'

    def log_and_route(self, file_path: str):
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
            'intent': intent
        }
        self.shared_memory.log(log_entry)
        if file_format == 'JSON':
            self.json_agent.process(content, file_path)
        elif file_format == 'Email':
            self.email_agent.process(content, file_path)
        # PDF handling: just log for now
        print(f"[ClassifierAgent] {file_path}: format={file_format}, intent={intent}")
        return log_entry 