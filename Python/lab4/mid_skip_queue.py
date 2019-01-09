import pprint
import copy


class MidSkipQueue(object):
    def __init__(self, k, iterable=None):
        assert k > 0, "k should be positive"
        self.k = k
        self.elements = iterable[:] if iterable else []

    def append(self, *args):
        if len(self.elements) <= self.k:
            append_amount = 2 * self.k - len(self.elements)
            self.elements += list(args)[-append_amount:]
        else:
            first_part = self.elements[:self.k]
            second_part = self.elements[self.k:]
            appended_elements = list(args)[-self.k:]
            remain_amount = self.k - len(appended_elements)
            remain_elements = second_part[len(second_part) - remain_amount:len(second_part)]

            self.elements = first_part + remain_elements + appended_elements
        return None

    def index(self, value):
        for i in xrange(len(self.elements)):
            if self.elements[i] == value:
                return i
        return -1

    def __getitem__(self, item):
        if not isinstance(item, slice):
            assert -len(self.elements) < item < len(self.elements), "IndexError: queue index out of range"
        return self.elements[item]

    def __contains__(self, item):
        return item in self.elements

    def __len__(self):
        return len(self.elements)

    def __eq__(self, other):
        return self.elements == other.elements

    def __hash__(self):
        return hash(self.elements)

    def __add__(self, iterable):
        queue = copy.deepcopy(self)
        queue.append(*iterable)
        return queue

    def __str__(self):
        return pprint.pformat(self.elements)


class MidSkipPriorityQueue(MidSkipQueue):
    def append(self, *args):
        union = self.elements + list(args)
        union.sort()
        largest = union[-self.k:]
        others = union[:len(union) - len(largest)]

        self.elements = others[:self.k] + largest
        return None
