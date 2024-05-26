import json
from abc import ABC, abstractmethod

class AbstractPrinter(ABC):
    def __init__(self, icon):
        self.icon = icon

    @classmethod
    def create(cls, style, icon):
        if style == 'tree':
            return tree(icon)
        elif style == 'rectangle':
            return rectangle(icon)

    @abstractmethod
    def print(self, data):
        pass

class tree(AbstractPrinter):
    def __init__(self, icon):
        super().__init__(self, icon)
    
    def print(self, data):
        print(json.dumps(data, indent=4))

class rectangle(AbstractPrinter):
    def __init__(self, icon):
        super().__init__(self, icon)
    
    def print(self, data):
        print(json.dumps(data, indent=4))

class Explorer:
    def __init__(self):
        self.data = None

    def load(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def print(self, style, icon):
        printer = AbstractPrinter.create(style, icon)
        printer.print(self.data)