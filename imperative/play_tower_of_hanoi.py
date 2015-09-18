#!/usr/bin/env python3

import sys

from tower_of_hanoi import Game

def print_peg(peg):
    print('{0}: {1}'.format(peg.name(), ' - '.join([str(disk.size()) for disk in peg.disks()])))

def print_pegs(*args):
    print('==========')
    print_peg(peg_a)
    print_peg(peg_b)
    print_peg(peg_c)

if len(sys.argv) != 2:
    print('usage: {0} <disk_count>'.format(sys.argv[0]))
    sys,exit(1)

disk_count = int(sys.argv[1])
assert disk_count > 0

game = Game()
peg_a = game.create_peg('A', disk_count)
peg_b = game.create_peg('B')
peg_c = game.create_peg('C')

print_pegs() # display initial state
game.move(disk_count, peg_a, peg_c, peg_b, print_pegs)
