#!/usr/bin/env python3

import argparse
import sys

import forms
import inputs
import solver
import values

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=argparse.FileType('r'), help='The file containing your input for the tax forms you are calculating.')
    parser.add_argument('--year', type=int, default=2021, help='The tax year to use')
    parser.add_argument('--form', dest='forms', action='append', help='Which form(s) you want to calculate')
    parser.add_argument('--writeback', action='store_true', default=False, help='Write any interactively-supplied input back to the config file when done (loses any comments/formatting present in file)')
    args = parser.parse_args()

    assert(len(args.forms) == 1) # TODO allow specifying more than one form

    forms_todo = []
    for form_name in args.forms:
        if args.year not in forms.available:
            print(f'Tax year {args.year} is not supported. Exiting...')
        found = False
        for f in forms.available[args.year]:
            if f().name() == form_name:
                found = True
                forms_todo.append(f)
                break
        if not found:
            print(f'Form {form_name} is not available for tax year {args.year}. Exiting...')
            sys.exit(1)

    input_store = inputs.InputStore(args.input_file.name)
    s = solver.Solver(input_store, forms.available[args.year])
    s.solve(forms_todo[0]())

    if args.writeback:
        input_store.write(args.input_file.name)

if __name__ == "__main__":
    main()
