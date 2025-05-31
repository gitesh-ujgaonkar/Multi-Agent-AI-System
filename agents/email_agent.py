from memory.shared_memory import SharedMemory
import re

class EmailAgent:
    def __init__(self, shared_memory: SharedMemory):
        self.shared_memory = shared_memory

    def process(self, content: str, source: str, thread_id=None):
        # Try to extract sender from the first line (mocked if not found)
        sender_match = re.search(r'From: (.+)', content)
        sender = sender_match.group(1) if sender_match else 'mock_sender@example.com'
        # Extract subject as thread_id if not provided
        subject_match = re.search(r'Subject: (.+)', content)
        thread_id = thread_id or (subject_match.group(1).strip() if subject_match else None)
        # Intent detection
        lowered = content.lower()
        if 'complaint' in lowered:
            intent = 'Complaint'
        elif 'invoice' in lowered:
            intent = 'Invoice'
        elif 'rfq' in lowered:
            intent = 'RFQ'
        elif 'regulation' in lowered:
            intent = 'Regulation'
        else:
            intent = 'Unknown'
        urgency = 'High' if 'urgent' in lowered or 'asap' in lowered else 'Normal'
        crm_dict = {
            'sender': sender,
            'intent': intent,
            'urgency': urgency,
            'body': content
        }
        log_entry = {
            'source': source,
            'file_format': 'Email',
            'extracted_fields': crm_dict,
            'thread_id': thread_id
        }
        self.shared_memory.log(log_entry)
        print(f"[EmailAgent] Processed {source}: intent={intent}, urgency={urgency}, thread_id={thread_id}") 