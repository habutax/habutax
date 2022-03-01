from habutax.form import InputForm
from habutax.inputs import *

class Form1099DIV(InputForm):
    form_name = "1099-div"
    tax_year = 2021

    def __init__(self, **kwargs):
        inputs = [
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
            StringInput('box_14_1', description="State"),
            StringInput('box_14_2', description="State"),
            StringInput('box_15_1', description="State identification no."),
            StringInput('box_15_2', description="State identification no."),
            FloatInput('box_16_1', description="State tax withheld"),
            FloatInput('box_16_2', description="State tax withheld"),
        ]

        super().__init__(__class__, inputs, **kwargs)
