import os
import json
from typing import List

def print_with_indent(value, indent=0):
    indentation = '\t' * indent
    print(f'{indentation}{value}')


class Entry:
    def __init__(self, title, entries=None, parent=None):
        self.title = title
        if entries is None:
            entries = []
        self.entries = entries
        self.parent = parent

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent=indent + 1)

    def __str__(self):
        return self.title

    def json(self):
        return {
            "title": self.title,
            "entries": [
                entry.json() if isinstance(entry, Entry) else str(entry) for entry in self.entries
            ]
        }

    @classmethod
    def from_json(cls, value):
        new_entry = cls(value['title'])
        for sub_entry in value.get('entries', []):
            new_entry.add_entry(cls.from_json(sub_entry))
        return new_entry

    def save(self, path):
        file_path = f'{path}/{self.title}.json'
        with open(file_path, 'w') as file:
            json.dump(self.json(), file, indent=4)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return cls.from_json(data)


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path: str = data_path
        self.entries: List[Entry] = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for filename in os.listdir(self.data_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_path, filename)
                entry = Entry.load(filepath)
                self.entries.append(entry)

    def add_entry(self, title: str):
        new_entry = Entry(title)
        self.entries.append(new_entry)

