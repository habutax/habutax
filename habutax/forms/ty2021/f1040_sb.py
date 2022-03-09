import os

from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *
from habutax.pdf_fields import *

class Form1040SB(Form):
    form_name = "1040_sb"
    tax_year = 2021
    description = "Schedule B (Form 1040)"
    long_description = "Interest and Ordinary Dividends"
    jurisdiction = Jurisdiction.US
    sequence_no = 8

    def __init__(self, **kwargs):
        NUM_FIELDS = 14
        inputs = [
            BooleanInput('excludable_us_bond_interest', description="Do you have any excludable interest on series EE and I U.S. savings bonds issued after 1989 to report?"),
            BooleanInput('financial_interest', description="At any time during 2021, did you have a financial interest in or signature authority over a financial account (such as a bank account, securities account, or brokerage account) located in a foreign country? See instructions for Form 1040, Schedule B."),
            BooleanInput('foreign_trust', description="During 2021, did you receive a distribution from, or were you the grantor of, or transferor to, a foreign trust? See instructions for Form 1040, Schedule B."),
        ]

        optional_fields = [
            FloatField('2', lambda s, i, v: sum([v[f'1_amount_{line}'] for line in range(NUM_FIELDS)])),
            FloatField('3', lambda s, i, v: s.not_implemented() if i['excludable_us_bond_interest'] else None),
            FloatField('4', lambda s, i, v: v['2'] - v['3']),
            FloatField('6', lambda s, i, v: sum([v[f'5_amount_{line}'] for line in range(NUM_FIELDS)])),
            BooleanField('7a', lambda s, i, v: s.not_implemented() if i['financial_interest'] else False),
            StringField('7b_country', lambda s, i, v: s.not_implemented() if i['financial_interest'] else None),
            BooleanField('7b', lambda s, i, v: s.not_implemented() if i['financial_interest'] else False),
            BooleanField('8', lambda s, i, v: s.not_implemented() if i['foreign_trust'] else False),
        ]

        # Because the other fields are pulled in as dependencies by Form 1040
        # when needed, and we want to allow part I and part II to be required
        # independently, add a check as a 'required field' (that will never be
        # filed) for part III, so that it is filled out when required.
        def part_3(self, i, v):
            if v['4'] > 1500.0 or v['6'] > 1500.0:
                v['7a']
                v['7b']
                v['8']
            # Also double-check that we don't have too many forms 1099-int or
            # 1099-div that we're trying to report here
            if i['1040.number_1099-int'] > NUM_FIELDS or i['1040.number_1099-div'] > NUM_FIELDS:
                self.not_implemented()
            return None

        required_fields = [
            StringField('part_3', part_3),
        ]

        for line in range(NUM_FIELDS):
            int_payer = StringField(f'1_payer_{line}', lambda s, i, v: v[f'1099-int:{s.which_1099int}.payer'] if s.which_1099int < i['1040.number_1099-int'] else None)
            int_payer.which_1099int = line
            int_amount = FloatField(f'1_amount_{line}', lambda s, i, v: v[f'1099-int:{s.which_1099int}.box_1'] + v[f'1099-int:{s.which_1099int}.box_3'] if s.which_1099int < i['1040.number_1099-int'] else None)
            int_amount.which_1099int = line
            div_payer = StringField(f'5_payer_{line}', lambda s, i, v: v[f'1099-div:{s.which_1099div}.payer'] if s.which_1099div < i['1040.number_1099-div'] else None)
            div_payer.which_1099div = line
            div_amount = FloatField(f'5_amount_{line}', lambda s, i, v: v[f'1099-div:{s.which_1099div}.box_1a'] if s.which_1099div < i['1040.number_1099-div'] else None)
            div_amount.which_1099div = line

            required_fields += [int_payer, int_amount, div_payer, div_amount]

        pdf_fields = [
            TextPDFField('topmostSubform[0].Page1[0].f1_1[0]', '1040.full_names'),
            TextPDFField('topmostSubform[0].Page1[0].f1_2[0]', '1040.you_ssn', max_length=11),
            TextPDFField('topmostSubform[0].Page1[0].f1_31[0]', '2'),
            TextPDFField('topmostSubform[0].Page1[0].f1_32[0]', '3'),
            TextPDFField('topmostSubform[0].Page1[0].f1_33[0]', '4'),
            TextPDFField('topmostSubform[0].Page1[0].f1_66[0]', '6'),
            ButtonPDFField('topmostSubform[0].Page1[0].c1_1[0]', '7a', '1'),
            ButtonPDFField('topmostSubform[0].Page1[0].c1_1[1]', '7a', '2', lambda s, v, f: not v),
            ButtonPDFField('topmostSubform[0].Page1[0].c1_2[0]', '7b', '1'),
            ButtonPDFField('topmostSubform[0].Page1[0].c1_2[1]', '7b', '2', lambda s, v, f: not v),
            TextPDFField('topmostSubform[0].Page1[0].f1_67[0]', '7b_country'),
            ButtonPDFField('topmostSubform[0].Page1[0].c1_3[0]', '8', '1'),
            ButtonPDFField('topmostSubform[0].Page1[0].c1_3[1]', '8', '2', lambda s, v, f: not v),
        ]

        for line in range(NUM_FIELDS):
            one_payer = TextPDFField(f'topmostSubform[0].Page1[0].f1_{3+line*2}[0]', f'1_payer_{line}')
            one_amt = TextPDFField(f'topmostSubform[0].Page1[0].f1_{4+line*2}[0]', f'1_amount_{line}')
            five_payer = TextPDFField(f'topmostSubform[0].Page1[0].f1_{34+line*2}[0]', f'5_payer_{line}')
            five_amt = TextPDFField(f'topmostSubform[0].Page1[0].f1_{35+line*2}[0]', f'5_amount_{line}')
            pdf_fields += [one_payer, one_amt, five_payer, five_amt]

        pdf_file = os.path.join(os.path.dirname(__file__), 'f1040sb.pdf')
        super().__init__(__class__, inputs, required_fields, optional_fields, pdf_fields=pdf_fields, pdf_file=pdf_file, **kwargs)

    def needs_filing(self, values):
        return True
