def get_nearest_lucky_ticket(ticket):
    next_ticket = ticket
    previous_ticket = ticket - 1

    while True:
        if is_lucky(next_ticket):
            return next_ticket
        if is_lucky(previous_ticket):
            return previous_ticket
        next_ticket += 1
        previous_ticket -= 1


def is_lucky(number):
    return digits_sum(number / 1000) == digits_sum(number % 1000)


def digits_sum(number):
    sum = 0
    while number > 0:
        sum += number % 10
        number /= 10
    return sum
