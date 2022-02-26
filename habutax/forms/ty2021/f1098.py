from habutax.form import InputForm
from habutax.inputs import *

class Form1098(InputForm):
    form_name = "1098"
    tax_year = 2021

    def __init__(self, **kwargs):
        inputs = [
            StringInput('recipient_lender_name', description="Recipient/Lender's name: To whom did you pay this mortgage interest?"),
            StringInput('payer_borrower', description="Payer/Borrower: Name of borrower who paid the interest"),
            FloatInput('box_1', description="Mortgage interest received from payer(s)/borrower(s)"),
            FloatInput('box_2', description="Outstanding mortgage principal"),
            StringInput('box_3', description="Mortgage origination date"),
            FloatInput('box_4', description="Refund of overpaid interest"),
            FloatInput('box_5', description="Mortgage insurance premiums"),
            FloatInput('box_6', description="Points paid on purchase of principal residence"),
            BooleanInput('box_7', description="Is the checkbox on box 7 checked?"),
            StringInput('box_8', description="Address or description of proprety securing mortgage"),
            IntegerInput('box_9', description="Number of properties securint the mortgage"),
            FloatInput('box_10', description="Other"),
            StringInput('box_11', description="Mortgage acquisition date"),
        ]

        super().__init__(__class__, inputs, **kwargs)
