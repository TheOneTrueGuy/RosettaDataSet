import os
import json
import random
import chardet
import logging

# Set up logging
logging.basicConfig(filename='rosetta_code_processing.log', level=logging.INFO)

# Set constants
TASK_LIMIT = 100  # Limit the number of tasks processed for testing purposes
MAX_JSON_SIZE = 48 * 1024 * 1024  # Maximum size of a JSON file in bytes

# Function to detect encoding and read a file
def read_file(file_path):
    print(f"Running read_file for {file_path}")
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        encoding = chardet.detect(raw_data)['encoding']
        return raw_data.decode(encoding)

# Function to process a task directory
def process_task_directory(task_dir):
    print(f"Running process_task_directory for {task_dir}")
    task_name = os.path.basename(task_dir)
    task_description_path = os.path.join(task_dir, '00-TASK.txt')
    task_description = read_file(task_description_path) if os.path.exists(task_description_path) else "No description available"
    
    solutions = []
    print(f"Entering loop to process language directories in {task_dir}")
    for lang_dir in os.listdir(task_dir):
        lang_dir_path = os.path.join(task_dir, lang_dir)
        if os.path.isdir(lang_dir_path):  # Check if it's a directory
            print(f"Entering loop to process files in {lang_dir_path}")
            for file in os.listdir(lang_dir_path):
                file_path = os.path.join(lang_dir_path, file)
                if os.path.isfile(file_path):  # Check if it's a file
                    try:
                        solution = read_file(file_path)
                        solutions.append({"language": lang_dir, "solution": solution})
                    except Exception as e:
                        logging.error(f"Error reading file {file_path}: {str(e)}")
            print(f"Exiting loop for files in {lang_dir_path}")
    print(f"Exiting loop for language directories in {task_dir}")
    return task_name, task_description, solutions

# Function to generate random pairs
def random_pairs(solutions, num_pairs):
    print(f"Running random_pairs with {len(solutions)} solutions and {num_pairs} pairs requested")
    pairs = []
    if len(solutions) >= 2:  # Ensure there are at least 2 solutions
        for _ in range(min(num_pairs, len(solutions) // 2)):  # Limit pairs to available solutions
            pair = random.sample(solutions, 2)
            pairs.append([{"language": pair[0]["language"], "solution": pair[0]["solution"]}, {"language": pair[1]["language"], "solution": pair[1]["solution"]}])
    return pairs

# Function to save JSON data
def save_json(data, file_num):
    print(f"Running save_json for file number {file_num}")
    json_file = f"rosetta_code_data_{file_num}.json"
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4, separators=(',', ': '))
    logging.info(f"JSON data saved to {json_file}")

# Main script
task_count = 0
json_data = []
json_size = 0
file_num = 1

print("Entering main loop to process task directories")
for task_dir in os.listdir(os.path.join('RosettaCodeData', 'Task')):
    task_dir_path = os.path.join('RosettaCodeData', 'Task', task_dir)
    if os.path.isdir(task_dir_path):  # Check if it's a directory
        task_name, task_description, solutions = process_task_directory(task_dir_path)
        pairs = random_pairs(solutions, 5)
        task_json = {"task_name": task_name, "task_description": task_description, "solution_pairs": pairs}
        json_data.append(task_json)
        json_size += len(json.dumps(task_json, separators=(',', ':')))
        
        if json_size > MAX_JSON_SIZE:
            save_json(json_data, file_num)
            json_data = []
            json_size = 0
            file_num += 1
        
        task_count += 1
        if task_count >= TASK_LIMIT:
            break
print("Exiting main loop for task directories")

if json_data:
    save_json(json_data, file_num)