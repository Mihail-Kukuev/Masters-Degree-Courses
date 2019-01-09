def set_bit(x, k):
    return x | 1 << k


def clear_bit(x, k):
    mask = (1 << k)
    return (x | mask) ^ mask


def test_bit(x, k):
    return bool(x & (1 << k))
