from lexicon import WORDS
from matcher import *
from misc import *


def anagram_question(alphagram):
    alphagram = alphagrammize(alphagram)
    print(alphagram)
    response = None
    anagrams = search(Anagram(alphagram, True))
    correct_answers = []
    wrong_answers = []

    while response != " ":
        response = input()

        if response != ' ':
            response = response.strip()

        if response == "!":
            result = {}
            break

        if alphagrammize(response) == alphagram:
            if response not in correct_answers and response not in wrong_answers:
                if response in anagrams:
                    correct_answers.append(response)
                else:
                    wrong_answers.append(response)
            else:
                print("Duplicate response")
        else:
            if response == " ":
                missed_answers = []
                for j in anagrams:
                    if j not in correct_answers:
                        missed_answers.append(j)
                print("Correct responses")
                print(correct_answers)
                print("Missed responses")
                print(missed_answers)
                print("Wrong responses")
                print(wrong_answers)
                print()

                result = {"Correct": correct_answers,
                          "Missed": missed_answers,
                          "Wrong": wrong_answers}
            else:
                print("Invalid response")
    return (result, response != "!")


def anagram_quiz(quiz):
    alphagrams = alphagrammize_list(quiz)
    results = {}

    n = 0
    for i, e in enumerate(alphagrams):
        print(str(len(alphagrams) - i) + " questions left")
        print(e)
        response = None
        anagrams = search(Anagram(e, True))
        correct_answers = []
        wrong_answers = []
        while response != " " or response == "done":
            response = input()
            if alphagrammize(response) == e:
                if response not in correct_answers and response not in wrong_answers:
                    if response in anagrams:
                        correct_answers.append(response)
                    else:
                        wrong_answers.append(response)
                else:
                    print("Duplicate response")
            else:
                if response == "done":
                    break
                if response == " ":
                    missed_answers = []
                    for j in anagrams:
                        if j not in correct_answers:
                            missed_answers.append(j)
                    print("Correct responses")
                    print(correct_answers)
                    print("Missed responses")
                    print(missed_answers)
                    print("Wrong responses")
                    print(wrong_answers)
                    print()

                    results[e] = {"Correct responses": correct_answers,
                                  "Missed responses": missed_answers,
                                  "Wrong responses": wrong_answers}
                else:
                    print("Invalid response")
        if response == "done":
            break
    return results
