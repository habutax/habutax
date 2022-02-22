from habutax.form import Form
from habutax.inputs import *
from habutax.fields import *

class Form1040SB(Form):
    form_name = "1040_sb"
    tax_year = 2021

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
            BooleanField('7b', lambda s, i, v: s.not_implemented() if i['financial_interest'] else None),
            BooleanField('8', lambda s, i, v: s.not_implemented() if i['foreign_trust'] else False),
        ]

        for line in range(NUM_FIELDS):
            int_payer = StringField(f'1_payer_{line}', lambda s, i, v: v[f'1099-int:{s.which_1099int}.payer'] if s.which_1099int < i['1040.number_1099-int'] else None)
            int_payer.which_1099int = line
            int_amount = FloatField(f'1_amount_{line}', lambda s, i, v: v[f'1099-int:{s.which_1099int}.box_1'] if s.which_1099int < i['1040.number_1099-int'] else None)
            int_amount.which_1099int = line
            div_payer = StringField(f'5_payer_{line}', lambda s, i, v: v[f'1099-div:{s.which_1099div}.payer'] if s.which_1099div < i['1040.number_1099-div'] else None)
            div_payer.which_1099div = line
            div_amount = FloatField(f'5_amount_{line}', lambda s, i, v: v[f'1099-div:{s.which_1099div}.box_1a'] if s.which_1099div < i['1040.number_1099-div'] else None)
            div_amount.which_1099div = line

            optional_fields += [int_payer, int_amount, div_payer, div_amount]

        # This is the only required field. Because the others are pulled in as
        # dependencies by Form 1040 when needed, and we want to allow part I
        # and part II to be required independently, add a check as a 'required
        # field' (that will never be filed) for part III, so that it is filled
        # out when required.
        def part_3(self, i, v):
            if v['4'] > 1500.0 or v['6'] > 1500.0:
                v['7a']
                v['7b']
                v['8']
            # Also double-check that we don't have too many forms 1099-int or
            # 1099-div that we're trying to report here
            if v['1040.number_1099-int'] > NUM_FIELDS or v['1040.number_1099-div'] > NUM_FIELDS:
                self.not_implemented()
            return None
        part_3_required = StringField('part_3', part_3)

        super().__init__(__class__, inputs, [part_3_required], optional_fields, **kwargs)
