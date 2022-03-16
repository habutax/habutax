__version__ = '0.0.4'

import argparse
import configparser
from pathlib import Path
import sys

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

    # Prompt the user to input missing input value
    prompt = f'\n----[ {missing.name()} ]----'
    prompt += '-' * max(0, (80 - len(prompt))) + '\n'

    # Provide context for why this question is being asked
    prompt += 'Additional input is needed by:\n'
    duplicates = {}
    for f in needed_by:
        form_desc = f.form().full_description()
        field_basename = f.base_name()
        instance = f'Instance \'{f.form().instance()}\' of ' if f.form().instance() else ''
        potential_prompt = f' * {instance}{form_desc}, line \'{field_basename}\'\n'
        if potential_prompt not in duplicates:
            duplicates[potential_prompt] = True
            prompt += potential_prompt

    # Include any help from the input specification about the question being
    # asked or the expected format of the response
    prompt += '\n-> ' + missing.help() + '\n\n'
    format_suggestion = missing.format_suggestion()
    if len(format_suggestion) > 0:
        prompt += format_suggestion + '\n'

    prompt += f'(Ctrl-C to abort): '

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
    try:
        successful = s.solve(args.forms)
        solution = s.solution()
    except Exception as e:
        raise e
    finally:
        # Ensure that even if an exception happens, any output the user already
        # entered is saved as they requested
        if args.writeback_input:
            input_store.write(args.input_file)

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

def fill_pdfs(args):
    solution = configparser.ConfigParser()
    with open(args.solution) as solution_file:
        solution.read_file(solution_file)
    tax_year = solution.getint('habutax', 'tax_year')

    # Remove this 'special' section so the PDF filler doesn't interpret it as
    # form data to be filled
    solution.remove_section('habutax')

    p = pdf_filler.PDFFiller(solution, forms.available_forms[tax_year], args.output, flatten=args.flatten)
    p.fill()

def list_forms(args):
    header_printed = False
    if args.contains is not None:
        search_string = args.contains.lower()

    width = max([len(f.form_name) for f in forms.available_forms[args.year]])
    format_str ="{:>{width}} | {:12} | {}"

    for form in forms.available_forms[args.year]:
        name = form.form_name

        description = f'{form.description}: {form.long_description}'
        search_match = args.contains is None or search_string in name.lower() or search_string in description.lower()
        jurisdiction_match = args.jurisdiction is None or args.jurisdiction.lower() == form.jurisdiction.name.lower()
        if search_match and jurisdiction_match:
            if not header_printed:
                header_printed = True
                if args.contains:
                    print("Matching forms:")
                else:
                    print("Form list:")
                print(format_str.format("name", "jurisdiction", "description", width=width))
                print(format_str.format("-"*width, "-"*12, "-"*width, width=width))
            print(format_str.format(name, form.jurisdiction.name, description, width=width))

    if not header_printed and (args.contains or args.jurisdiction):
        print("No forms matched your parameters")

def list_form_inputs(args):
    form_name, form_instance = form.name_and_instance(args.form)
    forms_map = {f.form_name : f for f in forms.available_forms[args.year]}

    if form_name not in forms_map:
        print(f'Cannot find form "{args.form}". The `list-forms` sub-command will list the valid form names.')
        sys.exit(1)

    form_class = forms_map[form_name]
    if hasattr(form_class, 'valid_instances'):
        if form_instance not in form_class.valid_instances:
            instances = ", ".join([f'"{i}"' for i in form_class.valid_instances])
            print(f'Form "{form_name}" requires a form instance be specified and that it be one of {instances}. For example, try "{form_name}:{form_class.valid_instances[0]}".')
            sys.exit(1)

    f = form_class(instance=form_instance)
    print(f'[{f.name()}]')
    print(f'# {f.full_description()}')

    input_map = {i.name(): i for i in f.inputs()}
    sorted_inputs = sorted(input_map.keys(), key=solver.sort_keys)

    for input_name in sorted_inputs:
        form_input = input_map[input_name]
        comment = '# ' + form_input.help() + '\n'
        format_suggestion = form_input.format_suggestion()
        if len(format_suggestion) > 0:
            comment += format_suggestion
        print('\n' + comment.replace('\n', '\n# '))
        print(f'#{form_input.base_name()} =')

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, help='sub-command help')
    default_year = 2021

    # Solver argument setup
    solve_parser = subparsers.add_parser('solve', help='Solve taxes using HabuTax')
    solve_parser.add_argument('input_file', type=str, help='The file containing your input for the tax forms you are calculating.')
    solve_parser.add_argument('--year', type=int, default=default_year, help=f'The tax year to use (default: {default_year})')
    solve_parser.add_argument('--form', dest='forms', action='append', help='Which form(s) you want to calculate')
    solve_parser.add_argument('--prompt-missing', action='store_true', default=False, help='Interactively prompt for any missing input')
    solve_parser.add_argument('--writeback-input', action='store_true', default=False, help='Write any interactively-supplied input back to the config file when done (loses any comments/formatting present in file)')
    solve_parser.add_argument('--solution', type=str, default=None, help='Output text file for the results of the tax solver (defaults to stdout)')
    solve_parser.set_defaults(func=solve)

    # fill-pdfs argument setup
    fill_pdfs_parser = subparsers.add_parser('fill-pdfs', help='Fill PDFs using a solution previously calculated using HabuTax')
    fill_pdfs_parser.add_argument('--no-flatten', dest='flatten', action='store_false', default=True, help='Do not "flatten" the PDF after filling, so its fields can still be edited')
    fill_pdfs_parser.add_argument('solution', type=str, help='The file containing the solution of the tax forms you want to generate PDFs of.')
    fill_pdfs_parser.add_argument('output', type=str, help='Path where you want to write the generated PDF file')
    fill_pdfs_parser.set_defaults(func=fill_pdfs)

    # list-forms argument setup
    list_forms_parser = subparsers.add_parser('list-forms', help='List all available forms, optionally restricting to those containing a string or within a jurisdiction')
    list_forms_parser.add_argument('--year', type=int, default=default_year, help=f'The tax year to use (default: {default_year})')
    list_forms_parser.add_argument('--contains', type=str, default=None, help='A string to search for (only print forms containing this string)')
    list_forms_parser.add_argument('--jurisdiction', type=str, default=None, help='Only display forms from this tax jurisdiction ("US" federal, "NC" state, etc.)')
    list_forms_parser.set_defaults(func=list_forms)

    # list-form-inputs argument setup
    list_form_inputs_parser = subparsers.add_parser('list-form-inputs', help='List all available inputs for a given form, in a format suitable for editing and passing as input to HabuTax.')
    list_form_inputs_parser.add_argument('form', type=str, help='The short name of the form for which you want to display the inputs')
    list_form_inputs_parser.add_argument('--year', type=int, default=default_year, help=f'The tax year to use (default: {default_year})')
    list_form_inputs_parser.set_defaults(func=list_form_inputs)

    args = parser.parse_args()
    args.func(args)
