import re


def index(string, numbers, k=5):
    if type(numbers) is int:
        numbers = [numbers]
    indexes = [m.start() + 1 for number in numbers
               for m in re.finditer('(?={0})'.format(number), string)]
    indexes.sort()
    return (len(indexes), indexes[:k])
