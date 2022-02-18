import sys

from pytax import forms
from pytax import values
from pytax import inputs

class DependencyTracker(object):
    def __init__(self):
        # map names of unmet dependencies to a list of their outstanding
        # dependents
        self._unmet = {}

        # A list of the names of newly-satisfied dependencies
        self._met = []

    def add_unmet(self, dependency_name, dependent):
        """Add an unmet dependency for a particular dependent"""
        if dependency_name not in self._unmet:
            self._unmet[dependency_name] = [dependent]
        else:
            self._unmet[dependency_name].append(dependent)

    def has_met(self):
        """Return True if there are met dependencies which have not been
        removed by calling met_dependents()""" 
        return len(self._met) > 0

    def has_unmet(self):
        """Returns True if there are still unmet dependencies (does not count
        met dependencies which have not yet been removed via a call to
        met_dependents()"""
        for dependency, dependents in self._unmet.items():
            if len(dependents) > 0 and dependency not in self._met:
                return True
        return False

    def meet(self, dependency_name):
        """Mark a depdendency as having been satisfied (allows any dependents
        to be released in met_dependents()"""
        self._met.append(dependency_name)

    def unmet_dependencies(self):
        """Returns the names of the unmet dependencies"""
        return list(self._unmet.keys())

    def unmet_dependents(self, dependency):
        """Return the list of objects of the dependents waiting on an unmet dependency"""
        return self._unmet[dependency]

    def met_dependents(self):
        """Generator returning the objects representing all dependents whose
        dependencies have been marked as satisfied. Note that this also removes
        the returned dependency, so if a further dependency is later
        discovered, this object must be re-added using add_unmet()"""
        while len(self._met) > 0:
            met = self._met[0]
            # check if there are any dependents waiting on this satisfied dependency
            if met in self._unmet:
                dependent = self._unmet[met].pop()

                if len(self._unmet[met]) == 0:
                    del self._unmet[met]
                    self._met.pop(0)

                yield dependent
            else:
                self._met.pop(0)
                continue

class Solver(object):
    def __init__(self, input_config, form_list):
        # Create a map to easily look up the forms we have available by name
        self.form_map = {f.form_name: f for f in form_list}

        # Map all available input and field names to their objects
        self.input_map = {}
        self.field_map = {}

        # Input values (also modified with any values the user specifies
        # interactively)
        self.i = input_config

        # Current state of solver, including values calculated, any unmet
        # field/input dependencies
        self.v = values.ValueStore()
        self.unattempted_fields = []
        self.field_dependencies = DependencyTracker()
        self.input_dependencies = DependencyTracker()

    def _add_form(self, form_name):
        split_form_name = form_name.split(':') 
        form_instance = None
        if len(split_form_name) == 2:
            form_name = split_form_name[0]
        elif len(split_form_name) != 1:
            raise RuntimeError(f'Unexpected form name: {form_name} (expected 0 or 1 colons)')
        form_name = split_form_name[0]

        if form_name not in self.form_map:
            raise NotImplementedError(f'Form {form_name} is not supported.')

        form = self.form_map[form_name](instance=form_instance)

        # Add new inputs to our internal map of names to input objects, update
        # the input mapper so it understands how to read these inputs
        for i in form.inputs():
            assert(i not in self.input_map)
            self.input_map[i.name()] = i
        self.i.update_input_spec(self.input_map)

        for f in form.fields():
            assert(f not in self.form_map)
            self.form_map[f.name()] = f

        self.unattempted_fields.extend(form.required_fields())

    def _get_input(self, input_name):
        missing = self.input_map[input_name]

        # See if the user wants to input this value, exit if not
        prompt = f'Missing config {missing.name()} in [{missing.section()}] section. To specify this input on the command-line, enter it below.\n\n'
        prompt += missing.help()
        prompt += f'\n{missing.name()} (leave blank to exit): '
        text = input(prompt)
        if len(text) > 0:
            self.i[missing.name()] = text
        else:
            print("Exiting...")
            sys.exit(1)

        self.input_dependencies.meet(missing.name())

    def _attempt_field(self, field):
        try:
            form_inputs = forms.FormAccessor(self.i, field.form)
            form_values = forms.FormAccessor(self.v, field.form)
            self.v[field.name()] = field.value(form_inputs, form_values)
            self.field_dependencies.meet(field.name())
        except values.UnmetDependency as ud:
            self.field_dependencies.add_unmet(ud.dependency, field)
        except inputs.MissingInput as mi:
            self.input_dependencies.add_unmet(mi.input_name, field)

    def solve(self, form_names):
        for form_name in form_names:
            self._add_form(form_name)

        while len(self.unattempted_fields) > 0 \
                or self.input_dependencies.has_met() \
                or self.field_dependencies.has_met():

            while len(self.unattempted_fields) > 0:
                self._attempt_field(self.unattempted_fields.pop())
            for field in self.field_dependencies.met_dependents():
                self._attempt_field(field)
            for input_name in self.input_dependencies.met_dependents():
                self._get_input(input_name)

        print("==RESULTS===============================\n")
        assert(len(self.unattempted_fields) == 0)
        assert(not self.input_dependencies.has_met())
        assert(not self.field_dependencies.has_met())

        if self.field_dependencies.has_unmet() \
                or self.input_dependencies.has_unmet():
            print("Failed to solve - missing dependencies follow:")
            if self.field_dependencies.has_unmet():
                print("Missing field [needed by]:")
                for dep in self.field_dependencies.unmet_dependencies():
                    dependents = [f.name() for f in self.field_dependencies.unmet_dependents(dep)]
                    print(f'{dep}: {dependents}')
            if self.input_dependencies.has_unmet():
                print("Missing input: needed by")
                for dep in self.input_dependencies.unmet_dependencies():
                    dependents = [i.name() for i in self.input_dependencies.unmet_dependents(dep)]
                    print(f'{dep}: {dependents}')
            print("\nProgress so far:")
        else:
            print("Successfully solved:")

        for k, v in self.v.items():
            print(f'{k: <30}: {v}')
