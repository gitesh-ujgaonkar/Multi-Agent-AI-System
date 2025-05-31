import os
from memory.shared_memory import SharedMemory
from agents.classifier_agent import ClassifierAgent

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
        if os.path.exists(file_path):
            classifier.log_and_route(file_path)
        else:
            print(f"[Demo] Test file not found: {file_path}")
    print("\n[SharedMemory Snapshot]")
    print(shared_memory.snapshot())

if __name__ == '__main__':
    run_demo() 