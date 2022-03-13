import habutax.enum as enum
from habutax.form import InputForm, Jurisdiction
from habutax.inputs import *

class Form1099R(InputForm):
    form_name = "1099-r"
    tax_year = 2021
    description = "Form 1099-R"
    long_description = "Distributions From Pensions, Annuities, Retirement or Profit-Sharing Plans, IRAs, Insurance Contracts, etc."
    jurisdiction = Jurisdiction.US

    def __init__(self, **kwargs):
        inputs = [
            StringInput('payer', description="Who paid you this distribution?"),
            StringInput('recipient', description="To whom was this distribution paid? (you or your spouse's name)"),
            EnumInput('belongs_to', enum.taxpayer_or_spouse, description="To whom was this distribution paid?"),
            FloatInput('box_1', description="Gross distribution"),
            FloatInput('box_2a', description="Taxable amount"),
            BooleanInput('box_2b_taxable_not_determined', description="'Taxable amount not determined' checked"),
            BooleanInput('box_2b_total_distribution', description="'Total distribution' checked"),
            FloatInput('box_3', description="Capital gain (included in box 2a)"),
            FloatInput('box_4', description="Federal income tax withheld"),
            FloatInput('box_5', description="Employee contributions/Designated Roth contributions or insurance premiums"),
            FloatInput('box_6', description="Net unrealized appreciation in employer’s securities"),
            StringInput('box_7_distirbution_codes', description="Distribution code(s)"),
            BooleanInput('box_7_ira_sep_simple', description="'IRA/SEP/SIMPLE' checked"),
            FloatInput('box_8', description="Other ($)"),
            FloatInput('box_8_pct', description="Other (%)"),
            FloatInput('box_9a', description="Your percentage of total distibution"),
            FloatInput('box_9b', description="Total employee contributions"),
            FloatInput('box_10', description="Amount allocable to IRR within 5 years"),
            FloatInput('box_11', description="1st year of desig. Roth contrib."),
            BooleanInput('box_12', description="'FATCA filing requirement' checked"),
            StringInput('box_13', description="Date of payment"),
            StringInput('box_14', description="Tax-exempt and tax credit bond CUSIP no."),
            FloatInput('box_14_1', description="State tax withheld"),
            EnumInput('box_14_1_state', enum.us_states, allow_empty=True, description="State for which tax was withheld"),
            StringInput('box_15_1', description="State/Payer's state no."),
            FloatInput('box_16_1', description="State distribution"),
            FloatInput('box_14_2', description="State tax withheld"),
            EnumInput('box_14_2_state', enum.us_states, allow_empty=True, description="State for which tax was withheld"),
            StringInput('box_15_2', description="State/Payer's state no."),
            FloatInput('box_16_2', description="State distribution"),
            FloatInput('box_17_1', description="Local tax withheld"),
            StringInput('box_18_1', description="Name of locality"),
            FloatInput('box_19_1', description="Local distribution"),
            FloatInput('box_17_2', description="Local tax withheld"),
            StringInput('box_18_2', description="Name of locality"),
            FloatInput('box_19_2', description="Local distribution"),
        ]

        super().__init__(__class__, inputs, **kwargs)
