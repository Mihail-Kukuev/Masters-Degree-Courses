import random
import argparse

PREDATOR = 'p'
PREY = 'f'
EMPTY = '-'


def life(input_filename, output_filename, iterations):
    with open(input_filename, 'r') as input_file:
        ocean_size, predator_twf, predator_reproduce_period, prey_reproduce_period = \
            [int(x) for x in input_file.readline().split()]

        ocean = [list(line.strip()) for line in input_file][:ocean_size]

    predators = get_predators(ocean)

    for iteration in xrange(1, iterations + 1):
        if not predators and not exists_prey(ocean):
            break

        if iteration % prey_reproduce_period == 0:
            reproduce(ocean, predators, PREY)

        if iteration % predator_reproduce_period == 0:
            reproduce(ocean, predators, PREDATOR)

        do_predators_step(ocean, predators)
        do_preys_step(ocean)

        kill_hungry_predators(ocean, predators, predator_twf)

    with open(output_filename, 'w+') as output_file:
        lines = [''.join(row) + '\n' for row in ocean]
        output_file.writelines(lines)

    return None


def exists_prey(ocean):
    for row in ocean:
        if PREY in row:
            return True
    return False


def get_predators(ocean):
    coordinates = [(x, y) for x in xrange(len(ocean))
                   for y in xrange(len(ocean))
                   if ocean[x][y] == PREDATOR]
    return {key: 0 for key in coordinates}


def reproduce(ocean, predators, animal):
    for x in xrange(len(ocean)):
        for y in xrange(len(ocean)):
            cell = neighbour_empty_cell(x, y, ocean)
            if cell is None:
                continue

            (x1, y1) = cell
            if ocean[x][y] == animal == PREY:
                ocean[x1][y1] = PREY
            elif ocean[x][y] == animal == PREDATOR:
                ocean[x1][y1] = PREDATOR
                predators[(x1, y1)] = 0


def do_predators_step(ocean, predators):
    for (x, y), time_without_food in predators.items():
        prey_cell = neighbour_prey(x, y, ocean)
        if prey_cell:
            prey_x, prey_y = prey_cell
            ocean[prey_x][prey_y] = EMPTY
            predators[x, y] = 0
        else:
            predators[x, y] += 1
            to_cell = neighbour_empty_cell(x, y, ocean)
            if to_cell:
                move(x, y, to_cell[0], to_cell[1], ocean)
                predators[to_cell] = predators[x, y]
                predators.pop((x, y))
    return None


def do_preys_step(ocean):
    preys = [(x, y) for x in xrange(len(ocean))
             for y in xrange(len(ocean)) if ocean[x][y] == PREY]

    for x, y in preys[:]:
        to_cell = neighbour_empty_cell(x, y, ocean)
        if to_cell:
            move(x, y, to_cell[0], to_cell[1], ocean)


def kill_hungry_predators(ocean, predators, time_limit):
    for (x, y), time_without_food in predators.items():
        if time_without_food == time_limit:
            predators.pop((x, y))
            ocean[x][y] = EMPTY
    return None


def neighbour_prey(x, y, ocean):
    for prey_x, prey_y in neighbour_cells(x, y, len(ocean)):
        if ocean[prey_x][prey_y] == PREY:
            return prey_x, prey_y
    return None


def move(from_x, from_y, to_x, to_y, ocean):
    ocean[to_x][to_y] = ocean[from_x][from_y]
    ocean[from_x][from_y] = EMPTY


def neighbour_empty_cell(x, y, ocean):
    for new_x, new_y in neighbour_cells(x, y, len(ocean)):
        if 0 <= new_x < len(ocean) and 0 <= new_y < len(ocean) and ocean[new_x][new_y] == EMPTY:
            return new_x, new_y
    return None


def neighbour_cells(x, y, ocean_size):
    cells = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    random.shuffle(cells)
    return [(x1, y1) for x1, y1 in cells
            if 0 <= x1 < ocean_size and 0 <= y1 < ocean_size]


def run_with_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--iterations', type=int, required=True, help='Number of iterations')
    parser.add_argument('-c', '--config', required=True, help='File with general configuration')
    parser.add_argument('-o', '--output', required=True, help='File for results output')

    args = parser.parse_args()

    life(args.config, args.output, args.iterations)


run_with_cmd()
