import unittest

from tower_of_hanoi_recursive import Disk, Peg, Solver

class DiskTestCase(unittest.TestCase):
    def test____lt____when_self_equals_other__returns_false(self):
        self.assertFalse(Disk(1) < Disk(1))

    def test____lt____when_self_greater_than_other__returns_false(self):
        self.assertFalse(Disk(2) < Disk(1))

    def test____lt____when_self_less_than_other__returns_true(self):
        self.assertTrue(Disk(1) < Disk(2))

class PegTestCase(unittest.TestCase):
    def setUp(self):
        self._disk_1 = Disk(1)
        self._disk_2 = Disk(2)
        self._disk_3 = Disk(3)
        self._peg = Peg('name')

    def test__disks__returns_copy(self):
        disks = self._peg.disks()
        disks.append(self._disk_1)

        self.assertTrue(self._peg.is_empty())

    def test__disks__returns_in_order_from_bottom_to_top(self):
        self._peg.push(self._disk_3)
        self._peg.push(self._disk_2)
        self._peg.push(self._disk_1)

        self.assertEqual([self._disk_3, self._disk_2, self._disk_1], self._peg.disks())

    def test__is_empty__when_empty__returns_true(self):
        self.assertTrue(self._peg.is_empty())

    def test__is_empty__when_not_empty__returns_false(self):
        self._peg.push(self._disk_1)

        self.assertFalse(self._peg.is_empty())

    def test__pop__when_empty__raises_exception(self):
        with self.assertRaises(Exception):
            self._peg.pop()

    def test__pop__when_not_empty__removes_top_disk(self):
        self._peg.push(self._disk_2)
        self._peg.push(self._disk_1)

        popped_disk = self._peg.pop()

        self.assertEqual(self._disk_1, popped_disk)
        self.assertEqual([self._disk_2], self._peg.disks())

    def test__push__when_empty__adds_disk(self):
        self._peg.push(self._disk_1)

        self.assertEqual([self._disk_1], self._peg.disks())

    def test__push__when_disk_smaller_than_top_disk__adds_disk_to_top(self):
        self._peg.push(self._disk_2)

        self._peg.push(self._disk_1)

        self.assertEqual([self._disk_2, self._disk_1], self._peg.disks())

    def test__push__when_disk_same_as_top_disk__raises_exception(self):
        self._peg.push(self._disk_1)

        with self.assertRaises(Exception):
            self._peg.push(self._disk_1)

    def test__push__when_disk_larger_than_top_disk__raises_exception(self):
        self._peg.push(self._disk_1)

        with self.assertRaises(Exception):
            self._peg.push(self._disk_2)

class SolverTestCase(unittest.TestCase):
    class _MoveSpy:
        '''
        A test spy that can be passed as the `callback` parameter of the
        `Solver.move` method.

        After `Solver.move` returns, the `disks_by_peg_name_for_each_call`
        attribute will contain the complete history of each peg's content after
        each of solver's moves.
        '''

        def __init__(self):
            print('_MoveSpy.__init__')
            self.disks_by_peg_name_for_each_call = []

        def __call__(self, *args, **kwargs):
            print('_MoveSpy.__call__')
            pegs = args[0]
            disks_by_peg_name = {peg.name(): peg.disks() for peg in pegs}
            self.disks_by_peg_name_for_each_call.append(disks_by_peg_name)

    def setUp(self):
        self._disk_1 = Disk(1)
        self._disk_2 = Disk(2)
        self._disk_3 = Disk(3)
        self._disk_4 = Disk(4)
        self._peg_a = Peg('a')
        self._peg_b = Peg('b')
        self._peg_c = Peg('c')
        self._solver = Solver()

    def test__move__when_disk_count_is_1__invokes_callback_after_each_move(self):
        move_spy = SolverTestCase._MoveSpy()
        self._peg_a.push(self._disk_1)

        self._solver.move(1, self._peg_a, self._peg_c, self._peg_b, move_spy)

        expected_disks_by_peg_name_for_each_call = [
            {
                self._peg_a.name(): [],
                self._peg_b.name(): [],
                self._peg_c.name(): [self._disk_1]
            }
        ]
        self.assertEqual(expected_disks_by_peg_name_for_each_call, move_spy.disks_by_peg_name_for_each_call)

    def test__move__when_disk_coselfunt_is_1__moves_disks_from_peg_a_to_peg_c(self):
        self._peg_a.push(self._disk_1)

        self._solver.move(1, self._peg_a, self._peg_c, self._peg_b)

        self.assertEqual([], self._peg_a.disks())
        self.assertEqual([], self._peg_b.disks())
        self.assertEqual([self._disk_1], self._peg_c.disks())

    def test__move__when_disk_count_is_2__invokes_callback_after_each_move(self):
        move_spy = SolverTestCase._MoveSpy()
        self._peg_a.push(self._disk_2)
        self._peg_a.push(self._disk_1)

        self._solver.move(2, self._peg_a, self._peg_c, self._peg_b, move_spy)

        expected_disks_by_peg_name_for_each_call = [
            {
                self._peg_a.name(): [self._disk_2],
                self._peg_b.name(): [self._disk_1],
                self._peg_c.name(): []
            },
            {
                self._peg_a.name(): [],
                self._peg_b.name(): [self._disk_1],
                self._peg_c.name(): [self._disk_2]
            },
            {
                self._peg_a.name(): [],
                self._peg_b.name(): [],
                self._peg_c.name(): [self._disk_2, self._disk_1]
            }
        ]
        self.assertEqual(expected_disks_by_peg_name_for_each_call, move_spy.disks_by_peg_name_for_each_call)

    def test__move__when_disk_count_is_2__moves_disks_from_peg_a_to_peg_c(self):
        self._peg_a.push(self._disk_2)
        self._peg_a.push(self._disk_1)

        self._solver.move(2, self._peg_a, self._peg_c, self._peg_b)

        self.assertEqual([], self._peg_a.disks())
        self.assertEqual([], self._peg_b.disks())
        self.assertEqual([self._disk_2, self._disk_1], self._peg_c.disks())

    def test__move__when_disk_count_is_3__moves_disks_from_peg_a_to_peg_c(self):
        self._peg_a.push(self._disk_3)
        self._peg_a.push(self._disk_2)
        self._peg_a.push(self._disk_1)

        self._solver.move(3, self._peg_a, self._peg_c, self._peg_b)

        self.assertEqual([], self._peg_a.disks())
        self.assertEqual([], self._peg_b.disks())
        self.assertEqual([self._disk_3, self._disk_2, self._disk_1], self._peg_c.disks())

    def test__move__when_disk_count_is_4__moves_disks_from_peg_a_to_peg_c(self):
        self._peg_a.push(self._disk_4)
        self._peg_a.push(self._disk_3)
        self._peg_a.push(self._disk_2)
        self._peg_a.push(self._disk_1)

        self._solver.move(4, self._peg_a, self._peg_c, self._peg_b)

        self.assertEqual([], self._peg_a.disks())
        self.assertEqual([], self._peg_b.disks())
        self.assertEqual([self._disk_4, self._disk_3, self._disk_2, self._disk_1], self._peg_c.disks())

    def test__move__when_disk_count_exceeds_source_peg_disk_count__raises_exception(self):
        self._peg_a.push(self._disk_1)

        with self.assertRaises(Exception):
            self._solver.move(2, self._peg_a, self._peg_c, self._peg_b)

if __name__ == '__main__':
    unittest.main()
