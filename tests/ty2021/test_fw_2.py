import unittest

from ..test_form import FormTestCase

import habutax.forms.ty2021 as ty2021
from habutax import enum

class FormW2TestCase(FormTestCase):
    def setUp(self):
        self.fixture_setup(ty2021.available_forms, input_fixture='tests/ty2021/fixtures/fw_2_0.habutax')

    def test_simple_w2(self):
        solution = self.assertSolve(['w-2:0'])

        self.assertIn('w-2:0', solution)

        self.assertEnumFieldEqual(solution, 'w-2:0.belongs_to', enum.taxpayer_or_spouse, enum.taxpayer_or_spouse.spouse)
        self.assertStringFieldEqual(solution, 'w-2:0.box_c', "Fake County Public School System")
        self.assertStringFieldEqual(solution, 'w-2:0.box_e', "Suzy Llama")
        self.assertDollarsEqual(solution, 'w-2:0.box_1', 12595.47)
        self.assertDollarsEqual(solution, 'w-2:0.box_2', 905.24)
        self.assertDollarsEqual(solution, 'w-2:0.box_3', 17763.74)
        self.assertDollarsEqual(solution, 'w-2:0.box_4', 1101.35)
        self.assertDollarsEqual(solution, 'w-2:0.box_5', 17763.74)
        self.assertDollarsEqual(solution, 'w-2:0.box_6', 257.57)
        self.assertDollarsEqual(solution, 'w-2:0.box_7', 0.00)
        self.assertDollarsEqual(solution, 'w-2:0.box_8', 0.00)
        self.assertDollarsEqual(solution, 'w-2:0.box_10', 0.00)
        self.assertDollarsEqual(solution, 'w-2:0.box_11', 0.00)
        self.assertBooleanFieldEqual(solution, 'w-2:0.box_13_retirement', True)
        self.assertBooleanFieldEqual(solution, 'w-2:0.box_13_sick_day', False)
        self.assertBooleanFieldEqual(solution, 'w-2:0.box_13_statutory', False)
        self.assertEnumFieldEqual(solution, 'w-2:0.box_15', enum.us_states, enum.us_states.SC)
        self.assertDollarsEqual(solution, 'w-2:0.box_16', 12595.47)
        self.assertDollarsEqual(solution, 'w-2:0.box_17', 455.00)
        self.assertDollarsEqual(solution, 'w-2:0.box_18', 0.00)
        self.assertDollarsEqual(solution, 'w-2:0.box_19', 0.00)
