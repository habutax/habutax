import habutax.enum as enum
from habutax.form import InputForm, Jurisdiction
from habutax.inputs import *

class Form1099G(InputForm):
    form_name = "1099-g"
    tax_year = 2021
    description = "Form 1099-G"
    long_description = "Certain Government Payments"
    jurisdiction = Jurisdiction.US

    def __init__(self, **kwargs):
        inputs = [
            EnumInput('belongs_to', enum.taxpayer_spouse_or_both, description="To whom does this 1099-G belong?"),
            StringInput('payer', description="Who paid you this amount?"),
            StringInput('recipient', description="To whom was this amount paid? (you or your spouse's name)"),
            FloatInput('box_1', description="Unemployment compensation"),
            FloatInput('box_2', description="State income tax refund, credit or offset"),
            IntegerInput('box_3', description="Refund (box 2 amount) is for tax year"),
            FloatInput('box_4', description="Federal income tax withheld"),
            FloatInput('box_5', description="RTAA payments"),
            FloatInput('box_6', description="Taxable grants"),
            FloatInput('box_7', description="Agriculture payments"),
            BooleanInput('box_8', description="Is box 2 is trade or business income?"),
            FloatInput('box_9', description="Market gain"),
            EnumInput('box_10a_1', enum.us_states, allow_empty=True, description="State #1"),
            StringInput('box_10b_1', description="State #1 identification no."),
            FloatInput('box_11_1', description="State #1 tax withheld"),
            EnumInput('box_10a_2', enum.us_states, allow_empty=True, description="State #2"),
            StringInput('box_10b_2', description="State #2 identification no."),
            FloatInput('box_11_2', description="State #2 tax withheld"),
        ]

        super().__init__(__class__, inputs, **kwargs)
