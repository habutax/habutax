import configparser
import unittest

from . import context

from habutax.inputs import InputStore
from habutax.fields import *
from habutax.solver import Solver

class FormTestCase(unittest.TestCase):
    def prompt_input(self, missing, needed_by):
        if missing.name() in self.input_dict:
            return (self.input_dict[missing.name()], True)
        return (None, False)

    def fixture_setup(self, available_forms, input_fixture=None, inputs={}, values={}):
        """Helper for setting up a test fixture. Values specified in 'inputs'
        override the values in 'input_fixture' if the same are specified in both.
        """
        if input_fixture is None:
            self.inputs = InputStore(configparser.ConfigParser())
        else:
            self.inputs = InputStore(input_fixture)

        if len(inputs) > 0:
            # Remove same-named inputs which exist in the input file if they
            # also exist in the input dictionary
            for input_name in inputs.keys():
                if input_name in self.inputs:
                    del self.inputs[input_name]
            self.solver = Solver(self.inputs, available_forms, prompt=self.prompt_input)
            self.input_dict = inputs
        else:
            self.solver = Solver(self.inputs, available_forms)

        for k, v in values.items():
            self.solver._v[k] = v

            # Create bogus field definitions and inject them into the solver so
            # that it can use them when writing the solution out
            form_name, field_name = k.split(".")
            if isinstance(v, str):
                self.solver._field_map[k] = StringField(field_name, lambda s, i, v: None)
            elif isinstance(v, bool):
                self.solver._field_map[k] = BooleanField(field_name, lambda s, i, v: None)
            elif isinstance(v, int):
                self.solver._field_map[k] = IntegerField(field_name, lambda s, i, v: None)
            elif isinstance(v, float):
                self.solver._field_map[k] = FloatField(field_name, lambda s, i, v: None)
            else:
                raise RuntimeError("Form tests can't currently handle setting Enum fields")
            class FakeForm(object):
                def __init__(self, form_name):
                    self.form_name = form_name
                def name(self):
                    return self.form_name
            self.solver._field_map[k].__form_init__(FakeForm(form_name))

    def assertSolve(self, form_names, field_names=[]):
        solved = self.solver.solve(form_names, field_names=field_names)
        solution = self.solver.solution()

        self.assertEqual(self.solver.unimplemented_fields(), [])
        self.assertEqual(self.solver.unmet_input_dependencies(), {})
        self.assertEqual(self.solver.unmet_field_dependencies(), {})
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
