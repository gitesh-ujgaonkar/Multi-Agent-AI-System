import os
from memory.shared_memory import SharedMemory
from agents.classifier_agent import ClassifierAgent
import re

def run_demo():
    shared_memory = SharedMemory()
    classifier = ClassifierAgent(shared_memory)
    test_dir = os.path.join(os.path.dirname(__file__), 'test_inputs')
    test_files = [
        os.path.join(test_dir, 'invoice.pdf'),
        os.path.join(test_dir, 'rfq.json'),
        os.path.join(test_dir, 'complaint_email.txt')
    ]
    for file_path in test_files:
        thread_id = None
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            subject_match = re.search(r'Subject: (.+)', content)
            thread_id = subject_match.group(1).strip() if subject_match else None
        classifier.log_and_route(file_path, thread_id=thread_id)
    print("\n[SharedMemory Snapshot]")
    print(shared_memory.snapshot())

if __name__ == '__main__':
    run_demo() 