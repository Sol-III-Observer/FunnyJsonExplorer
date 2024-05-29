import json
from abc import ABC, abstractmethod
import copy

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
        super().__init__(icon)
    
    def print(self, data, level = 0, l = []):
        if data == {}:
            return
        pre = ""
        pre_list = copy.copy(l)
        for i in pre_list:
            pre += i
        n = len(data.keys())
        pre_list.append("|")
        for k in data.keys():
            line = ""
            if n == 1:
                line = pre + "└"
                pre_list[level] = " "
            else:
                line = pre + "├"
            if type(data[k]) == dict:
                line += self.icon["intermediate"]
                line += k
                print(line)
                self.print(data[k], level + 1, pre_list)
            else:
                line += self.icon["leaf"]
                line += k
                if data[k] != None:
                    line += ':' + data[k]
                print(line)
            n -= 1

class rectangle(AbstractPrinter):
    def __init__(self, icon):
        super().__init__(icon)
    
    def print(self, data, level = 0):
        pass

class Explorer:
    def __init__(self):
        self.data = None

    def load(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def print(self, style, icon):
        printer = AbstractPrinter.create(style, icon)
        printer.print(self.data)