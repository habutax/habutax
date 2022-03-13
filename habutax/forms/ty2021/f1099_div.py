import habutax.enum as enum
from habutax.form import InputForm, Jurisdiction
from habutax.inputs import *

class Form1099DIV(InputForm):
    form_name = "1099-div"
    tax_year = 2021
    description = "Form 1099-DIV"
    long_description = "Dividends and Distributions"
    jurisdiction = Jurisdiction.US

    def __init__(self, **kwargs):
        inputs = [
            EnumInput('belongs_to', enum.taxpayer_spouse_or_both, description="To whom does this 1099-DIV belong?"),
            StringInput('payer', description="Who paid you these dividends?"),
            StringInput('recipient', description="To whom was this dividend paid? (you or your spouse's name)"),
            FloatInput('box_1a', description="Total ordinary dividends"),
            FloatInput('box_1b', description="Qualified dividends"),
            FloatInput('box_2a', description="Total capital gain distr."),
            FloatInput('box_2b', description="Unrecap. Sec. 1250 gain"),
            FloatInput('box_2c', description="Section 1202 gain"),
            FloatInput('box_2d', description="Collectibles (28%) gain"),
            FloatInput('box_2e', description="Section 897 ordinary dividends"),
            FloatInput('box_2f', description="Section 897 capital gain"),
            FloatInput('box_3', description="Nondividend distributions"),
            FloatInput('box_4', description="Federal income tax withheld"),
            FloatInput('box_5', description="Section 199A dividends"),
            FloatInput('box_6', description="Investment expenses"),
            FloatInput('box_7', description="Foreign tax paid"),
            StringInput('box_8', description="Foreign country or US possesion"),
            FloatInput('box_9', description="Cash liquidation distributions"),
            FloatInput('box_10', description="Noncash liquidation distributions"),
            BooleanInput('box_11', description="FATCA filing requirement box checked"),
            FloatInput('box_12', description="Exempt-interest dividend"),
            FloatInput('box_13', description="Specified private activity bond interest dividends"),
            EnumInput('box_14_1', enum.us_states, allow_empty=True, description="State #1"),
            StringInput('box_15_1', description="State #1 identification no."),
            FloatInput('box_16_1', description="State #1 tax withheld"),
            EnumInput('box_14_2', enum.us_states, allow_empty=True, description="State #2"),
            StringInput('box_15_2', description="State #2 identification no."),
            FloatInput('box_16_2', description="State #2 tax withheld"),
        ]

        super().__init__(__class__, inputs, **kwargs)
