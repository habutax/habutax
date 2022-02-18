from pytax.form import InputForm
from pytax.inputs import *

class Form1099INT(InputForm):
    form_name = "1099-int"
    tax_year = 2021

    def __init__(self, **kwargs):
        inputs = [
            StringInput('payer', description="Who paid you this interest?"),
            StringInput('recipient', description="To whom was this interest paid? (you or your spouse's name)"),
            FloatInput('box_1', description="Interest income"),
            FloatInput('box_2', description="Early withdrawal penalty"),
            FloatInput('box_3', description="Interest on U.S. Savings Bonds and Treasury obligations"),
            FloatInput('box_4', description="Federal income tax withheld"),
            FloatInput('box_5', description="Investment expenses"),
            FloatInput('box_6', description="Foreign tax paid"),
            StringInput('box_7', description="Foreign country or US possesion"),
            FloatInput('box_8', description="Tax-exempt interest"),
            FloatInput('box_9', description="Specified private activity bond interest"),
            FloatInput('box_10', description="Market discount"),
            FloatInput('box_11', description="Bond premium"),
            FloatInput('box_12', description="Bond premium on Treasury obligations"),
            FloatInput('box_13', description="Bond premium on tax-exempt bond"),
            StringInput('box_14', description="Tax-exempt and tax credit bond CUSIP no."),
            StringInput('box_15_1', description="State"),
            StringInput('box_15_2', description="State"),
            StringInput('box_16_1', description="State identification no."),
            StringInput('box_16_2', description="State identification no."),
            FloatInput('box_17_1', description="State tax withheld"),
            FloatInput('box_17_2', description="State tax withheld"),
        ]

        super().__init__(__class__, inputs, **kwargs)
