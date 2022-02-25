import unittest

from . import context

from habutax.inputs import *
from habutax.fields import *
from habutax.form import *
from habutax.solver import DependencyTracker

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
