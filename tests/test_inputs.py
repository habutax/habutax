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

        for value in ['John Smith ', ' ', '839']:
            self.assertTrue(str_input.valid(value))
            self.assertIsInstance(str_input.value(value), str)
            self.assertEqual(str_input.value(value), value.strip())

    def test_boolean_input(self):
        bool_input = BooleanInput('snake', description="Are you a snake?")
        bool_input.__form_init__(self.form)

        for invalid in ['nope', 'nah', 'maybe', 'tomorrow', 'definitely', '', '2']:
            self.assertFalse(bool_input.valid(invalid))

        for yes in ['yes', 'Yes', 'true', 'True', 'TRUE', '1', 'ON', 'on']:
            self.assertTrue(bool_input.valid(yes))
            self.assertIsInstance(bool_input.value(yes), bool)
            self.assertEqual(bool_input.value(yes), True)

        for no in ['no', 'NO', 'false', 'FALSE', 'False', '0', 'Off', 'OFF']:
            self.assertTrue(bool_input.valid(no))
            self.assertIsInstance(bool_input.value(no), bool)
            self.assertEqual(bool_input.value(no), False)

    def test_integer_input(self):
        int_input = IntegerInput('snakes', description="How many snakes are on your plane?")
        int_input.__form_init__(self.form)

        for invalid in ['not on my plane', '-', '+', '$', '0.4']:
            self.assertFalse(int_input.valid(invalid))

        for valid in ['-1', '3', '    51', '92838927359872']:
            self.assertTrue(int_input.valid(valid))
            self.assertIsInstance(int_input.value(valid), int)
            self.assertEqual(int_input.value(valid), int(valid.strip()))

        self.assertTrue(int_input.valid(''))
        self.assertIsInstance(int_input.value(''), int)
        self.assertEqual(int_input.value(''), 0)

    def test_float_input(self):
        float_input = FloatInput('fractional_snakes', description="How many snakes are on your plane?")
        float_input.__form_init__(self.form)

        for invalid in ['not on my plane', '-', '+', '$', '9 4', '84/']:
            self.assertFalse(float_input.valid(invalid))

        for valid in ['-0.14', '9\t', '    51', '92838927359872', '0.83858']:
            self.assertTrue(float_input.valid(valid))
            self.assertIsInstance(float_input.value(valid), float)
            self.assertAlmostEqual(float_input.value(valid), float(valid.strip()), places=5)

        self.assertTrue(float_input.valid(''))
        self.assertIsInstance(float_input.value(''), float)
        self.assertEqual(float_input.value(''), 0.0)

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

        for invalid in ['', 'green', 'GREEN', 'sky blue']:
            self.assertFalse(enum_color.valid(invalid))

        for valid, result in {'Red': colors.Red, 'Green': colors.Green, 'Blue': colors.Blue}.items():
            self.assertTrue(enum_color.valid(valid))
            self.assertIsInstance(enum_color.value(valid), enum.StringyEnum)
            self.assertEqual(enum_color.value(valid), result)

    def test_regex_input(self):
        regex_name = RegexInput('name', '^(Bob|[Rr]obert) Smith$', description="What is your name?")
        regex_name.__form_init__(self.form)

        for invalid in ['Bobert Smith', 'Bob', 'me']:
            self.assertFalse(regex_name.valid(invalid))

        for valid in ['Bob Smith', 'Robert Smith', 'robert Smith']:
            self.assertTrue(regex_name.valid(valid))
            self.assertIsInstance(regex_name.value(valid), str)
            self.assertEqual(regex_name.value(valid), valid)

        regex_routing = RegexInput('routing_number', '^(0[1-9]|1[0-2]|2[1-9]|3[0-2])[0-9]{7}$', description="What is your routing number?")
        regex_routing.__form_init__(self.form)

        for invalid in ['00', '000000000', '158374958']:
            self.assertFalse(regex_routing.valid(invalid))

        for valid in ['012345678', '310000000', '258377691']:
            self.assertTrue(regex_routing.valid(valid))
            self.assertEqual(regex_routing.value(valid), str(valid))

    def test_ssn_input(self):
        ssn = SSNInput('taxpayer_ssn', description="Your social security number")
        ssn.__form_init__(self.form)

        for invalid in ['1234567890', '12345678', 'hello?']:
            self.assertFalse(ssn.valid(invalid))

        for valid, result in {'000-00-0000': '000000000', '123456789': '123456789'}.items():
            self.assertTrue(ssn.valid(valid))
            self.assertEqual(ssn.value(valid), result)
