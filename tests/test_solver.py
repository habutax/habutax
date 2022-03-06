import unittest
from configparser import ConfigParser

from . import context

from habutax.inputs import *
from habutax.fields import *
from habutax.form import *
from habutax.solver import Solver, DependencyTracker, sort_keys

class TestForm(Form):
    form_name = "test"
    tax_year = 1970

    def __init__(self, **kwargs):
        test_inputs = [
            IntegerInput('bar', description="I don't know"),
        ]
        test_fields = [
            IntegerField('foo', lambda s, i, v: i['bar']),
            IntegerField('something', lambda s, i, v: i['bar']),
            IntegerField('else', lambda s, i, v: v['something'] - i['bar']),
        ]
        super().__init__(__class__, test_inputs, test_fields, [], **kwargs)

class DependencyTrackerTestCase(unittest.TestCase):
    def setUp(self):
        self.form = TestForm()
        self.dep = DependencyTracker()

    def test_add_unmet(self):
        self.dep.add_unmet('test.bar', self.form.required_fields()[0])

        self.assertTrue(self.dep.has_unmet())
        self.assertFalse(self.dep.has_met())

        unmet_dependencies = self.dep.unmet_dependencies()
        self.assertEqual(len(unmet_dependencies), 1)
        self.assertEqual(unmet_dependencies[0], 'test.bar')

        unmet_dependents = self.dep.unmet_dependents('test.bar')
        self.assertEqual(len(unmet_dependents), 1)
        self.assertEqual(unmet_dependents[0].name(), 'test.foo')

        self.dep.add_unmet('test.bar', self.form.required_fields()[1])
        self.dep.add_unmet('test.bar', self.form.required_fields()[2])

        self.assertTrue(self.dep.has_unmet())
        self.assertFalse(self.dep.has_met())

        unmet_dependencies = self.dep.unmet_dependencies()
        self.assertEqual(len(unmet_dependencies), 1)
        self.assertEqual(unmet_dependencies[0], 'test.bar')

        unmet_dependents = self.dep.unmet_dependents('test.bar')
        self.assertEqual(len(unmet_dependents), 3)
        unmet_dependent_names = [ud.name() for ud in unmet_dependents]
        self.assertIn('test.foo', unmet_dependent_names)
        self.assertIn('test.something', unmet_dependent_names)
        self.assertIn('test.else', unmet_dependent_names)

    def test_meet(self):
        self.dep.add_unmet('test.bar', self.form.required_fields()[0])
        self.dep.add_unmet('test.bar', self.form.required_fields()[1])
        self.dep.add_unmet('test.bar', self.form.required_fields()[2])

        self.assertTrue(self.dep.has_unmet())
        self.assertFalse(self.dep.has_met())

        self.dep.meet('test.bar')

        self.assertFalse(self.dep.has_unmet())
        self.assertTrue(self.dep.has_met())

    def test_met_dependents(self):
        self.dep.add_unmet('test.bar', self.form.required_fields()[0])
        self.dep.add_unmet('test.bar', self.form.required_fields()[1])
        self.dep.add_unmet('test.bar', self.form.required_fields()[2])

        self.assertEqual(len(list(self.dep.met_dependents())), 0)

        self.dep.meet('test.bar')

        self.assertFalse(self.dep.has_unmet())
        self.assertTrue(self.dep.has_met())

        met_dependent_names = [f.name() for f in self.dep.met_dependents()]
        self.assertEqual(len(met_dependent_names), 3)

        self.assertIn('test.foo', met_dependent_names)
        self.assertIn('test.something', met_dependent_names)
        self.assertIn('test.else', met_dependent_names)

        self.assertFalse(self.dep.has_unmet())
        self.assertFalse(self.dep.has_met())

