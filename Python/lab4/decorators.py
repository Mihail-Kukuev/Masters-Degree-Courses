import functools
import timeit


def memorize(f):
    cache = {}
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if args in cache:
            return cache[args]
        else:
            result = f(*args, **kwargs)
            cache[args] = result
            return result
    return wrapper


def profile(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        t = timeit.default_timer()
        result = f(*args, **kwargs)
        print(timeit.default_timer() - t)
        return result
    return wrapper


def convolve(k):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            result = f(*args, **kwargs)
            for x in xrange(k - 1):
                result = f(result)
            return result
        return wrapped
    return wrapper
