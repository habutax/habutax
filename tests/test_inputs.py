import configparser
import unittest

from . import context

import habutax.enum as enum
from habutax.inputs import *
from habutax.form import Form

class InputTestForm(Form):
    form_name = "0000"
    tax_year = 1970

    def __init__(self, **kwargs):
        super().__init__(__class__, [], [], [], **kwargs)

class InputTestCase(unittest.TestCase):
    def setUp(self):
        self.config = configparser.ConfigParser()
        self.form = InputTestForm()

    def tearDown(self):
        del self.config
        del self.form

    def test_string_input(self):
        str_input = StringInput('name', description="What is your name?")
        str_input.__form_init__(self.form)

        self.assertFalse(str_input.provided(self.config))
        self.assertFalse(str_input.valid(self.config))

        self.config['0000'] = {'wrong_name': 'John Smith'}
        self.assertFalse(str_input.provided(self.config))
        self.assertFalse(str_input.valid(self.config))

        self.config['0000'] = {'name': 'John Smith'}
        self.assertTrue(str_input.provided(self.config))
        self.assertTrue(str_input.valid(self.config))
        self.assertIsInstance(str_input.value(self.config), str)
        self.assertEqual(str_input.value(self.config), 'John Smith')

        self.config['0000'] = {'name': 839}
        self.assertTrue(str_input.provided(self.config))
        self.assertTrue(str_input.valid(self.config))
        self.assertIsInstance(str_input.value(self.config), str)
        self.assertEqual(str_input.value(self.config), '839')

    def test_boolean_input(self):
        bool_input = BooleanInput('snake', description="Are you a snake?")
        bool_input.__form_init__(self.form)

        self.assertFalse(bool_input.provided(self.config))
        self.assertFalse(bool_input.valid(self.config))

        self.config['0000'] = {'wrong_name': 'John Smith'}
        self.assertFalse(bool_input.provided(self.config))
        self.assertFalse(bool_input.valid(self.config))

        for invalid in ['nope', 'nah', 'maybe', 'tomorrow', 'definitely', '', '2']:
            self.config['0000'] = {'snake': invalid}
            self.assertTrue(bool_input.provided(self.config))
            self.assertFalse(bool_input.valid(self.config))

        for yes in ['yes', 'Yes', 'true', 'True', 'TRUE', '1']:
            self.config['0000'] = {'snake': yes}
            self.assertTrue(bool_input.provided(self.config))
            self.assertTrue(bool_input.valid(self.config))
            self.assertIsInstance(bool_input.value(self.config), bool)
            self.assertEqual(bool_input.value(self.config), True)

        for no in ['no', 'NO', 'false', 'FALSE', 'False', '0']:
            self.config['0000'] = {'snake': no}
            self.assertTrue(bool_input.provided(self.config))
            self.assertTrue(bool_input.valid(self.config))
            self.assertIsInstance(bool_input.value(self.config), bool)
            self.assertEqual(bool_input.value(self.config), False)

    def test_integer_input(self):
        int_input = IntegerInput('snakes', description="How many snakes are on your plane?")
        int_input.__form_init__(self.form)

        self.assertFalse(int_input.provided(self.config))
        self.assertFalse(int_input.valid(self.config))

        self.config['0000'] = {'wrong_name': 'John Smith'}
        self.assertFalse(int_input.provided(self.config))
        self.assertFalse(int_input.valid(self.config))

        for invalid in ['not on my plane', '-', '+', '$', '0.4']:
            self.config['0000'] = {'snakes': invalid}
            self.assertTrue(int_input.provided(self.config))
            self.assertFalse(int_input.valid(self.config))

        for valid in ['-1', '3', '    51', '92838927359872']:
            self.config['0000'] = {'snakes': valid}
            self.assertTrue(int_input.provided(self.config))
            self.assertTrue(int_input.valid(self.config))
            self.assertIsInstance(int_input.value(self.config), int)
            self.assertEqual(int_input.value(self.config), int(valid.strip()))

        self.config['0000'] = {'snakes': ''}
        self.assertTrue(int_input.provided(self.config))
        self.assertTrue(int_input.valid(self.config))
        self.assertIsInstance(int_input.value(self.config), int)
        self.assertEqual(int_input.value(self.config), 0)

    def test_float_input(self):
        float_input = FloatInput('fractional_snakes', description="How many snakes are on your plane?")
        float_input.__form_init__(self.form)

        self.assertFalse(float_input.provided(self.config))
        self.assertFalse(float_input.valid(self.config))

        self.config['0000'] = {'wrong_name': 'John Smith'}
        self.assertFalse(float_input.provided(self.config))
        self.assertFalse(float_input.valid(self.config))

        for invalid in ['not on my plane', '-', '+', '$', '9 4', '84/']:
            self.config['0000'] = {'fractional_snakes': invalid}
            self.assertTrue(float_input.provided(self.config))
            self.assertFalse(float_input.valid(self.config))

        for valid in ['-0.14', '9\t', '    51', '92838927359872', '0.83858']:
            self.config['0000'] = {'fractional_snakes': valid}
            self.assertTrue(float_input.provided(self.config))
            self.assertTrue(float_input.valid(self.config))
            self.assertIsInstance(float_input.value(self.config), float)
            self.assertAlmostEqual(float_input.value(self.config), float(valid.strip()), places=5)

        self.config['0000'] = {'fractional_snakes': ''}
        self.assertTrue(float_input.provided(self.config))
        self.assertTrue(float_input.valid(self.config))
        self.assertIsInstance(float_input.value(self.config), float)
        self.assertEqual(float_input.value(self.config), 0.0)

    def test_enum_input(self):
        colors = enum.make('Colors of the rainbow', {
            'Red': 'the color you bleed',
            'Orange': 'tasty fruit',
            'Yellow': 'like the sun',
            'Green': 'leaves in the summer',
            'Blue': 'cool ocean breeze',
            'Indigo': 'purple',
            'Violet': 'also purple',
        })
        enum_color = EnumInput('favorite_color', colors, description="What is your favorite color?")
        enum_color.__form_init__(self.form)

        self.assertFalse(enum_color.provided(self.config))
        self.assertFalse(enum_color.valid(self.config))

        self.config['0000'] = {'wrong_color': 'azul'}
        self.assertFalse(enum_color.provided(self.config))
        self.assertFalse(enum_color.valid(self.config))

        for invalid in ['', 'green', 'GREEN', 'sky blue']:
            self.config['0000'] = {'favorite_color': invalid}
            self.assertTrue(enum_color.provided(self.config))
            self.assertFalse(enum_color.valid(self.config))

        for valid, result in {'Red': colors.Red, 'Green': colors.Green, 'Blue': colors.Blue}.items():
            self.config['0000'] = {'favorite_color': valid}
            self.assertTrue(enum_color.provided(self.config))
            self.assertTrue(enum_color.valid(self.config))
            self.assertIsInstance(enum_color.value(self.config), enum.StringyEnum)
            self.assertEqual(enum_color.value(self.config), result)

    def test_regex_input(self):
        regex_name = RegexInput('name', '^(Bob|[Rr]obert) Smith$', description="What is your name?")
        regex_name.__form_init__(self.form)

        self.assertFalse(regex_name.provided(self.config))
        self.assertFalse(regex_name.valid(self.config))

        self.config['0000'] = {'wrong_name': 'Bob Smith'}
        self.assertFalse(regex_name.provided(self.config))
        self.assertFalse(regex_name.valid(self.config))

        for invalid in ['Bobert Smith', 'Bob', 'me']:
            self.config['0000'] = {'name': invalid}
            self.assertTrue(regex_name.provided(self.config))
            self.assertFalse(regex_name.valid(self.config))

        for valid in ['Bob Smith', 'Robert Smith', 'robert Smith']:
            self.config['0000'] = {'name': valid}
            self.assertTrue(regex_name.provided(self.config))
            self.assertTrue(regex_name.valid(self.config))
            self.assertIsInstance(regex_name.value(self.config), str)
            self.assertEqual(regex_name.value(self.config), valid)

        regex_routing = RegexInput('routing_number', '^(0[1-9]|1[0-2]|2[1-9]|3[0-2])[0-9]{7}$', description="What is your routing number?")
        regex_routing.__form_init__(self.form)

        self.assertFalse(regex_routing.provided(self.config))
        self.assertFalse(regex_routing.valid(self.config))

        for invalid in ['00', '000000000', 158374958]:
            self.config['0000'] = {'routing_number': invalid}
            self.assertTrue(regex_routing.provided(self.config))
            self.assertFalse(regex_routing.valid(self.config))

        for valid in ['012345678', '310000000', 258377691]:
            self.config['0000'] = {'routing_number': valid}
            self.assertTrue(regex_routing.provided(self.config))
            self.assertTrue(regex_routing.valid(self.config))
            self.assertEqual(regex_routing.value(self.config), str(valid))

    def test_ssn_input(self):
        ssn = SSNInput('taxpayer_ssn', description="Your social security number")
        ssn.__form_init__(self.form)

        self.assertFalse(ssn.provided(self.config))
        self.assertFalse(ssn.valid(self.config))

        for invalid in ['1234567890', '12345678', 'hello?']:
            self.config['0000'] = {'taxpayer_ssn': invalid}
            self.assertTrue(ssn.provided(self.config))
            self.assertFalse(ssn.valid(self.config))

        for valid, result in {'000-00-0000': '000000000', '123456789': '123456789'}.items():
            self.config['0000'] = {'taxpayer_ssn': valid}
            self.assertTrue(ssn.provided(self.config))
            self.assertTrue(ssn.valid(self.config))
            self.assertEqual(ssn.value(self.config), result)
