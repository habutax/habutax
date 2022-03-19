import unittest

from ..test_form import FormTestCase

import habutax.forms.ty2021 as ty2021

class Form1040S1TestCase0(FormTestCase):
    def setUp(self):
        values = {
            '1099-g:0.box_2': 329.09,
            '1099-g:1.box_2': 108.14,
            '1098:0.box_4': 102.33,
            '1099-int:0.box_2': 53.98,
            '8889:spouse.hsa_deduction': 7200.00,
        }
        self.fixture_setup(ty2021.available_forms, input_fixture='tests/ty2021/fixtures/f1040_s1_0.habutax', values=values)

    def test_1040_s1(self):
        solution = self.assertSolve(['1040_s1'], field_names=['1040_s1.10', '1040_s1.26'])

        self.assertIn('1040_s1', solution)

        self.assertDollarsEqual(solution, '1040_s1.1', 437.23)
        self.assertDollarsEqual(solution, '1040_s1.2a', 0.00)
        self.assertStringFieldEqual(solution, '1040_s1.2b', '')
        self.assertDollarsEqual(solution, '1040_s1.7', 0.00)
        self.assertDollarsEqual(solution, '1040_s1.8z', 102.33)
        self.assertStringFieldEqual(solution, '1040_s1.8z_type', "Refund of overpaid mortgage interest")
        self.assertDollarsEqual(solution, '1040_s1.10', 539.56)
        self.assertDollarsEqual(solution, '1040_s1.11', 0.00)
        self.assertDollarsEqual(solution, '1040_s1.13', 7200.00)
        self.assertDollarsEqual(solution, '1040_s1.18', 53.98)
        self.assertDollarsEqual(solution, '1040_s1.19a', 4983.2)
        self.assertStringFieldEqual(solution, '1040_s1.19b', '123456789')
        self.assertStringFieldEqual(solution, '1040_s1.19c', '04/01/2011')
        self.assertDollarsEqual(solution, '1040_s1.24z', 123.45)
        self.assertStringFieldEqual(solution, '1040_s1.24z_type', 'something')
        self.assertDollarsEqual(solution, '1040_s1.25', 123.45)
        self.assertDollarsEqual(solution, '1040_s1.26', 12360.63)

class Form1040S1TestCase1(FormTestCase):
    def setUp(self):
        values = {
        }
        self.fixture_setup(ty2021.available_forms, input_fixture='tests/ty2021/fixtures/f1040_s1_1.habutax')

    def test_1040_s1(self):
        solution = self.assertSolve(['1040_s1'], field_names=['1040_s1.10', '1040_s1.26'])

        self.assertIn('1040_s1', solution)

        self.assertDollarsEqual(solution, '1040_s1.1', 0.00)
        self.assertDollarsEqual(solution, '1040_s1.2a', 1245.46)
        self.assertStringFieldEqual(solution, '1040_s1.2b', '12/10/2018')
        self.assertDollarsEqual(solution, '1040_s1.7', 943.00)
        self.assertDollarsEqual(solution, '1040_s1.10', 2188.46)
        self.assertDollarsEqual(solution, '1040_s1.11', 234.50)
        self.assertDollarsEqual(solution, '1040_s1.13', 0.0)
        self.assertDollarsEqual(solution, '1040_s1.24z', 0.0)
        self.assertStringFieldEqual(solution, '1040_s1.24z_type', '')
        self.assertDollarsEqual(solution, '1040_s1.25', 0.0)
        self.assertDollarsEqual(solution, '1040_s1.26', 234.50)

class Form1040S1TestCase1_no_hsa(FormTestCase):
    def setUp(self):
        inputs = {
            '1040.filing_status': 'MarriedFilingJointly',
            '1040_s1.hsa_contribution_you': 'no',
            '1040_s1.hsa_contribution_spouse': 'no',
        }
        self.fixture_setup(ty2021.available_forms, input_fixture='tests/ty2021/fixtures/f1040_s1_1.habutax', inputs=inputs)

    def test_1040_s1(self):
        solution = self.assertSolve(['1040_s1'], field_names=['1040_s1.26'])
        self.assertDollarsEqual(solution, '1040_s1.13', 0.0)

class Form1040S1TestCase1_you_hsa(FormTestCase):
    def setUp(self):
        inputs = {
            '1040.filing_status': 'MarriedFilingJointly',
            '1040_s1.hsa_contribution_you': 'yes',
            '1040_s1.hsa_contribution_spouse': 'no',
        }
        values = {
            '8889:you.hsa_deduction': 198.30,
        }
        self.fixture_setup(ty2021.available_forms, input_fixture='tests/ty2021/fixtures/f1040_s1_1.habutax', inputs=inputs, values=values)

    def test_1040_s1(self):
        solution = self.assertSolve(['1040_s1'], field_names=['1040_s1.26'])
        self.assertDollarsEqual(solution, '1040_s1.13', 198.30)

class Form1040S1TestCase1_spouse_hsa(FormTestCase):
    def setUp(self):
        inputs = {
            '1040.filing_status': 'MarriedFilingJointly',
            '1040_s1.hsa_contribution_you': 'no',
            '1040_s1.hsa_contribution_spouse': 'yes',
        }
        values = {
            '8889:spouse.hsa_deduction': 1250.00,
        }
        self.fixture_setup(ty2021.available_forms, input_fixture='tests/ty2021/fixtures/f1040_s1_1.habutax', inputs=inputs, values=values)

    def test_1040_s1(self):
        solution = self.assertSolve(['1040_s1'], field_names=['1040_s1.26'])
        self.assertDollarsEqual(solution, '1040_s1.13', 1250.00)

class Form1040S1TestCase1_both_hsa(FormTestCase):
    def setUp(self):
        inputs = {
            '1040.filing_status': 'MarriedFilingJointly',
            '1040_s1.hsa_contribution_you': 'yes',
            '1040_s1.hsa_contribution_spouse': 'yes',
        }
        values = {
            '8889:spouse.hsa_deduction': 1250.00,
            '8889:you.hsa_deduction': 3892.00,
        }
        self.fixture_setup(ty2021.available_forms, input_fixture='tests/ty2021/fixtures/f1040_s1_1.habutax', inputs=inputs, values=values)

    def test_1040_s1(self):
        solution = self.assertSolve(['1040_s1'], field_names=['1040_s1.26'])
        self.assertDollarsEqual(solution, '1040_s1.13', 5142.00)
