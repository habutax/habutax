import sys

import forms
import values
import inputs

class Solver(object):
    def __init__(self, input_config, form_list):
        self.i = input_config
        self.v = values.ValueStore()


    def get_input(self, missing):
        # See if the user wants to input this value, exit if not
        prompt = f'Missing config {missing.name} in [{missing.section}] section. To specify this input on the command-line, enter it below.\n\n'
        prompt += missing.help()
        prompt += f'\n{missing.name} (leave blank to exit): '
        text = input(prompt)
        if len(text) > 0:
            self.i[missing.name] = text
        else:
            print("Exiting...")
            sys.exit(1)

    def solve(self, form):
        input_map = {i.name: i for i in form.inputs()}
        field_map = {f.name: f for f in form.fields()}

        # Ensure form is fetching/validating input values through the lens of
        # the current form
        self.i.update_input_spec(input_map)

        # Set up initial dependency mappings on the first pass
        unmet_fields = {} # unmet dependencies -> dependents
        newly_satisfied_fields = {}
        newly_satisfied_inputs = {}
        for field in form.required_fields():
            try:
                self.v[field.name] = field.value(self.i, self.v)
                newly_satisfied_fields[field.name] = True
            except values.UnmetDependency as ud:
                if ud.dependency not in unmet_fields:
                    unmet_fields[ud.dependency] = [field]
                else:
                    unmet_fields[ud.dependency].append(field)
            except inputs.MissingInput as mi:
                # Go ahead and get prompt for missing values and add them to
                # newly_satisfied_inputs so we remember to re-check those
                # fields next pass
                missing = input_map[mi.input_name]
                self.get_input(missing)
                newly_satisfied_inputs[mi.input_name] = field

        while len(newly_satisfied_fields) + len(newly_satisfied_inputs) > 0:
            # First, pick which field we want to work on this time
            if len(newly_satisfied_inputs) > 0:
                met = next(iter(newly_satisfied_inputs))
                field = newly_satisfied_inputs[met]
                del newly_satisfied_inputs[met]
            else:
                met = next(iter(newly_satisfied_fields))
                # check if there are any fields waiting on this field
                if met in unmet_fields:
                    field = unmet_fields[met].pop()
                    if len(unmet_fields[met]) == 0:
                        del unmet_fields[met]
                        del newly_satisfied_fields[met]
                else:
                    del newly_satisfied_fields[met]
                    continue

            try:
                self.v[field.name] = field.value(self.i, self.v)
                newly_satisfied_fields[field.name] = True
            except values.UnmetDependency as ud:
                if ud.dependency not in unmet_fields:
                    unmet_fields[ud.dependency] = [field]
                else:
                    unmet_fields[ud.dependency].append(field)
            except inputs.MissingInput as mi:
                # Go ahead and prompt for missing values and add them to
                # newly_satisfied_inputs so we remember to re-check those
                # fields next pass
                missing = input_map[mi.input_name]
                self.get_input(missing)
                newly_satisfied_inputs[mi.input_name] = field

        if len(unmet_fields) > 0:
            print("\nFailed to solve for these fields:")
            for name in unmet_fields.keys():
                for field in unmet_fields[name]:
                    print(f'{field.name} (waiting on {name})')
            print("\nProgress so far:")
        else:
            print("Successfully solved:")

        for k, v in self.v.items():
            print(f'{k: <30}: {v}')
