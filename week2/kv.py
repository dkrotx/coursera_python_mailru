import os
import operator
import tempfile
import argparse
from pathlib import Path
import json

def load_data(path):
    if Path(path).exists():
        with open(path) as f:
            return json.load(f)

    return []

def save_data(path, obj):
    with open(path, 'w') as f:
        json.dump(obj, f)

parser = argparse.ArgumentParser()
parser.add_argument("--key", required=True)
parser.add_argument("--val")

args = parser.parse_args()

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
data = load_data(storage_path)

if args.val:
    data.append((args.key, args.val))
    save_data(storage_path, data)
else:
    matched = map(operator.itemgetter(1), filter(lambda t: t[0] == args.key, data))
    print(', '.join(matched))
