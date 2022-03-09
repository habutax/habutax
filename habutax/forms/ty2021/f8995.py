import os

from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *
from habutax.pdf_fields import *

class Form8995(Form):
    form_name = "8995"
    tax_year = 2021
    description = "Form 8995"
    long_description = "Qualified Business Income Deduction Simplified Computation"
    jurisdiction = Jurisdiction.US
    sequence_no = 55

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

        pdf_fields = [
            TextPDFField('topmostSubform[0].Page1[0].f1_1[0]', '1040.full_names'),
            TextPDFField('topmostSubform[0].Page1[0].f1_2[0]', '1040.you_ssn', max_length=11),
            # not implemented
#            TextPDFField('topmostSubform[0].Page1[0].Table[0].Ln1A_Row1[0].f1_3[0]', '1a_i'),
#            TextPDFField('topmostSubform[0].Page1[0].Table[0].Ln1A_Row1[0].f1_4[0]', '1b_i', max_length=11),
#            TextPDFField('topmostSubform[0].Page1[0].Table[0].Ln1A_Row1[0].f1_5[0]', '1c_i'),
#            TextPDFField('topmostSubform[0].Page1[0].Table[0].Ln1B_Row2[0].f1_6[0]', '1a_ii'),
#            TextPDFField('topmostSubform[0].Page1[0].Table[0].Ln1B_Row2[0].f1_7[0]', '1b_ii', max_length=11),
#            TextPDFField('topmostSubform[0].Page1[0].Table[0].Ln1B_Row2[0].f1_8[0]', '1c_ii'),
#            TextPDFField('topmostSubform[0].Page1[0].Table[0].Ln1C_Row3[0].f1_9[0]', '1a_iii'),
#            TextPDFField('topmostSubform[0].Page1[0].Table[0].Ln1C_Row3[0].f1_10[0]', '1b_iii', max_length=11),
#            TextPDFField('topmostSubform[0].Page1[0].Table[0].Ln1C_Row3[0].f1_11[0]', '1c_iii'),
#            TextPDFField('topmostSubform[0].Page1[0].Table[0].Ln1D_Row4[0].f1_12[0]', '1a_iv'),
#            TextPDFField('topmostSubform[0].Page1[0].Table[0].Ln1D_Row4[0].f1_13[0]', '1b_iv', max_length=11),
#            TextPDFField('topmostSubform[0].Page1[0].Table[0].Ln1D_Row4[0].f1_14[0]', '1c_iv'),
#            TextPDFField('topmostSubform[0].Page1[0].Table[0].Ln1E_Row5[0].f1_15[0]', '1a_v'),
#            TextPDFField('topmostSubform[0].Page1[0].Table[0].Ln1E_Row5[0].f1_16[0]', '1b_v', max_length=11),
#            TextPDFField('topmostSubform[0].Page1[0].Table[0].Ln1E_Row5[0].f1_17[0]', '1c_v'),
            TextPDFField('topmostSubform[0].Page1[0].ReadOrderSubForm[0].f1_18[0]', '2'),
            TextPDFField('topmostSubform[0].Page1[0].f1_19[0]', '3'),
            TextPDFField('topmostSubform[0].Page1[0].f1_20[0]', '4'),
            TextPDFField('topmostSubform[0].Page1[0].f1_21[0]', '5'),
            TextPDFField('topmostSubform[0].Page1[0].f1_22[0]', '6'),
            TextPDFField('topmostSubform[0].Page1[0].f1_23[0]', '7'),
            TextPDFField('topmostSubform[0].Page1[0].f1_24[0]', '8'),
            TextPDFField('topmostSubform[0].Page1[0].f1_25[0]', '9'),
            TextPDFField('topmostSubform[0].Page1[0].f1_26[0]', '10'),
            TextPDFField('topmostSubform[0].Page1[0].f1_27[0]', '11'),
            TextPDFField('topmostSubform[0].Page1[0].f1_28[0]', '12'),
            TextPDFField('topmostSubform[0].Page1[0].f1_29[0]', '13'),
            TextPDFField('topmostSubform[0].Page1[0].f1_30[0]', '14'),
            TextPDFField('topmostSubform[0].Page1[0].f1_31[0]', '15'),
            TextPDFField('topmostSubform[0].Page1[0].f1_32[0]', '16'),
            TextPDFField('topmostSubform[0].Page1[0].f1_33[0]', '17'),
        ]
        pdf_file = os.path.join(os.path.dirname(__file__), 'f8995.pdf')

        super().__init__(__class__, inputs, required_fields, optional_fields, pdf_fields=pdf_fields, pdf_file=pdf_file, **kwargs)

    def needs_filing(self, values):
        return True
