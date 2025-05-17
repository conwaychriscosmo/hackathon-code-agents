import json
import os

def load_ticket(path):
    with open(path, 'r') as f:
        return json.load(f)

def write_files(files: dict, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    for filename, content in files.items():
        with open(os.path.join(out_dir, filename), 'w') as f:
            f.write(content)
