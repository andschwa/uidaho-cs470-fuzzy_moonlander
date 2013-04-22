#!/usr/local/bin/python

import sys


from moonlander import Moonlander


def main():
    attempts = 100
    successes = 0.0
    final_position = 0.0
    final_y_velocity = 0.0
    final_fuel = 0.0
    for _ in range(attempts):
        moonlander = Moonlander()
        while moonlander.landed == 'in_air':
            moonlander.update()
        if moonlander.landed == 'landed':
            successes += 1
        print('This moonlander {}'.format(moonlander.landed))
        final_position += abs(moonlander.x_position)
        final_y_velocity += moonlander.y_velocity
        final_fuel += moonlander.fuel
    print('Moonlander success: {} percent'.format(successes/float(attempts)))
    print('Average final position: {}'.format(final_position/float(attempts)))
    print('Average final y_velocity: {}'.format(final_y_velocity/float(attempts)))
    print('Average final fuel: {}'.format(final_fuel/float(attempts)))


if __name__ == '__main__':
    sys.exit(main())
