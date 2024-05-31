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
        pre_list.append("│")
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
                    line += ": " + data[k]
                print(line)
            n -= 1

class rectangle(AbstractPrinter):
    def __init__(self, icon):
        super().__init__(icon)
    
    def print(self, data, level = 0, l = [], bottom = True):
        first = False
        if level == 0:
            first = True
        if data == {}:
            return
        pre = ""
        pre_list = copy.copy(l)
        for i in pre_list:
            pre += i
        n = len(data.keys())
        pre_list.append("│")
        for k in data.keys():
            line = pre + "├"
            if type(data[k]) == dict:
                line += self.icon["intermediate"]
                line += k
            else:
                line += self.icon["leaf"]
                line += k
                if data[k] != None:
                    line += ": " + data[k]
            for i in range(len(line), 40):
                line += "─"
            line += "┤"
            if first:
                for i in range(len(line)):
                    if line[i] == "├":
                        line = line[0:i] + "┌" + line[i+1:]
                    elif line[i] == "┤":
                        line = line[0:i] + "┐" + line[i+1:]
                first = False
            if bottom and (n == 1) and type(data[k]) != dict:
                line = "└" + line[1:]
                for i in range(len(line)):
                    if line[i] == "├" or line[i] == "│":
                        line = line[0:i] + "┴" + line[i+1:]
                    elif line[i] == "┤":
                        line = line[0:i] + "┘" + line[i+1:]
            print(line)
            if type(data[k]) == dict:
                self.print(data[k], level + 1, pre_list, (n == 1) and bottom)
            n -= 1

class Explorer:
    def __init__(self):
        self.data = None

    def load(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def print(self, style, icon):
        printer = AbstractPrinter.create(style, icon)
        printer.print(self.data)