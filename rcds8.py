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
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        encoding = chardet.detect(raw_data)['encoding']
        return raw_data.decode(encoding)

# Function to process a task directory
def process_task_directory(task_dir):
    task_name = os.path.basename(task_dir)
    solutions = []
    for lang_dir in os.listdir(task_dir):
        lang_dir_path = os.path.join(task_dir, lang_dir)
        if os.path.isdir(lang_dir_path):  # Check if it's a directory
            for file in os.listdir(lang_dir_path):
                file_path = os.path.join(lang_dir_path, file)
                if os.path.isfile(file_path):  # Check if it's a file
                    try:
                        solution = read_file(file_path)
                        solutions.append(solution)
                    except Exception as e:
                        logging.error(f"Error reading file {file_path}: {str(e)}")
    return task_name, solutions

# Function to generate random pairs
def random_pairs(solutions, num_pairs):
    pairs = []
    if len(solutions) >= 2:  # Ensure there are at least 2 solutions
        for _ in range(min(num_pairs, len(solutions) // 2)):  # Limit pairs to available solutions
            pair = random.sample(solutions, 2)
            pairs.append(pair)
            solutions.remove(pair[0])  # Remove used solutions to avoid duplicates
            solutions.remove(pair[1])
    return pairs

# Function to save JSON data
def save_json(data, file_num):
    json_file = f"rosetta_code_data_{file_num}.json"
    with open(json_file, 'w') as f:
        json.dump(data, f, separators=(',', ':'))
    logging.info(f"JSON data saved to {json_file}")

# Main script
task_count = 0
json_data = []
json_size = 0
file_num = 1

for task_dir in os.listdir('RosettaCodeData'):
    task_dir_path = os.path.join('RosettaCodeData', task_dir)
    if os.path.isdir(task_dir_path):  # Check if it's a directory
        if task_dir != '.git':  # Skip the .git directory
            task_name, solutions = process_task_directory(task_dir_path)
            pairs = random_pairs(solutions, 5)
            task_json = {"task_name": task_name, "solution_pairs": pairs}
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

if json_data:
    save_json(json_data, file_num)
