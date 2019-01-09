def calculate_special_sum(n):
    return sum(x * (x + 1) for x in xrange(1, n))
