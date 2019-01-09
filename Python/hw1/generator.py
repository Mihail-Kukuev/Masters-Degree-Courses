import random
import argparse

PREDATOR = 'p'
PREY = 'f'
WALL = 'w'
EMPTY = '-'


def add_objects(obj, ocean):
    size = len(ocean)
    count = random.randrange(size / 2, size * 2)
    while count > 0:
        x = random.randrange(size)
        y = random.randrange(size)
        if ocean[x][y] == EMPTY:
            ocean[x][y] = obj
            count -= 1
    return None


def generate(filename, size):
    ocean = [[EMPTY] * size for i in range(size)]

    add_objects(WALL, ocean)
    add_objects(PREDATOR, ocean)
    add_objects(PREY, ocean)

    interval = 30
    params_string = str(size)
    for i in xrange(3):
        number = random.randrange(interval / 2, interval * 2)
        params_string += ' ' + str(number)

    with open(filename, 'w+') as f:
        f.write(params_string + '\n')
        f.writelines([''.join(row) + '\n' for row in ocean])

    return None


def run_with_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help='File for output')
    parser.add_argument('-s', '--size', type=int, default=10, help='Size of square 2D ocean')

    args = parser.parse_args()

    generate(args.file, args.size)


run_with_cmd()
