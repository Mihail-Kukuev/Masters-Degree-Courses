def calculate_gcd(a, b):
    return a if (b == 0) else calculate_gcd(b, a % b)
