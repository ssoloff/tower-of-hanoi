#!/usr/bin/env python3

class Disk:
    '''
    A disk in the Tower of Hanoi game.
    '''

    def __init__(self, size):
        '''
        Initializes a new instance of the `Disk` class.

        :param size: The size of the disk; must be positive.
        :type size: int
        '''

        assert size > 0

        self._size = size

    def __lt__(self, other):
        return self._size < other._size

class Peg:
    '''
    A peg upon which disks are stacked in the Tower of Hanoi game.

    Disks may only be stacked in order of decreasing size.
    '''

    def __init__(self):
        self._stack = []

    def _is_smaller_than_top_disk(self, disk):
        return True if self.is_empty() else disk < self._peek()

    def _peek(self):
        return self._stack[-1]

    def disks(self):
        '''
        Returns a sequence of disks on the peg ordered from bottom to top.

        :returns: A sequence of disks on the peg ordered from bottom to top.
        '''

        return self._stack[:]

    def is_empty(self):
        '''
        Indicates the peg is empty.

        :returns: `True` if the peg is empty; otherwise `False`.
        '''

        return len(self._stack) == 0

    def pop(self):
        '''
        Removes the disk at the top of the peg.

        :returns: The removed disk.

        :raises: Exception - If the peg is empty.
        '''

        if self.is_empty():
            raise Exception('peg is empty')

        return self._stack.pop()

    def push(self, disk):
        '''
        Adds the disk to the top of the peg.

        :param disk: The disk to add.
        :type disk: Disk

        :raises: Exception - If the disk is not smaller than the top disk.
        '''

        if not self._is_smaller_than_top_disk(disk):
            raise Exception('disk must be smaller than top disk')

        self._stack.append(disk)

class Solver:
    '''
    Solver the three-peg Tower of Hanoi puzzle.
    '''

    def move(self, disk_count, source_peg, destination_peg, alternate_peg):
        '''
        Moves the specified count of disks from the source peg to the
        destination peg.

        :param disk_count: The count of disks to move; must be positive.
        :type disk_count: int
        :param source_peg: The peg containing the disks to move.
        :type source_peg: Peg
        :param destination_peg: The peg to which the disks will be moved.
        :type destination_peg: Peg
        :param alternate_peg: The peg to be used to facilitate the move
            according to the puzzle rules.
        :type alternate_peg: Peg
        '''

        assert disk_count > 0

        if disk_count > 1:
            self.move(disk_count - 1, source_peg, alternate_peg, destination_peg)
        destination_peg.push(source_peg.pop())
        if disk_count > 1:
            self.move(disk_count - 1, alternate_peg, destination_peg, source_peg)

if __name__ == '__main__':
    print('TODO')
