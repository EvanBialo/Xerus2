from lexicon import WORDS
import matcher


def alphagrammize(word):
    return ''.join(sorted(word))


def alphagrammize_list(l):
    alphagrams = []

    for i in l:
        if alphagrammize(i) not in alphagrams:
            alphagrams.append(alphagrammize(i))
    return alphagrams


def search(*matchers, words=WORDS):
    for i in matchers:
        words2 = []
        for j, word in enumerate(words):
            if i.match(word):
                words2.append(word)
        words = words2
    return words


def multi_match(string, *matchers):
    for i in matchers:
        if not matcher.Subanagram("...").match(string):
            return False
    return True


if __name__ == "__main__":
    print(search(matcher.Anagram("uniist.")))