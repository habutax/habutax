__version__ = '0.0.1'

import argparse
import configparser
from pathlib import Path

from habutax import enum
from habutax import fields
from habutax import form
from habutax import forms
from habutax import inputs
from habutax import pdf_fields
from habutax import pdf_filler
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

def solve(args):
    if args.writeback_input:
        Path(args.input_file).touch() # Ensure the input file exists (this allows writing back without the user having to manually touch it first)

    input_store = inputs.InputStore(args.input_file)
    prompt_fn = prompt_input if args.prompt_missing else None
    s = solver.Solver(input_store, forms.available_forms[args.year], prompt=prompt_fn)
    successful = s.solve(args.forms)
    solution = s.solution()

    # Attach tax year to solution
    solution['habutax'] = {
        'tax_year': args.year,
        'version': __version__,
    }

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

    if not args.solution:
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
        with open(args.solution, 'w') as outfile:
            solution.write(outfile)
        print(f'\nSolver results written to {args.solution}')

    if args.writeback_input:
        input_store.write(args.input_file)

def fill_pdfs(args):
    solution = configparser.ConfigParser()
    with open(args.solution) as solution_file:
        solution.read_file(solution_file)
    tax_year = solution.getint('habutax', 'tax_year')

    # Remove this 'special' section so the PDF filler doesn't interpret it as
    # form data to be filled
    solution.remove_section('habutax')

    p = pdf_filler.PDFFiller(solution, forms.available_forms[tax_year], args.output)
    p.fill()

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    # Solver argument setup
    solve_parser = subparsers.add_parser('solve', help='Solve taxes using HabuTax')
    solve_parser.add_argument('input_file', type=str, help='The file containing your input for the tax forms you are calculating.')
    solve_parser.add_argument('--year', type=int, default=2021, help='The tax year to use')
    solve_parser.add_argument('--form', dest='forms', action='append', help='Which form(s) you want to calculate')
    solve_parser.add_argument('--prompt-missing', action='store_true', default=False, help='Interactively prompt for any missing input')
    solve_parser.add_argument('--writeback-input', action='store_true', default=False, help='Write any interactively-supplied input back to the config file when done (loses any comments/formatting present in file)')
    solve_parser.add_argument('--solution', type=str, default=None, help='Output text file for the results of the tax solver (defaults to stdout)')
    solve_parser.set_defaults(func=solve)

    # fill-pdfs argument setup
    fill_pdfs_parser = subparsers.add_parser('fill-pdfs', help='Fill PDFs using a solution previously calculated using HabuTax')
    fill_pdfs_parser.add_argument('solution', type=str, help='The file containing the solution of the tax forms you want to generate PDFs of.')
    fill_pdfs_parser.add_argument('output', type=str, help='Path where you want to write the generated PDF file')
    fill_pdfs_parser.set_defaults(func=fill_pdfs)

    args = parser.parse_args()
    args.func(args)
