import unittest

from ..test_form import FormTestCase

import habutax.forms.ty2021 as ty2021

class Form1040SimpleTestCase(FormTestCase):
    def setUp(self):
        self.fixture_setup(ty2021.available_forms, input_fixture='tests/ty2021/fixtures/f1040_one_w2.habutax')

    def test_simple_1040(self):
        solution = self.assertSolve(['1040'])

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
