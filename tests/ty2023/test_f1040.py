from ..test_form import FormTestCase

import habutax.forms.ty2023 as ty2023


class Form1040SimpleTestCase(FormTestCase):
    def setUp(self):
        self.fixture_setup(ty2023.available_forms, input_fixture='tests/ty2023/fixtures/f1040_one_w2.habutax')

    def test_simple_1040(self):
        solution = self.assertSolve(['1040'])

        self.assertIn('1040', solution)
        self.assertIn('w-2:0', solution)

        self.assertDollarsEqual(solution, '1040.1a', 100000) # W-2 income
        self.assertDollarsEqual(solution, '1040.11', 100000) # AGI
        self.assertDollarsEqual(solution, '1040.12', 13850)  # standard deduction
        self.assertDollarsEqual(solution, '1040.15', 100000 - 13850) # taxable income
        self.assertDollarsEqual(solution, '1040.16', 14266) # tax
        self.assertDollarsEqual(solution, '1040.24', 14266) # total tax
        self.assertDollarsEqual(solution, '1040.25a', 16551.90) # W-2 withholding
        self.assertDollarsEqual(solution, '1040.25d', 16551.90) # total withholding
        self.assertDollarsEqual(solution, '1040.33', 16551.90) # total payments
        self.assertDollarsEqual(solution, '1040.34', 2285.90) # overpayment
        self.assertDollarsEqual(solution, '1040.35a', 2285.90) # refund
        self.assertDollarsEqual(solution, '1040.37', 0) # amount you owe
        self.assertDollarsEqual(solution, '1040.38', 0) # tax penalty
