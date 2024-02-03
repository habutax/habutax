from ..test_form import FormTestCase

import habutax.forms.ty2022 as ty2022


class Form1040S3TestCase(FormTestCase):
    def setUp(self):
        values = {
            '1040.11': 83450.73,
            '1099-int:0.box_6': 329.09,
            '1099-div:0.box_7': 108.14,
        }
        self.fixture_setup(ty2022.available_forms, input_fixture='tests/ty2022/fixtures/f1040_s3_0.habutax', values=values)

    def test_1040_s3(self):
        solution = self.assertSolve(['1040_s3'], field_names=['1040_s3.8'])
        self.assertIn('1040_s3', solution)

        self.assertDollarsEqual(solution, '1040_s3.1', 437.23)
        self.assertDollarsEqual(solution, '1040_s3.8', 437.23)


class Form1040S3TestCaseTooManyForeignTaxesMFJ(FormTestCase):
    def setUp(self):
        values = {
            '1040.11': 83450.73,
            '1099-int:0.box_6': 329.09,
            '1099-div:0.box_7': 423.09,
        }
        self.fixture_setup(ty2022.available_forms, input_fixture='tests/ty2022/fixtures/f1040_s3_0.habutax', values=values)

    def test_1040_s3(self):
        solution = self.assertUnimplementedSolution(['1040_s3'], field_names=['1040_s3.8'])


class Form1040S3TestCaseTooManyForeignTaxesSingle(FormTestCase):
    def setUp(self):
        inputs = {
            '1040.filing_status': 'Single'
        }
        values = {
            '1040.11': 83450.73,
            '1099-int:0.box_6': 329.09,
            '1099-div:0.box_7': 123.09,
        }
        self.fixture_setup(ty2022.available_forms, input_fixture='tests/ty2022/fixtures/f1040_s3_0.habutax', inputs=inputs, values=values)

    def test_1040_s3(self):
        solution = self.assertUnimplementedSolution(['1040_s3'], field_names=['1040_s3.8'])
