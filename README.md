# HabuTax

<p align="center">
<img src="doc/habutax_logo.svg" alt="HabuTax Logo" title="HabuTax Logo" width="384"/>
</p>

HabuTax is a package designed to help you compute your United States income tax
return. It aims to be simple (both in implementation and ease of use) and
extensible (to make it easy for contributors to expand the existing set of
forms).

## Design Goals

* **Fail loudly:** If a particular form or calculation is not implemented,
  HabuTax should inform the user and fail to complete their return. Even if a
  particular case is rare, we would rather notify the user that something is
  amiss than silently fail to correctly calculate their return.
* **Simplicity:** HabuTax aims to be simple in order to ease implementation and
  reduce the chance of errors or other bugs. For now, this means the primary
  interface is the command-line and text files.
* **Form Modularity:** Much of the complexity of US income tax returns comes
  from the quantity of calculations rather than the complexity of any individual
  calculation. HabuTax tackles this complexity with a divide-and-conquer
  approach: It specifies calculations and dependencies at the level of
  individual form fields and uses a generic dependency solver to identify the
  dependencies and perform all calculations. This makes it much easier to add
  and modify tax forms as well as detect/report unimplemented scenarios at a
  fine granularity.
* **Tested:** We seek to test HabuTax with various income tax return scenarios
  to ensure its calculations are correct.

## Implemented Forms

* 1040 (no variants)
* 1040, Schedule 1
* 1040, Schedule A
* 1040, Schedule B
* 8606
* 8995 (currently only Section 199a dividends, but additional Qualified Business
  Income support could be added upon request)

### Inputs

In addition to the above "output" forms, HabuTax supports the following forms
provided to you by your employer or financial institution:

* 1098
* 1099-DIV
* 1099-G
* 1099-INT
* 1099-R
* W-2

## Coming soon

* 1040, Schedule 3
* 2441
* 8283
* 8889
* 8959
* NC state forms

## Usage

You can test HabuTax out with the following command-lines:

```
% git clone https://github.com/habutax/habutax
% cd habutax
% python3 -m habutax \
    --year 2021 \
    --form 1040 \
    --writeback \
    --prompt-missing \
    taxes_2021.habutax
```

taxes_2021.habutax is a plain-text input file, in [INI
format](https://en.wikipedia.org/wiki/INI_file#Format). Each form has its own
section in the input file. If you don't want to supply anything up front, you
don't need to: the `--prompt` option causes HabuTax to prompt you for any
missing input, while `--writeback` causes any values you enter interactively in
this way to be written back to the input file.

The output is currently printed to stdout, though we plan to optionally write
the output to a text file.

For complete help text for the command-line interface, you can use `python3 -m
habutax --help`.

## Contributing

Please feel free to open an issue if you have ideas for improving HabuTax, or
jump straight to a merge request if you have fairly simple code contributions.
Opening an issue to discuss the architecture of your contribution may be helpful
to avoid wasted effort for more significant changes.

To learn more about the HabuTax internals, you may wish to read our
documentation about [how the solver works](doc/solver.md) or [how to add/modify
tax forms](doc/adding_modifying_forms.md).

### Tests

Tests are currently run using `make test` in the root directory of the
repository. We are always looking to add additional tests, and particularly
welcome your contribution of anonymized tax input data (along with the right
answers!) to help ensure HabuTax's calculations remain correct for all
scenarios.
