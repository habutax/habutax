import configparser
import unittest

from . import context

from habutax.inputs import InputStore
from habutax.fields import *
from habutax.solver import Solver

class FormTestCase(unittest.TestCase):
    def prompt_input(self, missing, needed_by):
        if missing.name() in self.input_dict:
            return self.input_dict[missing.name()]
        return None

    def fixture_setup(self, available_forms, input_fixture=None, inputs={}, values={}):
        if input_fixture is None:
            self.inputs = InputStore(configparser.ConfigParser())
        else:
            self.inputs = InputStore(input_fixture)

        if len(inputs) > 0:
            self.solver = Solver(self.inputs, available_forms, prompt=self.prompt_input)
            self.input_dict = inputs
        else:
            self.solver = Solver(self.inputs, available_forms)

        for k, v in values.items():
            self.solver._v[k] = v

    def assertSolve(self, form_names):
        solved = self.solver.solve(form_names)
        solution = self.solver.solution()

        self.assertTrue(solved)

        return solution

    def assertFieldEqual(self, solution, field, expected, fieldtype=StringField):
        f = fieldtype('assertFieldEqual', lambda s, i, v: None)
        form, field = field.split('.')
        calculated = f.from_string(solution[form][field])
        self.assertEqual(calculated, expected)

    def assertStringFieldEqual(self, solution, field, expected):
        self.assertFieldEqual(solution, field, expected, fieldtype=StringField)

    def assertBooleanFieldEqual(self, solution, field, expected):
        self.assertFieldEqual(solution, field, expected, fieldtype=BooleanField)

    def assertIntegerFieldEqual(self, solution, field, expected):
        self.assertFieldEqual(solution, field, expected, fieldtype=IntegerField)

    def assertFloatFieldEqual(self, solution, field, expected, places=2):
        f = FloatField('assertFloatFieldEqual', lambda s, i, v: None, places=places)
        form, field = field.split('.')
        calculated = f.from_string(solution[form][field])
        self.assertAlmostEqual(calculated, expected, places=places)

    def assertDollarsEqual(self, solution, field, expected):
        self.assertFloatFieldEqual(solution, field, expected, places=2)

    def assertEnumFieldEqual(self, solution, field, enum, expected):
        f = EnumField('assertEnumFieldEqual', enum, lambda s, i, v: None)
        form, field = field.split('.')
        calculated = f.from_string(solution[form][field])
        self.assertEqual(calculated, expected)
