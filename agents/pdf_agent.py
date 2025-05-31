import re
from memory.shared_memory import SharedMemory

class PDFAgent:
    def __init__(self, shared_memory: SharedMemory):
        self.shared_memory = shared_memory

    def process(self, content: str, source: str, thread_id=None):
        # Extract invoice fields using regex
        invoice_number = re.search(r'Invoice Number[:\s]*([A-Za-z0-9-]+)', content)
        amount = re.search(r'Amount[:\s]*\$([0-9,.]+)', content)
        due_date = re.search(r'Due Date[:\s]*([0-9-]+)', content)
        extracted_fields = {
            'invoice_number': invoice_number.group(1) if invoice_number else None,
            'amount': amount.group(1) if amount else None,
            'due_date': due_date.group(1) if due_date else None
        }
        log_entry = {
            'source': source,
            'file_format': 'PDF',
            'extracted_fields': extracted_fields,
            'thread_id': thread_id
        }
        self.shared_memory.log(log_entry)
        print(f"[PDFAgent] Processed {source}: {extracted_fields}") 