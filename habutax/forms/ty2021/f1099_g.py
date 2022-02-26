from habutax.form import InputForm
from habutax.inputs import *

class Form1099G(InputForm):
    form_name = "1099-g"
    tax_year = 2021

    def __init__(self, **kwargs):
        inputs = [
            IntegerInput('box_1', description="Refund is for tax year"),
            StringInput('box_2', description="Recipient's identifying number(s)"),
            FloatInput('box_3', description="State income tax refund, credit or offset"),
        ]

        super().__init__(__class__, inputs, **kwargs)
