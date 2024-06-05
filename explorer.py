import json
from abc import ABC, abstractmethod
import copy

class AbstractPrinter(ABC):
    def __init__(self, icon):
        self.icon = icon

    @classmethod
    def create(cls, style, icon):
        if style == 'tree':
            return TreePrinter(icon)
        elif style == 'rectangle':
            return RectanglePrinter(icon)

    @abstractmethod
    def print(self, data):
        pass

class BuildLine(ABC):
    def __init__(self, icon):
        self.icon = icon
        self.lines = []

    @abstractmethod
    def build(self, data, level = 0, l = []):
        pass

class TreeLine(BuildLine):
    def __init__(self, icon):
        super().__init__(icon)

    def build(self, data, level = 0, l = []):
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
                self.lines.append(line)
                self.build(data[k], level + 1, pre_list)
            else:
                line += self.icon["leaf"]
                line += k
                if data[k] != None:
                    line += ": " + data[k]
                self.lines.append(line)
            n -= 1

class TreePrinter(AbstractPrinter):
    def __init__(self, icon):
        super().__init__(icon)
    
    def print(self, data):
        if data == {}:
            return
        l = TreeLine(self.icon)
        l.build(data)
        for i in l.lines:
            print(i)

class RectangleLine(BuildLine):
    def __init__(self, icon):
        super().__init__(icon)
        self.lines = []

    def build(self, data, level = 0, l = []):
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
            self.lines.append(line)
            if type(data[k]) == dict:
                self.build(data[k], level + 1, pre_list)
            n -= 1

class RectanglePrinter(AbstractPrinter):
    def __init__(self, icon):
        super().__init__(icon)
    
    def print(self, data):
        if data == {}:
            return
        l = RectangleLine(self.icon)
        l.build(data)
        lines = l.lines.copy()

        for i in range(len(lines[0])):
            if lines[0][i] == "├":
                lines[0] = lines[0][0:i] + "┌" + lines[0][i+1:]
            elif lines[0][i] == "┤":
                lines[0] = lines[0][0:i] + "┐" + lines[0][i+1:]

        lines[-1] = "└" + lines[-1][1:]
        for i in range(1, len(lines[-1])):
            if lines[-1][i] == "├" or l.lines[-1][i] == "│":
                lines[-1] = lines[-1][0:i] + "┴" + lines[-1][i+1:]
            elif lines[-1][i] == "┤":
                lines[-1] = lines[-1][0:i] + "┘" + lines[-1][i+1:]

        for i in lines:
            print(i)

class Explorer:
    def __init__(self):
        self.data = None

    def load(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def print(self, style, icon):
        printer = AbstractPrinter.create(style, icon)
        printer.print(self.data)