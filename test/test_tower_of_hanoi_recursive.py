import unittest

from tower_of_hanoi_recursive import Disk, Peg

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
        self._peg = Peg()

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

if __name__ == '__main__':
    unittest.main()
