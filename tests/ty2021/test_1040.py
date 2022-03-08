import unittest

from .. import context

import habutax.forms.ty2021 as ty2021
from habutax.inputs import InputStore
from habutax.solver import Solver

class Form1040SimpleTestCase(unittest.TestCase):
    def setUp(self):
        self.inputs = InputStore('tests/ty2021/fixtures/one_w2.habutax')
        self.solver = Solver(self.inputs, ty2021.available_forms)

    def assertDollarsEqual(self, solution, field, expected):
        form, field = field.split('.')
        calculated = float(solution[form][field])
        self.assertAlmostEqual(calculated, expected, places=2)

    def test_simple_1040(self):
        solved = self.solver.solve(['1040'])
        solution = self.solver.solution()

        self.assertTrue(solved)

        self.assertIn('1040', solution)
        self.assertIn('w-2:0', solution)

        self.assertDollarsEqual(solution, '1040.1', 100000)
        self.assertDollarsEqual(solution, '1040.12c', 12550 + 300)
        self.assertDollarsEqual(solution, '1040.15', 100000 - (12550 + 300))
        self.assertDollarsEqual(solution, '1040.16', 14943)
        self.assertDollarsEqual(solution, '1040.25a', 16551.9)
        self.assertDollarsEqual(solution, '1040.25d', 16551.9)
        self.assertDollarsEqual(solution, '1040.33', 16551.9)
        self.assertDollarsEqual(solution, '1040.34', 1608.9)
        self.assertDollarsEqual(solution, '1040.35a', 1608.9)
        self.assertDollarsEqual(solution, '1040.37', 0)
        self.assertDollarsEqual(solution, '1040.38', 0)
