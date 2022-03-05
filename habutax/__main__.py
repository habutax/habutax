#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys

from habutax import forms
from habutax import inputs
from habutax import solver
from habutax import values

def prompt_input(missing, needed_by):
    """
    Given `missing`, an Input which the solver identified as being needed but
    not supplied, prompt the user to supply it. `needed_by` is a list of the
    Field objects which need the input.
    """
    # See if the user wants to input this value, exit if not
    prompt = f'Missing config {missing.name()} in [{missing.section()}] section. To specify this input on the command-line, enter it below.\n\n'
    prompt += missing.help()
    prompt += f'\n{missing.name()} (Ctrl-C to refuse to input): '

    value = None

    while value is None or not missing.valid(value):
        try:
            if value is not None:
                prompt = "Invalid input, try again?: "
            value = input(prompt)
        except KeyboardInterrupt:
            return (None, False)

    return (value, True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='The file containing your input for the tax forms you are calculating.')
    parser.add_argument('--year', type=int, default=2021, help='The tax year to use')
    parser.add_argument('--form', dest='forms', action='append', help='Which form(s) you want to calculate')
    parser.add_argument('--prompt-missing', action='store_true', default=False, help='Interactively prompt for any missing input')
    parser.add_argument('--writeback-input', action='store_true', default=False, help='Write any interactively-supplied input back to the config file when done (loses any comments/formatting present in file)')
    parser.add_argument('--output', type=str, default=None, help='Output text file for the results of the tax solver (defaults to stdout)')
    args = parser.parse_args()

    if args.writeback_input:
        Path(args.input_file).touch() # Ensure the input file exists (this allows writing back without the user having to manually touch it first)

    input_store = inputs.InputStore(args.input_file)
    prompt_fn = prompt_input if args.prompt_missing else None
    s = solver.Solver(input_store, forms.available_forms[args.year], prompt=prompt_fn)
    successful = s.solve(args.forms)
    solution = s.solution()

    if successful:
        print("\nSuccessfully solved!")
    else:
        print("\nFailed to solve, because...")

        unimplemented_fields = s.unimplemented_fields()
        unmet_input_dependencies = s.unmet_input_dependencies()
        unmet_field_dependencies = s.unmet_field_dependencies()

        if len(unimplemented_fields) > 0:
            print("\nThe following fields encountered unimplemented behavior:")
            for unimplemented in unimplemented_fields:
                print(f'- {unimplemented}')
        if len(unmet_input_dependencies) > 0:
            print("\nThe following inputs were needed but not supplied:")
            for dependency, dependents in unmet_input_dependencies.items():
                print(f'{dependency} (needed by: {", ".join(dependents)})')
        if len(unmet_field_dependencies) > 0:
            print("\nThe following fields were needed but unable to be produced (likely due to unsupplied inputs or unimplemented behavior above):")
            for dependency, dependents in unmet_field_dependencies.items():
                print(f'{dependency} (needed by: {", ".join(dependents)})')

    if not args.output:
        class StringWriter(object):
            def __init__(self):
                self.output = ""
            def write(self, written):
                self.output += written
            def __str__(self):
                return self.output
        string_writer = StringWriter()
        solution.write(string_writer)

        print(string_writer)
    else:
        with open(args.output, 'w') as outfile:
            solution.write(outfile)
        print(f'\nSolver results written to {args.output}')

    if args.writeback_input:
        input_store.write(args.input_file)

if __name__ == "__main__":
    main()
