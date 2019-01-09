def distribute(sequence, k):
    minimum = min(sequence)
    interval = (max(sequence) - minimum) * 1.0 / k
    hist = [0] * k
    for x in sequence:
        range_index = int((x - minimum) / interval)
        range_index -= 1 if range_index == k else 0
        hist[range_index] += 1
    return hist


def print_hist(distribution):
    for level in range(max(distribution) + 1, 0, -1):
        print ''.join([' * ' if x >= level else ' - ' for x in distribution])
