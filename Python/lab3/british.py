import re
import random
import argparse


def shuffle_letters(word):
    middle_letters = word[1:-1]
    return word[:1] + ''.join(random.sample(middle_letters, len(middle_letters))) + word[-1:]


def sort_letters(word):
    return word[:1] + ''.join(sorted(word[1:-1])) + word[-1:]


def shuffle(text, use_random):
    pattern = re.compile('(\w+(?:-\w+)*)')
    words = pattern.split(text)
    for i in range(len(words)):
        if pattern.match(words[i]):
            words[i] = shuffle_letters(words[i]) if use_random else sort_letters(words[i])
    return ''.join(words)


def run_with_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--random', action='store_true', help='Shuffle letters randomly')
    parser.add_argument('-f', '--file', help='File with text')
    parser.add_argument('-s', '--string', help='String as input text')

    args = parser.parse_args()

    text = args.string

    if args.file:
        file = open(args.file)
        text = file.read()
        file.close()

    print shuffle(text, args.random)


run_with_cmd()
