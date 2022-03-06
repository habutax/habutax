import unittest

from .. import context

import habutax.forms.ty2021 as ty2021
from habutax.inputs import InputStore
from habutax.solver import Solver

class Form1040SimpleTestCase(unittest.TestCase):
    def setUp(self):
        self.inputs = InputStore('tests/ty2021/fixtures/one_w2.habutax')
        self.solver = Solver(self.inputs, ty2021.available_forms)

    def test_simple_1040(self):
        solved = self.solver.solve(['1040'])
        solution = self.solver.solution()

        self.assertTrue(solved)

        self.assertIn('1040', solution)
        self.assertIn('w-2:0', solution)
