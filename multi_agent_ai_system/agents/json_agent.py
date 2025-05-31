import json
from multi_agent_ai_system.memory.shared_memory import SharedMemory

REQUIRED_FIELDS = ["rfq_id", "requester", "items", "due_date"]

class JSONAgent:
    def __init__(self, shared_memory: SharedMemory):
        self.shared_memory = shared_memory

    def process(self, content: str, source: str):
        try:
            data = json.loads(content)
            extracted_fields = {k: data.get(k) for k in data}
            missing_fields = [field for field in REQUIRED_FIELDS if field not in data]
            flags = {'missing_fields': missing_fields}
        except Exception as e:
            extracted_fields = {}
            flags = {'error': str(e)}
        log_entry = {
            'source': source,
            'file_format': 'JSON',
            'extracted_fields': extracted_fields,
            'flags': flags
        }
        self.shared_memory.log(log_entry)
        print(f"[JSONAgent] Processed {source}: {flags}") 