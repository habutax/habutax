#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys

from habutax import forms
from habutax import inputs
from habutax import solver
from habutax import values

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='The file containing your input for the tax forms you are calculating.')
    parser.add_argument('--year', type=int, default=2021, help='The tax year to use')
    parser.add_argument('--form', dest='forms', action='append', help='Which form(s) you want to calculate')
    parser.add_argument('--prompt-missing', action='store_true', default=False, help='Interactively prompt for any missing input')
    parser.add_argument('--writeback', action='store_true', default=False, help='Write any interactively-supplied input back to the config file when done (loses any comments/formatting present in file)')
    args = parser.parse_args()

    if args.writeback:
        Path(args.input_file).touch() # Ensure the input file exists (this allows writing back without the user having to manually touch it first)

    input_store = inputs.InputStore(args.input_file)
    s = solver.Solver(input_store, forms.available_forms[args.year], prompt=args.prompt_missing)
    s.solve(args.forms)

    if args.writeback:
        input_store.write(args.input_file)

if __name__ == "__main__":
    main()
