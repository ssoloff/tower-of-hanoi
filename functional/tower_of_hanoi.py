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

    def __eq__(self, other):
        return self._size == other._size

    def __lt__(self, other):
        return self._size < other._size

    def __repr__(self):
        return 'Disk(size={size})'.format(size=self._size)

    def size(self):
        '''
        Returns the size of the disk.

        :returns: The size of the disk.
        '''

        return self._size

class Peg:
    '''
    A peg upon which disks are stacked in the Tower of Hanoi game.

    Disks may only be stacked in order of decreasing size.
    '''

    def __init__(self, name, disks=[]):
        '''
        Initializes a new instance of the `Peg' class.

        :param name: The peg name.
        :param disks: The optional sequence of disks on the peg ordered from
            bottom to top.  Defaults to an empty sequence.
        '''

        self._disks = disks[:]
        self._name = name

    def __eq__(self, other):
        return (self._name == other._name) and (self._disks == other._disks)

    def __repr__(self):
        return 'Peg(name={name}, disks={disks})'.format(name=self._name, disks=self._disks)

    def _is_smaller_than_top_disk(self, disk):
        return True if self.is_empty() else disk < self._peek()

    def _peek(self):
        return self._disks[-1]

    def disks(self):
        '''
        Returns a sequence of disks on the peg ordered from bottom to top.

        :returns: A sequence of disks on the peg ordered from bottom to top.
        '''

        return self._disks[:]

    def is_empty(self):
        '''
        Indicates the peg is empty.

        :returns: `True` if the peg is empty; otherwise `False`.
        '''

        return len(self._disks) == 0

    def name(self):
        '''
        Gets the peg name.

        :returns: The peg name.
        '''

        return self._name

    def pop(self):
        '''
        Removes the disk at the top of the peg.

        :returns: A tuple containing a new peg with the top disk removed and
            the disk that was removed.

        :raises: Exception - If the peg is empty.
        '''

        if self.is_empty():
            raise Exception('peg is empty')

        return (Peg(self._name, self._disks[0:-1]), self._peek())

    def push(self, disk):
        '''
        Adds the disk to the top of the peg.

        :param disk: The disk to add.
        :type disk: Disk

        :returns: A new peg with the pushed disk added to the top.

        :raises: Exception - If the disk is not smaller than the top disk.
        '''

        if not self._is_smaller_than_top_disk(disk):
            raise Exception('disk must be smaller than top disk')

        return Peg(self._name, self._disks + [disk])

class Game:
    '''
    Facade for the three-peg Tower of Hanoi game.
    '''

    def create_peg(self, name, disk_count=0):
        ''''
        Returns a new peg with the specified name and containing the specified
        number of disks in descending order of size from the bottom to the top.

        :param name: The peg name.
        :type name: str
        :param disk_count: The number of disks to add to the peg; must not be
            negative.
        :type disk_count: int

        :returns: A new peg.
        '''

        assert disk_count >= 0

        return Peg(name, [Disk(disk_size) for disk_size in range(disk_count, 0, -1)])

    def move(self, disk_count, source_peg, destination_peg, intermediate_peg, callback=(lambda *args, **kwargs: None)):
        '''
        Moves the specified count of disks from the source peg to the
        destination peg.

        :param disk_count: The count of disks to move; must be positive.
        :type disk_count: int
        :param source_peg: The peg containing the disks to move.
        :type source_peg: Peg
        :param destination_peg: The peg to which the disks will be moved.
        :type destination_peg: Peg
        :param intermediate_peg: The peg to be used to facilitate the move
            according to the game rules.
        :type intermediate_peg: Peg
        :param callback: The optional callback to be invoked *after* each disk
            is moved.  The callback will receive a sequence of all pegs in no
            particular order.

        :returns: A tuple containing the new source, destination, and
            intermediate pegs that reflect the result of the move.
        '''

        assert disk_count > 0

        if disk_count > 1:
            source_peg, intermediate_peg, destination_peg = self.move(disk_count - 1, source_peg, intermediate_peg, destination_peg, callback)
        source_peg, disk = source_peg.pop()
        destination_peg = destination_peg.push(disk)
        callback([source_peg, destination_peg, intermediate_peg])
        if disk_count > 1:
            intermediate_peg, destination_peg, source_peg = self.move(disk_count - 1, intermediate_peg, destination_peg, source_peg, callback)

        return (source_peg, destination_peg, intermediate_peg)