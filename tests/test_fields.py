import configparser
import unittest

from . import context

import habutax.enum as enum
from habutax.fields import *
from habutax.form import Form

class FieldTestForm(Form):
    form_name = "0000"
    tax_year = 1970

    def __init__(self, **kwargs):
        super().__init__(__class__, [], [], [], **kwargs)

class FieldTestCase(unittest.TestCase):
    def setUp(self):
        self.config = configparser.ConfigParser()
        self.form = FieldTestForm()

    def tearDown(self):
        del self.config
        del self.form

    def test_not_implemented(self):
        f = IntegerField('favorite_number', lambda s, i, v: s.not_implemented() if i['favorite_number'] < 10 else i['favorite_number'])
        f.__form_init__(self.form)

        self.assertEqual(f.value({'favorite_number': 10}, {}), 10)
        with self.assertRaises(FieldNotImplemented):
            f.value({'favorite_number': 9}, {})

    def test_type_error(self):
        colors = enum.make('Colors of the rainbow', {
            'Red': 'the color you bleed',
            'Orange': 'tasty fruit',
            'Yellow': 'like the sun',
            'Green': 'leaves in the summer',
            'Blue': 'cool ocean breeze',
            'Indigo': 'purple',
            'Violet': 'also purple',
        })
        fields = [
            StringField('one', lambda s, i, v: False),
            BooleanField('two', lambda s, i, v: "hello"),
            IntegerField('three', lambda s, i, v: 400.14),
            FloatField('four', lambda s, i, v: 900),
            EnumField('five', colors, lambda s, i, v: "again?"),
        ]
        for f in fields:
            f.__form_init__(self.form)

            with self.assertRaises(TypeError):
                f.value({}, {})

    def test_string_field(self):
        f = StringField('name', lambda s, i, v: "your name is: " + i['name'])
        f.__form_init__(self.form)

        self.assertEqual(f.value({'name': 'Bob'}, {}), "your name is: Bob")

        for value in ['John Smith ', '', '839']:
            string = f.to_string(value)
            value2 = f.from_string(string)
            self.assertEqual(value, string)
            self.assertEqual(value, value2)

    def test_boolean_field(self):
        f = BooleanField('has_name', lambda s, i, v: len(i['name']) > 0)
        f.__form_init__(self.form)

        self.assertTrue(f.value({'name': 'Bob'}, {}))
        self.assertFalse(f.value({'name': ''}, {}))

        for value in [True, False]:
            string = f.to_string(value)
            value2 = f.from_string(string)
            self.assertEqual(value, value2)

    def test_integer_field(self):
        f = IntegerField('name_length', lambda s, i, v: len(i['name']))
        f.__form_init__(self.form)

        self.assertEqual(f.value({'name': 'Bob'}, {}), 3)
        self.assertEqual(f.value({'name': ''}, {}), 0)

        for value in [98317, 0, -8, 10000]:
            string = f.to_string(value)
            value2 = f.from_string(string)
            self.assertEqual(string, str(value))
            self.assertEqual(value, value2)

    def test_float_field(self):
        f = FloatField('bytwo', lambda s, i, v: i['number'] / 2.0, places=5)
        f.__form_init__(self.form)

        self.assertAlmostEqual(f.value({'number': 2}, {}), 1, places=10)
        self.assertAlmostEqual(f.value({'number': -515}, {}), -257.5, places=10)
        self.assertAlmostEqual(f.value({'number': 2.6666666666}, {}), 1.33333, places=10)

        for v, s, v2 in [(float(98317), "98317.00000", 98317),
                         (-0.0091, "-0.00910", -0.0091),
                         (-8.888899, "-8.88890", -8.8889),
                         (0.0001, "0.00010", 0.0001),
                         (10000, "10000.00000", 10000)]:
            string = f.to_string(v)
            value2 = f.from_string(string)
            self.assertEqual(string, s)
            self.assertAlmostEqual(v2, value2, places=10)

    def test_float_field_rounding(self):

        f = FloatField('bytwo', lambda s, i, v: i['number'] / 2.0, places=2)
        f.__form_init__(self.form)

        self.assertAlmostEqual(f.value({'number': 2}, {}), 1, places=5)
        self.assertAlmostEqual(f.value({'number': -515}, {}), -257.50, places=5)
        self.assertAlmostEqual(f.value({'number': 2.6666666666}, {}), 1.33, places=5)
        self.assertAlmostEqual(f.value({'number': 98.999999}, {}), 49.5, places=5)

        for v, s, v2 in [(float(98317), "98317.00", 98317),
                         (.238, "0.24", 0.24),
                         (-8.8888, "-8.89", -8.89),
                         (0.0001, "0.00", 0),
                         (10000, "10000.00", 10000),
                         (98.2, "98.20", 98.2),
                         (-0.0091, "-0.01", -0.01)]:
            string = f.to_string(v)
            value2 = f.from_string(string)
            self.assertEqual(string, s)
            self.assertAlmostEqual(v2, value2, places=10)
