#!/usr/local/bin/python

import sys


from moonlander import Moonlander


def main():
    moonlander = Moonlander()
    while moonlander.landed == 'in_air':
        moonlander.update()
    print('Moonlander has {}'.format(moonlander.landed))


if __name__ == '__main__':
    sys.exit(main())
