import os
import json
import random
import sys

# Constants
BASE_DIR = r'F:\AI\RosettaCodeData'  # Directory where the repository is cloned
JSON_MAX_SIZE_MB = 48         # Max size of each JSON file in megabytes
TASK_LIMIT = None             # Set this to limit the number of tasks for testing

def random_pairs(files, num_pairs=5):
    pairs = []
    if len(files) < 2:
        return pairs
    for _ in range(num_pairs):
        pairs.append(random.sample(files, 2))
    return pairs

def process_task_directory(task_path):
    solutions = []
    for root, _, files in os.walk(task_path):
        for file in files:
            if file.endswith(".txt"):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        solutions.append(f.read())
                except UnicodeDecodeError:
                    # Handle encoding issues by trying a different encoding
                    try:
                        with open(os.path.join(root, file), 'r', encoding='latin1') as f:
                            solutions.append(f.read())
                    except Exception as e:
                        print(f"Error reading file {file}: {e}", file=sys.stderr)
    return solutions

def save_json(data, index):
    filename = f"solutions_{index}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def main():
    index = 1
    current_size = 0
    json_data = {}

    for task_name in os.listdir(BASE_DIR):
        if TASK_LIMIT and len(json_data) >= TASK_LIMIT:
            break
        
        task_path = os.path.join(BASE_DIR, task_name)
        if not os.path.isdir(task_path):
            continue
        
        solutions = process_task_directory(task_path)
        pairs = random_pairs(solutions)
        
        if pairs:
            json_data[task_name] = pairs
        
        # Estimate JSON size and save if it exceeds limit
        json_size = len(json.dumps(json_data).encode('utf-8')) / (1024 * 1024)  # size in MB
        if json_size > JSON_MAX_SIZE_MB:
            save_json(json_data, index)
            index += 1
            json_data = {}
            current_size = 0

    # Save remaining data
    if json_data:
        save_json(json_data, index)

if __name__ == "__main__":
    main()
