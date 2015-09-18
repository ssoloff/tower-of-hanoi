import unittest
import unittest.mock as mock

from tower_of_hanoi import Disk, Game, Peg

class DiskTestCase(unittest.TestCase):
    def test____eq____when_self_equals_other__returns_true(self):
        self.assertEqual(Disk(1), Disk(1))

    def test____eq____when_self_size_not_equals_other__returns_false(self):
        self.assertNotEqual(Disk(1), Disk(2))

    def test____lt____when_self_equals_other__returns_false(self):
        self.assertFalse(Disk(1) < Disk(1))

    def test____lt____when_self_greater_than_other__returns_false(self):
        self.assertFalse(Disk(2) < Disk(1))

    def test____lt____when_self_less_than_other__returns_true(self):
        self.assertTrue(Disk(1) < Disk(2))

class PegTestCase(unittest.TestCase):
    def _create_peg(self, name=None, disks=[]):
        return Peg(name if None else self._name, disks)

    def setUp(self):
        self._disk_1 = Disk(1)
        self._disk_2 = Disk(2)
        self._disk_3 = Disk(3)
        self._name = 'name'

    def test____eq____when_self_equals_other__returns_true(self):
        self.assertEqual(Peg(self._name, [self._disk_1]), Peg(self._name, [self._disk_1]))

    def test____eq____when_self_disks_not_equals_other__returns_false(self):
        self.assertNotEqual(Peg(self._name, [self._disk_1]), Peg(self._name, [self._disk_2]))

    def test____eq____when_self_name_not_equals_other__returns_false(self):
        self.assertNotEqual(Peg(self._name, [self._disk_1]), Peg('other-name', [self._disk_1]))

    def test__disks__returns_copy(self):
        peg = self._create_peg()

        peg.disks().append(self._disk_1)

        self.assertEqual([], peg.disks())

    def test__disks__returns_in_order_from_bottom_to_top(self):
        peg = self._create_peg(disks=[self._disk_3, self._disk_2, self._disk_1])

        self.assertEqual([self._disk_3, self._disk_2, self._disk_1], peg.disks())

    def test__is_empty__when_empty__returns_true(self):
        peg = self._create_peg()

        self.assertTrue(peg.is_empty())

    def test__is_empty__when_not_empty__returns_false(self):
        peg = self._create_peg(disks=[self._disk_1])

        self.assertFalse(peg.is_empty())

    def test__pop__when_empty__raises_exception(self):
        peg = self._create_peg()

        with self.assertRaises(Exception):
            peg.pop()

    def test__pop__when_not_empty__returns_new_peg_with_top_disk_removed_and_removed_disk(self):
        peg = self._create_peg(disks=[self._disk_2, self._disk_1])

        new_peg, popped_disk = peg.pop()

        self.assertEqual(self._create_peg(disks=[self._disk_2]), new_peg)
        self.assertEqual(self._disk_1, popped_disk)

    def test__push__when_empty__returns_new_peg_with_added_disk(self):
        peg = self._create_peg()

        new_peg = peg.push(self._disk_1)

        self.assertEqual(self._create_peg(disks=[self._disk_1]), new_peg)

    def test__push__when_disk_smaller_than_top_disk__returns_peg_with_added_disk_on_top(self):
        peg = self._create_peg(disks=[self._disk_2])

        new_peg = peg.push(self._disk_1)

        self.assertEqual(self._create_peg(disks=[self._disk_2, self._disk_1]), new_peg)

    def test__push__when_disk_same_as_top_disk__raises_exception(self):
        peg = self._create_peg(disks=[self._disk_1])

        with self.assertRaises(Exception):
            peg.push(self._disk_1)

    def test__push__when_disk_larger_than_top_disk__raises_exception(self):
        peg = self._create_peg(disks=[self._disk_1])

        with self.assertRaises(Exception):
            peg.push(self._disk_2)

