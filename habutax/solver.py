import sys

from habutax import fields
from habutax import form
from habutax import inputs
from habutax import values

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

def _sort_keys(key):
    last_numeric = False
    last_alpha = False
    current = ''
    keys = []

    for c in key:
        this_numeric = c in '01234567890'
        this_alpha = c.isalpha()
        if (last_numeric and not this_numeric) or \
                (last_alpha and not this_alpha):
            if len(current) > 0:
                if last_numeric:
                    keys.append((False, int(current)))
                else:
                    keys.append((True, current))
                current = ''

        if this_numeric or this_alpha:
            current += c
        else:
            current = ''

        last_numeric = this_numeric
        last_alpha = this_alpha

    # Output the last partial sub-key in the string
    if len(current) > 0:
        if last_numeric:
            keys.append((False, int(current)))
        else:
            keys.append((True, current))

    return keys

def sort_keys(key):
    if isinstance(key, fields.Field) or isinstance(key, inputs.Input):
        key = key.name()

    if '.' in key:
        form, key = key.split('.')
    else:
        form = ''
    return (_sort_keys(form), _sort_keys(key))

class Solver(object):
    def __init__(self, input_config, form_list, prompt=None):
        self._prompt = prompt
        self._refused_input = self._prompt is None

        # Create a map to easily look up the available forms by name
        self._form_map = {f.form_name: f for f in form_list}

        # Map all available input and field names to their objects
        self._input_map = {}
        self._field_map = {}

        # Input values (also modified with any values the user specifies
        # interactively)
        self._i = input_config

        # Current state of solver, including form instances, values calculated,
        # any unmet field/input dependencies
        self.forms = {}
        self._v = values.ValueStore()
        self._unattempted_fields = []
        self._unimplemented_fields = []
        self._solving_fields = set()
        self._field_dependencies = DependencyTracker()
        self._input_dependencies = DependencyTracker()

        self._done_solving = False # Set to True if/when done solving
        self._solved = False       # Set to True if/when successfully solved

    def _add_unattempted(self, unattempted):
        if isinstance(unattempted, list):
            self._unattempted_fields.extend(unattempted)
        else:
            self._unattempted_fields.append(unattempted)
        self._unattempted_fields.sort(key=sort_keys)

    def _add_form(self, form_name):
        form_name, form_instance = form.name_and_instance(form_name)

        if form_name not in self._form_map:
            raise NotImplementedError(f'Form {form_name} is not supported.')

        new_form = self._form_map[form_name](solver=self, instance=form_instance)
        self.forms[new_form.name()] = new_form

        # Add new inputs to our internal map of names to input objects, update
        # the input mapper so it understands how to read these inputs
        for i in new_form.inputs():
            assert(i not in self._input_map)
            self._input_map[i.name()] = i
        self._i.update_input_spec(self._input_map)

        for f in new_form.fields():
            assert(f not in self._field_map)
            self._field_map[f.name()] = f

        self._add_unattempted(new_form.required_fields())
        self._solving_fields |= set([f.name() for f in new_form.required_fields()])

    def _attempt_input(self, input_name, needed_by):
        missing = self._input_map[input_name]

        value, supplied = self._prompt(missing, needed_by)

        if supplied:
            assert(missing.valid(value))
            self._i[missing.name()] = value
            self._input_dependencies.meet(missing.name())
        else:
            self._refused_input = True
        return supplied

    def _attempt_field(self, field):
        try:
            form_inputs = form.FormAccessor(self._i, field.form())
            form_values = form.FormAccessor(self._v, field.form())
            self._v[field.name()] = field.value(form_inputs, form_values)
            self._field_dependencies.meet(field.name())
        except values.UnmetDependency as ud:
            # If this field is not already in the fields the solver is
            # attempting to solve, add it
            if ud.dependency not in self._solving_fields:
                # If this field is not even in the list of forms the solver is
                # aware of, it must be in another form - find that form
                if ud.dependency not in self._field_map:
                    form_name, field_name = ud.dependency.split('.')
                    self._add_form(form_name)
                assert(ud.dependency in self._field_map)
                self._add_unattempted(self._field_map[ud.dependency])
                self._solving_fields.add(ud.dependency)

            self._field_dependencies.add_unmet(ud.dependency, field)
        except inputs.MissingInput as mi:
            self._input_dependencies.add_unmet(mi.input_name, field)
        except fields.FieldNotImplemented as fni:
            self._unimplemented_fields.append(fni.field_name)

    def solve(self, form_names):
        for form_name in form_names:
            self._add_form(form_name)

        while len(self._unattempted_fields) > 0 \
                or self._input_dependencies.has_met() \
                or (self._input_dependencies.has_unmet() and not self._refused_input) \
                or self._field_dependencies.has_met():

            while len(self._unattempted_fields) > 0:
                self._attempt_field(self._unattempted_fields.pop())
            for field in sorted(self._field_dependencies.met_dependents(), key=sort_keys):
                self._attempt_field(field)
            if not self._refused_input:
                for input_name in sorted(self._input_dependencies.unmet_dependencies(), key=sort_keys):
                    needed_by = self._input_dependencies.unmet_dependents(input_name)
                    self._attempt_input(input_name, needed_by)
                    if self._refused_input:
                        break
            # Must be list() because _attempt_field modifies
            # input_dependencies, and we don't want to get stuck in a loop
            # waiting for an input we can't provide without polling user for it
            for field in list(self._input_dependencies.met_dependents()):
                self._attempt_field(field)

        assert(len(self._unattempted_fields) == 0)
        assert(not self._input_dependencies.has_met())
        assert(not self._field_dependencies.has_met())

        self._done_solving = True

        if not self._field_dependencies.has_unmet() \
                and not self._input_dependencies.has_unmet() \
                and len(self._unimplemented_fields) == 0:
            self._solved = True

        return self._solved

    def solution(self):
        """Return a ConfigParser object representing the portions of the
        requested forms which were successfully solved"""
        assert(self._done_solving)
        return self._v.to_config(self._field_map)

    def unimplemented_fields(self):
        """Return a list of the unimplemented field names after a call to
        solve()"""
        assert(self._done_solving)
        return self._unimplemented_fields

    def _unmet_dependencies(self, dependency_tracker):
        unmet_dependencies = {}
        for dep in dependency_tracker.unmet_dependencies():
            dependents = [f.name() for f in dependency_tracker.unmet_dependents(dep)]
            unmet_dependencies[dep] = dependents
        return unmet_dependencies

    def unmet_input_dependencies(self):
        """Return a dict mapping names of any unmet input dependencies to a
        list of the names of their (discovered) dependent fields after a call
        to solve()"""
        assert(self._done_solving)
        return self._unmet_dependencies(self._input_dependencies)

    def unmet_field_dependencies(self):
        """Return a dict mapping names of any unmet field dependencies to a
        list of the names of their (discovered) dependents after a call to
        solve()"""
        assert(self._done_solving)
        return self._unmet_dependencies(self._field_dependencies)
