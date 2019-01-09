from itertools import izip


def unique(iterable):
    checked = set([])
    for item in iterable:
        if item not in checked:
            checked.add(item)
            yield item


def transpose(iterables):
    return map(list, izip(*iterables))
