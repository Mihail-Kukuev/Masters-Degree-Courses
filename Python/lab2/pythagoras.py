def get_pythagoras_triples(n):
    return [(x, y, z) for x in xrange(1, n + 1)
            for y in xrange(1, n + 1)
            for z in xrange(1, n + 1)
            if x * x + y * y == z * z]


print get_pythagoras_triples(10)