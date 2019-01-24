import re
from lexicon import WORDS
from misc import *


class Matcher:
    def __init__(self, pattern, ignore_extension=False):
        self.ignore_extension = ignore_extension
        self.pattern = pattern

    def match(self, string):
        return string == self.pattern


class Anagram(Matcher):
    def match(self, string):
        pattern = self.pattern
        if not self.ignore_extension:
            or_longer = '@' in pattern
            blanks = pattern.count('.')
            pattern = str(pattern).replace('.', '').replace('@', '')

        for i in pattern:
            if i in string:
                for j, e in enumerate(string):
                    if e == i:
                        string = string[:j] + string[j + 1:]
                        break
            else:
                return False

        if self.ignore_extension:
            return string == ''

        if or_longer:
            if len(string) >= blanks:
                return True
        else:
            if len(string) == blanks:
                return True
        return False


class Subanagram(Matcher):
    def match(self, string):
        pattern = self.pattern
        if not self.ignore_extension:
            blanks = pattern.count('.')
            pattern = pattern.replace('.', '')

        for i in pattern:
            if i in string:
                for j, e in enumerate(string):
                    if e == i:
                        string = string[:j] + string[j + 1:]
                        break

        if len(string) <= blanks:
            return True
        return False


class Pattern(Matcher):
    def match(self, string):
        pattern = self.pattern
        if not self.ignore_extension:
            pattern = pattern.replace('@', "[a-z]*")
        else:
            pattern = pattern.replace('.', '').replace('@', '')

        re_pattern = re.compile(pattern)
        m = re_pattern.match(string)
        if re_pattern.match(string) == None:
            return False
        return re_pattern.match(string)[0] == string


class Length(Matcher):
    def __init__(self, min_len=1, max_len=15):
        self.min_len = min_len
        self.max_len = max_len

    def match(self, string):
        string_len = len(string)
        return string_len >= self.min_len and string_len <= self.max_len
