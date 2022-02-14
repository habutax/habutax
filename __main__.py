#!/usr/bin/env python3

import forms
import inputs
import solver
import values

def main():
    input_store = inputs.InputStore('example.pytax')
    s = solver.Solver(input_store, [forms.Form1040])
    s.solve(forms.Form1040())

if __name__ == "__main__":
    main()
