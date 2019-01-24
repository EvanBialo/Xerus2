from lexicon import WORDS
from cardbox import cardbox_quiz
from matcher import *
from quiz import anagram_question, anagram_quiz

default_cardbox = 'evan'


def judge(*words):
    for word in words:
        if word not in WORDS:
            return False
    return True


def quiz_from_cardbox(*matchers, cb=dcb):
    cardbox_quiz(cb, 0.01, 3, 2, 1, *matchers)


def quiz(*matchers):
    anagram_quiz(*matchers)


if __name__ == "__main__":
    quiz_from_cardbox()
