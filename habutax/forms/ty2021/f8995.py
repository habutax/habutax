from habutax.form import Form
from habutax.inputs import *
from habutax.fields import *

class Form8995(Form):
    form_name = "8995"
    tax_year = 2021

    def __init__(self, **kwargs):
        inputs = [
            BooleanInput('other_than_199a', description='Do you have any qualified business income (other than section 199a dividends) you need to report for this year or carryover from a previous year you need to report for qualified busiess income of REIT dividends and PTP income, or any reason you cannot claim the 199a dividends reported on your forms 1099-DIV?'),
            BooleanInput('schedule_d', description='Are you required to file schedule D?'),
        ]

        optional_fields = [
            FloatField('2', lambda s, i, v: s.not_implemented() if i['other_than_199a'] else None),
            FloatField('3', lambda s, i, v: s.not_implemented() if i['other_than_199a'] else None),
            FloatField('4', lambda s, i, v: max(0.0, v['2'] + v['3'])),
            FloatField('5', lambda s, i, v: v['4'] * 0.20),
            FloatField('6', lambda s, i, v: sum([v[f'1099-div:{n}.box_5'] for n in range(i['1040.number_1099-div'])])),
            FloatField('7', lambda s, i, v: s.not_implemented() if i['other_than_199a'] else None),
            FloatField('8', lambda s, i, v: max(0.0, v['6'] + v['7'])),
            FloatField('9', lambda s, i, v: v['8'] * 0.20),
            FloatField('10', lambda s, i, v: v['5'] + v['9']),
            FloatField('11', lambda s, i, v: v['1040.11'] - v['1040.12c']),
            FloatField('12', lambda s, i, v: v['1040.3a'] + v['1040.7'] if not i['schedule_d'] else s.not_implemented()),
            FloatField('13', lambda s, i, v: max(0.0, v['11'] - v['12'])),
            FloatField('14', lambda s, i, v: v['13'] * 0.20),
            FloatField('15', lambda s, i, v: min(v['10'], v['14'])),
        ]

        required_fields = [
            FloatField('16', lambda s, i, v: min(0.0, v['2'] + v['3'])),
            FloatField('17', lambda s, i, v: min(0.0, v['6'] + v['7'])),
        ]
        super().__init__(__class__, inputs, required_fields, optional_fields, **kwargs)
