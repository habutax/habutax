from enum import Enum, auto
import copy
import os
import re
import unittest

from . import context

class DocumentationTestCase(unittest.TestCase):
    def find_doc_code(self, documentation_filename, code_filename):

        escaped_code_filename = re.escape(code_filename)
        code_listing = re.compile(f'^example code: {escaped_code_filename}$')
        start = re.compile('^```python$')
        stop = re.compile('^```$')

        class State(Enum):
            SEARCHING = auto()
            CONFIRMING = auto()
            READING = auto()

        code = ""
        full_doc_filename = os.path.join(context.habutax_basedir, 'doc', documentation_filename)
        with open(full_doc_filename) as doc:
            state = State.SEARCHING
            for line in doc:
                if state == State.READING:
                    if stop.match(line):
                        self.assertTrue(len(code) > 0)
                        return code
                    else:
                        code += line
                elif state == State.CONFIRMING:
                    if start.match(line):
                        state = State.READING
                    else:
                        state = State.SEARCHING
                elif code_listing.match(line):
                    state = State.CONFIRMING

        self.assertTrue(False)

    def find_compile_doc_code(self, documentation_filename, code_filename):
        code = self.find_doc_code(documentation_filename, code_filename)
        return compile(code, f'doc/{documentation_filename} example code: {code_filename}', 'exec')

    def setUp(self):
        """Because the tests in this class exec() code examples, which causes
        pollution of the global space (via imports or definitions of classes,
        etc.), save as much of the current state of the globals as we can to
        restore it later"""
        self._saved_globals = {}
        self._keep_globals = set()

        for k, v in globals().items():
            try:
                self._saved_globals[k] = copy.deepcopy(globals()[k])
            except:
                self._keep_globals.add(k)

    def tearDown(self):
        """Restore global state as it was saved by setUp() as much as we can"""
        for k in list(globals().keys()):
            if k not in self._saved_globals and k not in self._keep_globals:
                del globals()[k]
            elif k in self._saved_globals:
                globals()[k] = self._saved_globals[k]

        del self._saved_globals
        del self._keep_globals

    def test_form0000_example(self):
        f0000 = self.find_compile_doc_code('adding_modifying_forms.md', 'f0000.py')

        # Defines class Form0000
        exec(f0000, globals())

        f0 = Form0000()
        self.assertEqual(f0.name(), "0000")

        self.assertEqual(len(f0.inputs()), 3)
        self.assertEqual(len(f0.required_fields()), 0)
        self.assertEqual(len(f0.fields()), 2)

        self.assertEqual(f0.inputs()[0].name(), "0000.base_tax")
        self.assertEqual(f0.fields()[1].name(), "0000.2")

        # Test with 'naughty' input
        naughty_inputs = {
            'base_tax': 8429.3,
            'nice': False,
            'naughty_tax': 83.50,
        }
        naughty_fields = {
            '1': f0.fields()[0].value(naughty_inputs, {}),
        }
        naughty_fields['2'] = f0.fields()[1].value(naughty_inputs, naughty_fields)

        self.assertAlmostEqual(naughty_fields['2'], 8512.80, places=2)

        # Test with 'nice' input
        nice_inputs = {
            'base_tax': 8429.3,
            'nice': True,
        }
        nice_fields = {
            '1': f0.fields()[0].value(nice_inputs, {}),
        }
        nice_fields['2'] = f0.fields()[1].value(nice_inputs, nice_fields)

        self.assertAlmostEqual(nice_fields['2'], 8429.3, places=2)

    def test_formsomething_example(self):
        fsomething = self.find_compile_doc_code('adding_modifying_forms.md', 'fsomething.py')

        # Defines class FormSomething
        exec(fsomething, globals())

        f0 = FormSomething()
        self.assertEqual(len(f0.inputs()), 3)
        self.assertEqual(len(f0.required_fields()), 3)
        self.assertEqual(len(f0.fields()), 3)

        inputs = {
            'name': "Monty",
            'ssn': "000-00-0000",
            'eye_color': f0.EYES.brown,
        }

        values = {}
        for field in f0.required_fields():
            values[field.name()] = field.value(inputs, values)

        self.assertEqual(values['something.name'], "Monty")
        self.assertEqual(values['something.ssn'], "000-00-0000")
        self.assertEqual(values['something.eye_color'], f0.EYES.brown)
