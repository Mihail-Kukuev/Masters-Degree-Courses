def get_sequence_items(k):
    element = 0
    length = 1
    mask = 1

    for i in range(k):
        tmp = (~element & mask)
        element = (element << length) | tmp
        mask = (mask << length) | mask
        length = length << 1

    return element
