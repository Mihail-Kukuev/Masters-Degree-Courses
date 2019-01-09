import collections
from operator import mul
from os.path import join
from os.path import isdir
from os.path import abspath

import os


def scalar_product(first_iterable, second_iterable):
    def number_cast(a):
        return int(a, 0) if type(a) is str else a

    try:
        first_iterable = map(number_cast, first_iterable)
        second_iterable = map(number_cast, second_iterable)
        return sum(map(mul, first_iterable, second_iterable))
    except ValueError:
        return None


def flatten(iterables):
    stack = [iter(iterables)]
    while stack:
        for item in stack[-1]:
            if isinstance(item, collections.Iterable) and not isinstance(item, str):
                stack.append(iter(item))
                break
            else:
                yield item
        else:
            stack.pop()


def walk_files(path):
    tree = []
    for item in os.listdir(path):
        full_name = join(abspath(path), item)
        tree.append(walk_files(full_name) if isdir(full_name) else full_name)
    return tree
