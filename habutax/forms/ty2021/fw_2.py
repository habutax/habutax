import habutax.enum as enum
from habutax.form import InputForm, Jurisdiction
from habutax.inputs import *

class FormW2(InputForm):
    form_name = "w-2"
    tax_year = 2021
    description = "Form W-2"
    long_description = "Wage and Tax Statement"
    jurisdiction = Jurisdiction.US

    def __init__(self, **kwargs):
        # FIXME go through these inputs and prohibit those we don't handle
        # (fail loudly)
        box_12 = enum.make("W-2, box 12 code", {
            'A': 'Uncollected social security or RRTA tax on tips. Include this tax on Form 1040 or 1040-SR. See the Form 1040 instructions.',
            'B': 'Uncollected Medicare tax on tips. Include this tax on Form 1040 or 1040-SR. See the Form 1040 instructions.',
            'C': 'Taxable cost of group-term life insurance over $50,000 (included in boxes 1, 3 (up to the social security wage base), and 5)',
            'D': 'Elective deferrals to a section 401(k) cash or deferred arrangement.  Also includes deferrals under a SIMPLE retirement account that is part of a section 401(k) arrangement.',
            'E': 'Elective deferrals under a section 403(b) salary reduction agreement',
            'F': 'Elective deferrals under a section 408(k)(6) salary reduction SEP',
            'G': 'Elective deferrals and employer contributions (including nonelective deferrals) to a section 457(b) deferred compensation plan',
            'H': 'Elective deferrals to a section 501(c)(18)(D) tax-exempt organization plan. See the Form 1040 instructions for how to deduct.',
            'J': 'Nontaxable sick pay (information only, not included in box 1, 3, or 5)',
            'K': '20% excise tax on excess golden parachute payments. See the Form 1040 instructions.',
            'L': 'Substantiated employee business expense reimbursements (nontaxable)',
            'M': 'Uncollected social security or RRTA tax on taxable cost of group- term life insurance over $50,000 (former employees only). See the Form 1040 instructions.',
            'N': 'Uncollected Medicare tax on taxable cost of group-term life insurance over $50,000 (former employees only). See the Form 1040 instructions.',
            'P': 'Excludable moving expense reimbursements paid directly to a member of the U.S. Armed Forces (not included in box 1, 3, or 5)',
            'Q': 'Nontaxable combat pay. See the Form 1040 instructions for details on reporting this amount.',
            'R': 'Employer contributions to your Archer MSA. Report on Form 8853, Archer MSAs and Long-Term Care Insurance Contracts.',
            'S': 'Employee salary reduction contributions under a section 408(p) SIMPLE plan (not included in box 1)',
            'T': 'Adoption benefits (not included in box 1). Complete Form 8839, Qualified Adoption Expenses, to figure any taxable and nontaxable amounts.',
            'V': 'Income from exercise of nonstatutory stock option(s) (included in boxes 1, 3 (up to the social security wage base), and 5). See Pub. 525, Taxable and Nontaxable Income, for reporting requirements.',
            'W': 'Employer contributions (including amounts the employee elected to contribute using a section 125 (cafeteria) plan) to your health savings account. Report on Form 8889, Health Savings Accounts (HSAs).',
            'Y': 'Deferrals under a section 409A nonqualified deferred compensation plan',
            'Z': 'Income under a nonqualified deferred compensation plan that fails to satisfy section 409A. This amount is also included in box 1. It is subject to an additional 20% tax plus interest. See the Form 1040 instructions.',
            'AA': 'Designated Roth contributions under a section 401(k) plan',
            'BB': 'Designated Roth contributions under a section 403(b) plan',
            'DD': 'Cost of employer-sponsored health coverage. The amount reported with code DD is not taxable.',
            'EE': 'Designated Roth contributions under a governmental section 457(b) plan. This amount does not apply to contributions under a tax- exempt organization section 457(b) plan.',
            'FF': 'Permitted benefits under a qualified small employer health reimbursement arrangement',
            'GG': 'Income from qualified equity grants under section 83(i)',
            'HH': 'Aggregate deferrals under section 83(i) elections as of the close of the calendar year',
        })
        inputs = []
        for letter in 'abcd':
            inputs.append(EnumInput(f'box_12{letter}_code', box_12, allow_empty=True, description=f'Box 12{letter} alphabetic code'))
            inputs.append(FloatInput(f'box_12{letter}_value', description=f'Box 12{letter} value'))
        inputs += [
            EnumInput('belongs_to', enum.taxpayer_or_spouse, description="To whom does this W-2 belong?"),
            StringInput('box_c', description="Employer"),
            StringInput('box_d', description="Control number"),
            StringInput('box_e', description="Employee's name"),
            StringInput('box_f', description="Employee's address and zipcode"),
            FloatInput('box_1', description="Wages, tips, other compensation"),
            FloatInput('box_2', description="Federal income tax withheld"),
            FloatInput('box_3', description="Social security wages"),
            FloatInput('box_4', description="Social security tax withheld"),
            FloatInput('box_5', description="Medicare wages and tips"),
            FloatInput('box_6', description="Medicare tax withheld"),
            FloatInput('box_7', description="Social security tips"),
            FloatInput('box_8', description="Allocated tips"),
            FloatInput('box_10', description="Dependent care benefits"),
            FloatInput('box_11', description="Nonqualified plans"),
            BooleanInput('box_13_statutory', description="Box 13 statutory employee checked"),
            BooleanInput('box_13_retirement', description="Box 13 Retirement plan checked"),
            BooleanInput('box_13_sick_day', description="Box 13 third-party sick day"),
            StringInput('box_14', description="Other"),
            EnumInput('box_15', enum.us_states, allow_empty=True, description="State"),
            FloatInput('box_16', description="State wages, tips, etc."),
            FloatInput('box_17', description="State income tax"),
            FloatInput('box_18', description="Local wages, tips, etc."),
            FloatInput('box_19', description="Local income tax "),
            FloatInput('box_20', description="Locality name"),
        ]

        super().__init__(__class__, inputs, **kwargs)
