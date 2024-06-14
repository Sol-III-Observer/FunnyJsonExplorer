import json
from abc import ABC, abstractmethod
import copy

class lines:
    def __init__(self):
        self.__list = []
        self.__len = 0

    def append(self, line):
        self.__list.append(line)
        self.__len += 1

    def get(self, index):
        if index >= self.__len or index < 0:
            return None
        return self.__list[index]
    
    def __len__(self):
        return self.__len

class linesIterator:
    def __init__(self, lines):
        self.lines = lines
        self.__index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.__index >= len(self.lines):
            raise StopIteration
        result = self.lines.get(self.__index)
        self.__index += 1
        return result

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

class LineBuilder(ABC):
    def __init__(self, icon):
        self.icon = icon
        self.lines = lines()

    @abstractmethod
    def build(self, data, level = 0, l = []):
        pass

class TreeLine(LineBuilder):
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
        for i in linesIterator(l.lines):
            print(i)

class RectangleLine(LineBuilder):
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

        for (i, line) in enumerate(linesIterator(l.lines)):
            s = line
            if i == 0:
                for j in range(len(s)):
                    if s[j] == "├":
                        s = s[0:j] + "┌" + s[j+1:]
                    elif s[j] == "┤":
                        s = s[0:j] + "┐" + s[j+1:]
            if i == len(l.lines) - 1:
                s = "└" + s[1:]
                for j in range(1, len(s)):
                    if s[j] == "├" or s[j] == "│":
                        s = s[0:j] + "┴" + s[j+1:]
                    elif s[j] == "┤":
                        s = s[0:j] + "┘" + s[j+1:]
            print(s)

class Explorer:
    def __init__(self):
        self.data = None

    def load(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def print(self, style, icon):
        printer = AbstractPrinter.create(style, icon)
        printer.print(self.data)