class GameTestCase(unittest.TestCase):
    def _create_peg_a(self, disks):
        return Peg('a', disks)

    def _create_peg_b(self, disks=[]):
        return Peg('b', disks)

    def _create_peg_c(self, disks=[]):
        return Peg('c', disks)

    def setUp(self):
        self._disk_1 = Disk(1)
        self._disk_2 = Disk(2)
        self._disk_3 = Disk(3)
        self._disk_4 = Disk(4)
        self._peg_b = self._create_peg_b()
        self._peg_c = self._create_peg_c()
        self._game = Game()

    def test__create_peg__returns_peg_with_specified_name(self):
        name = 'name'

        peg = self._game.create_peg(name)

        self.assertEqual(name, peg.name())

    def test__create_peg__when_disk_count_is_0__returns_empty_peg(self):
        peg = self._game.create_peg('name', 0)

        self.assertEqual([], peg.disks())

    def test__create_peg__when_disk_count_is_1__returns_peg_with_1_disk(self):
        peg = self._game.create_peg('name', 1)

        self.assertEqual([self._disk_1], peg.disks())

    def test__create_peg__when_disk_count_is_3__returns_peg_with_3_disks_in_ascending_order_from_top(self):
        peg = self._game.create_peg('name', 3)

        self.assertEqual([self._disk_3, self._disk_2, self._disk_1], peg.disks())

    def test__move__when_disk_count_is_1__invokes_callback_after_each_move(self):
        move_spy = mock.Mock()
        peg_a = self._create_peg_a([self._disk_1])

        self._game.move(1, peg_a, self._peg_c, self._peg_b, move_spy)

        expected_move_spy_call_args_list = [
            mock.call([
                self._create_peg_a([]),
                self._create_peg_c([self._disk_1]),
                self._create_peg_b([])
            ])
        ]
        self.assertEqual(expected_move_spy_call_args_list, move_spy.call_args_list)

    def test__move__when_disk_count_is_1__moves_disks_from_peg_a_to_peg_c(self):
        peg_a = self._create_peg_a([self._disk_1])

        new_peg_a, new_peg_c, new_peg_b = self._game.move(1, peg_a, self._peg_c, self._peg_b)

        self.assertEqual(self._create_peg_a([]), new_peg_a)
        self.assertEqual(self._create_peg_b([]), new_peg_b)
        self.assertEqual(self._create_peg_c([self._disk_1]), new_peg_c)

    def test__move__when_disk_count_is_2__invokes_callback_after_each_move(self):
        move_spy = mock.Mock()
        peg_a = self._create_peg_a([self._disk_2, self._disk_1])

        self._game.move(2, peg_a, self._peg_c, self._peg_b, move_spy)

        expected_move_spy_call_args_list = [
            mock.call([
                self._create_peg_a([self._disk_2]),
                self._create_peg_b([self._disk_1]),
                self._create_peg_c([])
            ]),
            mock.call([
                self._create_peg_a([]),
                self._create_peg_c([self._disk_2]),
                self._create_peg_b([self._disk_1])
            ]),
            mock.call([
                self._create_peg_b([]),
                self._create_peg_c([self._disk_2, self._disk_1]),
                self._create_peg_a([])
            ])
        ]
        self.assertSequenceEqual(expected_move_spy_call_args_list, move_spy.call_args_list)

    def test__move__when_disk_count_is_2__moves_disks_from_peg_a_to_peg_c(self):
        peg_a = self._create_peg_a([self._disk_2, self._disk_1])

        new_peg_a, new_peg_c, new_peg_b = self._game.move(2, peg_a, self._peg_c, self._peg_b)

        self.assertEqual(self._create_peg_a([]), new_peg_a)
        self.assertEqual(self._create_peg_b([]), new_peg_b)
        self.assertEqual(self._create_peg_c([self._disk_2, self._disk_1]), new_peg_c)

    def test__move__when_disk_count_is_3__moves_disks_from_peg_a_to_peg_c(self):
        peg_a = self._create_peg_a([self._disk_3, self._disk_2, self._disk_1])

        new_peg_a, new_peg_c, new_peg_b = self._game.move(3, peg_a, self._peg_c, self._peg_b)

        self.assertEqual(self._create_peg_a([]), new_peg_a)
        self.assertEqual(self._create_peg_b([]), new_peg_b)
        self.assertEqual(self._create_peg_c([self._disk_3, self._disk_2, self._disk_1]), new_peg_c)

    def test__move__when_disk_count_is_4__moves_disks_from_peg_a_to_peg_c(self):
        peg_a = self._create_peg_a([self._disk_4, self._disk_3, self._disk_2, self._disk_1])

        new_peg_a, new_peg_c, new_peg_b = self._game.move(4, peg_a, self._peg_c, self._peg_b)

        self.assertEqual(self._create_peg_a([]), new_peg_a)
        self.assertEqual(self._create_peg_b([]), new_peg_b)
        self.assertEqual(self._create_peg_c([self._disk_4, self._disk_3, self._disk_2, self._disk_1]), new_peg_c)

    def test__move__when_disk_count_exceeds_source_peg_disk_count__raises_exception(self):
        peg_a = self._create_peg_a([self._disk_1])

        with self.assertRaises(Exception):
            self._game.move(2, peg_a, self._peg_c, self._peg_b)

if __name__ == '__main__':
    unittest.main()
