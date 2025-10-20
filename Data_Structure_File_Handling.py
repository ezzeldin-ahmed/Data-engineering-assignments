# data_assignment2.py

from typing import TypedDict, NamedTuple
from dataclasses import dataclass
from pydantic import BaseModel
import json
import csv
import yaml
import xml.etree.ElementTree as ET
import numpy as np
import time
import pandas as pd

# -----------------------------
# 1. Create and save data in multiple formats
# -----------------------------

users = [
    {"id": 1, "name": "Akali", "email": "akali@example.com", "age": 30},
    {"id": 2, "name": "Jhin", "email": "jhin@example.com", "age": 25},
    {"id": 3, "name": "Kata", "email": "kata@example.com", "age": 27}
]

# JSON
with open("users.json", "w") as f:
    json.dump(users, f, indent=4)

# CSV
with open("users.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name", "email", "age"])
    writer.writeheader()
    writer.writerows(users)

# YAML
import yaml
from collections import OrderedDict

ordered_users = [
    OrderedDict([
        ("id", 1),
        ("name", "Akali"),
        ("email", "akali@example.com"),
        ("age", 30)
    ]),
    OrderedDict([
        ("id", 2),
        ("name", "Jhin"),
        ("email", "jhin@example.com"),
        ("age", 25)
    ]),
    OrderedDict([
        ("id", 3),
        ("name", "Kata"),
        ("email", "kata@example.com"),
        ("age", 27)
    ])
]

# ✅ Convert OrderedDict to normal dict before dumping
normal_users = [dict(u) for u in ordered_users]

with open("users.yaml", "w", encoding="utf-8") as f:
    yaml.safe_dump(normal_users, f, sort_keys=False, allow_unicode=True)



# XML
def indent(elem, level=0):
    """Helper function to indent XML for readability"""
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level + 1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

root = ET.Element("users")
for u in users:
    user_elem = ET.SubElement(root, "user")
    for k, v in u.items():
        child = ET.SubElement(user_elem, k)
        child.text = str(v)

indent(root)  # 👈 add indentation before saving

tree = ET.ElementTree(root)
tree.write("users.xml", encoding="utf-8", xml_declaration=True)
print("Wrote users.xml (formatted nicely)")


print("✅ Files created: users.json, users.csv, users.yaml, users.xml\n")

# -----------------------------
# 2. Define User structures
# -----------------------------

class UserTypedDict(TypedDict):
    id: int
    name: str
    email: str
    age: int

class UserNamedTuple(NamedTuple):
    id: int
    name: str
    email: str
    age: int

@dataclass
class UserDataClass:
    id: int
    name: str
    email: str
    age: int

class UserPydantic(BaseModel):
    id: int
    name: str
    email: str
    age: int

# Example usage
example_user = users[0]
print("TypedDict:", UserTypedDict(**example_user))
print("NamedTuple:", UserNamedTuple(**example_user))
print("DataClass:", UserDataClass(**example_user))
print("Pydantic:", UserPydantic(**example_user), "\n")

# -----------------------------
# 3. NumPy vs Python list comparison
# -----------------------------

python_list = [i for i in range(1_000_000)]
numpy_array = np.arange(1_000_000)

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper

@measure_time
def multiply_list(data, scalar):
    return [x * scalar for x in data]

@measure_time
def multiply_numpy(data, scalar):
    return data * scalar

print("⚙️ Performance Comparison:")
multiply_list(python_list, 5)
multiply_numpy(numpy_array, 5)
print()

# -----------------------------
# 4. Load CSV with pandas
# -----------------------------

df = pd.read_csv("users.csv")
print("📊 Loaded DataFrame:\n", df)
print("\n✅ All tasks completed successfully.")

