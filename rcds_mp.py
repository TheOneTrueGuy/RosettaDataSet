import os
import json
import random
import chardet

# Define the directory where the Rosetta Code data is stored
data_directory = r'F:\AI\RosettaCodeData'

# Create a list to store the JSON data
json_data = []

# Iterate over the tasks in the data directory
for task_name in os.listdir(data_directory):
    task_directory = os.path.join(data_directory, task_name)
    
    # Check if the task directory exists
    if os.path.isdir(task_directory):
        # Create a list to store the solutions for the task
        task_solutions = []
        
        # Iterate over the languages in the task directory
        for language in os.listdir(task_directory):
            language_file = os.path.join(task_directory, language)
            
            # Check if the language file exists
            if os.path.isfile(language_file):
                # Open the file in binary mode
                with open(language_file, 'rb') as file:
                    # Read the content of the file
                    content = file.read()
                    
                # Detect the encoding of the content
                encoding = chardet.detect(content)['encoding']
                
                # Decode the content using the detected encoding
                content = content.decode(encoding, errors='replace')
                
                # Add the content to the task's list of solutions
                task_solutions.append(content)
        
        # Randomly choose multiple pairs of solutions for the task
        if len(task_solutions) > 1:
            for _ in range(5):  # Generate 5 pairs of solutions for each task
                random_solutions = random.sample(task_solutions, 2)
                
                # Create a JSON object for the task
                json_object = {
                    'task_type': task_name,
                    'solution1': random_solutions[0],
                    'solution2': random_solutions[1]
                }
                
                # Add the JSON object to the list
                json_data.append(json_object)

# Write the JSON data to a file
with open('rosettacode_data.json', 'w') as file:
    json.dump(json_data, file, indent=4)
