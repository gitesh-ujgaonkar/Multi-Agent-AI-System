import os
import datetime
from multi_agent_ai_system.memory.shared_memory import SharedMemory
from multi_agent_ai_system.agents.json_agent import JSONAgent
from multi_agent_ai_system.agents.email_agent import EmailAgent
from multi_agent_ai_system.agents.pdf_agent import PDFAgent
import pdfplumber
import openai

class ClassifierAgent:
    def __init__(self, shared_memory: SharedMemory):
        self.shared_memory = shared_memory
        self.json_agent = JSONAgent(shared_memory)
        self.email_agent = EmailAgent(shared_memory)
        self.pdf_agent = PDFAgent(shared_memory)
        openai.api_key = os.getenv("OPENAI_API_KEY")

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
        # LLM fallback
        if openai.api_key:
            try:
                prompt = f"Classify the intent of this {file_format} document. Possible intents: Invoice, RFQ, Complaint, Regulation, Other.\nContent:\n{content[:1000]}"
                resp = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=10
                )
                intent = resp['choices'][0]['message']['content'].strip()
                return intent
            except Exception as e:
                print(f"[LLM intent detection failed]: {e}")
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