class SortOrderTestCase(unittest.TestCase):
    def test_sort_keys_same_form(self):
        original = [
            '1040.10',
            '1040.829',
            '1040.1a',
            '1040.8a8',
            '1040.1',
        ]
        expected = [
            '1040.1',
            '1040.1a',
            '1040.8a8',
            '1040.10',
            '1040.829',
        ]
        self.assertListEqual(sorted(original, key=sort_keys), expected)

    def test_sort_keys_no_form(self):
        original = [
            '2',
            '5_wkst_to_do_thing_10',
            '20',
            '5_wkst_to_do_thing_1',
            '1a',
            '5_wkst_to_do_thing_2',
            '1',
            '5_wkst_to_do_thing_9a',
            '1c',
            '5_wkst_to_do_thing_90',
        ]
        expected = [
            '1',
            '1a',
            '1c',
            '2',
            '5_wkst_to_do_thing_1',
            '5_wkst_to_do_thing_2',
            '5_wkst_to_do_thing_9a',
            '5_wkst_to_do_thing_10',
            '5_wkst_to_do_thing_90',
            '20',
        ]
        self.assertListEqual(expected, sorted(original, key=sort_keys))

    def test_sort_keys_different_forms(self):
        original = [
            '1040_sa.10',
            '8995.5b',
            '1040_sb.829',
            '1040_s8812.1a',
            'w-2.box_1',
            '1040.first_name',
            '8959.5b',
        ]
        expected = [
            '1040.first_name',
            '1040_s8812.1a',
            '1040_sa.10',
            '1040_sb.829',
            '8959.5b',
            '8995.5b',
            'w-2.box_1',
        ]
        self.assertListEqual(sorted(original, key=sort_keys), expected)

    def test_sort_keys_mixed_form_presence(self):
        original = [
            '1040_sb.829',
            '10',
            '5b',
            '1040.first_name',
            '51',
            '1040_s8812.1a',
            'box_1',
            '5a',
            '8995.5b',
        ]
        expected = [
            '5a',
            '5b',
            '10',
            '51',
            'box_1',
            '1040.first_name',
            '1040_s8812.1a',
            '1040_sb.829',
            '8995.5b',
        ]
        self.assertListEqual(sorted(original, key=sort_keys), expected)

    def test_sort_keys_mixed_types(self):
        test_form = TestForm()
        original = [
            "test.9a",
            test_form.inputs()[0],
            "z.foobar",
            test_form.fields()[0],
            "test.c",
            test_form.fields()[1],
            "test.z00",
            "000.1",
            test_form.fields()[2],
        ]
        expected = [
            "000.1",
            "test.9a",
            test_form.inputs()[0], # test.bar
            "test.c",
            test_form.fields()[2], # test.else
            test_form.fields()[0], # test.foo
            test_form.fields()[1], # test.something
            "test.z00",
            "z.foobar",
        ]
        self.assertListEqual(sorted(original, key=sort_keys), expected)

class SolverTestCase(unittest.TestCase):
    def setUp(self):
        self.config = ConfigParser()
        self.inputs = InputStore(self.config)
        self.solver = Solver(self.inputs, [TestForm])

    def test_basic_form(self):
        self.config['test'] = {'bar': '5'}
        solved = self.solver.solve(['test'])

        self.assertTrue(solved)
        solution = self.solver.solution()
        self.assertIn('test', solution)

        for field, value in (('foo', '5'), ('something', '5'), ('else', '0')):
            self.assertIn(field, solution['test'])
            self.assertEqual(solution['test'][field], value)

    def test_basic_form_missing_input(self):
        solved = self.solver.solve(['test'])

        self.assertFalse(solved)
        solution = self.solver.solution()
        self.assertNotIn('test', solution)

        self.assertEqual(len(self.solver.unimplemented_fields()), 0)

        dep = self.solver.unmet_input_dependencies()
        self.assertEqual(len(dep), 1)
        self.assertIn('test.bar', dep)
        self.assertEqual(len(dep['test.bar']), 2)
        self.assertIn('test.foo', dep['test.bar'])
        self.assertIn('test.something', dep['test.bar'])

        self.assertEqual(len(self.solver.unmet_field_dependencies()), 1)
