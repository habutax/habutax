import unittest

from . import context

from habutax import enum

class EnumTestCase(unittest.TestCase):
    def test_enum_make(self):
        e = enum.make('a', {'b': "yay!", 'c': "foobar"})
        self.assertEqual(str(e.b), "b")
        self.assertEqual(str(e.c), "c")
        self.assertEqual(str(e['c']), "c")
        self.assertEqual(e.b.value, "yay!")
        self.assertEqual(e.c.name, "c")
        self.assertEqual(e.__members__['c'].value, "foobar")
