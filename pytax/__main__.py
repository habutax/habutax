#!/usr/bin/env python3

import argparse
import sys

from pytax import forms
from pytax import inputs
from pytax import solver
from pytax import values

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=argparse.FileType('r'), help='The file containing your input for the tax forms you are calculating.')
    parser.add_argument('--year', type=int, default=2021, help='The tax year to use')
    parser.add_argument('--form', dest='forms', action='append', help='Which form(s) you want to calculate')
    parser.add_argument('--prompt-missing', action='store_true', default=False, help='Interactively prompt for any missing input')
    parser.add_argument('--writeback', action='store_true', default=False, help='Write any interactively-supplied input back to the config file when done (loses any comments/formatting present in file)')
    args = parser.parse_args()

    input_store = inputs.InputStore(args.input_file.name)
    s = solver.Solver(input_store, forms.available_forms[args.year], prompt=args.prompt_missing)
    s.solve(args.forms)

    if args.writeback:
        input_store.write(args.input_file.name)

if __name__ == "__main__":
    main()
