def get_primes(n):
    return [x for x in xrange(2, n + 1) if all([x % y for y in xrange(2, x)])]
