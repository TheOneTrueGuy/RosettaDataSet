import json

with open('rosettacode_data.json') as file:
    data = json.load(file)

chunk_size = 5
chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

for i, chunk in enumerate(chunks):
    with open(f'RosettaCodeDataSet_{i}.json', 'w') as file:
        json.dump(chunk, file)
