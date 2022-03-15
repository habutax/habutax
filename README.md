# HabuTax

<p align="center">
<img src="https://github.com/habutax/habutax/raw/main/doc/habutax_logo.svg" alt="HabuTax Logo" title="HabuTax Logo" width="384"/>
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

* Form 1040, U.S. Individual Income Tax Return
* Schedule 1 (Form 1040), Additional Income and Adjustments to Income
* Schedule 3 (Form 1040), Additional Credits and Payments (part I only)
* Schedule A (Form 1040), Itemized Deductions
* Schedule B (Form 1040), Interest and Ordinary Dividends
* Schedule 8812 (Form 1040), Credits for Qualifying Children and Other
  Dependents
* Form 8606, Nondeductible IRAs
* Form 8959, Additional Medicare Tax
* Form 8995, Qualified Business Income Deduction Simplified Computation
  (currently only Section 199a dividends, but additional Qualified Business
  Income support could be added upon request)
* Form 8889, Health Savings Accounts
* NC Tax Forms (Form D-400, N.C. Individual Income Tax Return plus schedules A and S)

### Inputs

In addition to the above "output" forms, HabuTax supports the following forms
provided to you by your employer or financial institution:

* Form 1098, Mortgage Interest Statement
* Form 1099-DIV, Dividends and Distributions
* Form 1099-G, Certain Government Payments (previous-year state income tax
  refunds)
* Form 1099-INT, Interest Income
* Form 1099-R, Distributions From Pensions, Annuities, Retirement or
  Profit-Sharing Plans, IRAs, Insurance Contracts, etc.
* Form W-2, Wage and Tax Statement

## Coming soon

* Form 2441, Child and Dependent Care Expenses

## Installation

HabuTax can be used either directly from a source checkout, or by installing it
as a package.

### Dependencies

HabuTax requires Python >= 3.8. An installation of
[pdftk](https://gitlab.com/pdftk-java/pdftk) is additionally required to fill
PDF forms after solving (output to plain text does not require it).

### Package Installation

Installing the latest released version of HabuTax is as easy as `pip install
habutax`.

### Package Installation (from Source)

To install HabuTax as a local python package using the latest source (regardless
of whether it is released), execute the following commands (noting that the
version number may change from the below):

```
% git clone https://github.com/habutax/habutax && cd habutax
% python -m build
% pip install dist/habutax-0.0.1-py3-none-any.whl
% habutax --help
```

### Running Directly from Source Directory

To run out of your source directory, clone the git repository and prefix the
`habutax` command with `python3 -m`:

```
% git clone https://github.com/habutax/habutax && cd habutax
% python3 -m habutax --help
```

Note that the remainder of the documentation assumes that you have HabuTax
installed as a package, so if you choose to run it out of the source directory,
you will need to prefix all the `habutax` commands you see with `python3 -m`,
and ensure you are running out of the root of the directory.

## Usage

You can test HabuTax out with the following command-line:

```
habutax solve \
    --year 2021 \
    --form 1040 \
    --writeback-input \
    --prompt-missing \
    --solution taxes_2021.solution \
    taxes_2021.habutax
```

taxes_2021.habutax is a plain-text input file, in [INI
format](https://en.wikipedia.org/wiki/INI_file#Format). Each form has its own
section in the input file. If you don't want to supply anything up front, you
don't need to: the `--prompt` option causes HabuTax to prompt you for any
missing input, while `--writeback-input` causes any values you enter
interactively in this way to be written back to the input file.

The above example saves the results to a file named `taxes_2021.solution`. If
you omit the `--solution` argument, it will print the results to stdout instead.

Once you have successfully "solved" your taxes, you can write the results to PDF
using:

```
habutax fill-pdfs \
    taxes_2021.solution \
    taxes_2021.pdf
```

HabuTax also has sub-commands for listing the available forms (`habutax
list-forms`) or list all possible inputs form a form (`habutax
list-form-inputs`).

For complete help text for the command-line interface, you can use `habutax
--help` (`--help` is also available on the sub-commands).

## Can You Help?

Please [open an issue](https://github.com/habutax/habutax/issues/new) if you
want to help or have ideas for improving HabuTax, or jump straight to a merge
request if you have fairly simple code contributions. Opening an issue to
discuss the architecture of your contribution first may be helpful to avoid
wasted effort for more significant changes.

One of the primary motivations in the design of HabuTax is to ensure it is easy
to [add and maintain new
forms](https://github.com/habutax/habutax/tree/main/doc/adding_modifying_forms.md).
Crowdsourcing this piece is important to ensure this project remains healthy
long-term. We are open to ideas of how best to do so: One idea is to have
contributors informally agree to update and/or test an individual form for
coming tax year. Our guess is that, on average, updating a single form for a new
year will take less time than filling out a personal income tax return!

To learn more about the HabuTax internals, you may wish to read our
documentation about [how the solver
works](https://github.com/habutax/habutax/tree/main/doc/solver.md) or [how to
add/modify tax
forms](https://github.com/habutax/habutax/tree/main/doc/adding_modifying_forms.md).

### Tests and Form Data for Them

Tests are currently run using `make test` in the root directory of the
repository. We are always looking to add additional tests, and particularly
welcome your contribution of anonymized tax input data (along with the right
answers!) to help ensure HabuTax's calculations remain correct for all
scenarios. Even data from a single form in isolation is quite helpful. Please
free to [open an issue](https://github.com/habutax/habutax/issues/new)
describing what you would like to do!
