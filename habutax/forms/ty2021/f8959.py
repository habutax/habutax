import os

from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *
from habutax.pdf_fields import *

class Form8959(Form):
    form_name = "8959"
    tax_year = 2021
    description = "Form 8959"
    long_description = "Additional Medicare Tax"
    jurisdiction = Jurisdiction.US
    sequence_no = 71

    def __init__(self, **kwargs):
        inputs = [
            BooleanInput('other_medicare_income', description="Do you have any unreported tip income (Form 4137, line 6) or wages on which medicare tax was not withheld? (this is not common)"),
        ]
        def additional_medicare_threshold(self, i, v):
            statuses = self.form('1040').FILING_STATUS
            threshold = 200000.0
            if i['1040.filing_status'] is statuses.MarriedFilingJointly:
                threshold = 250000.0
            elif i['1040.filing_status'] is statuses.MarriedFilingSeparately:
                threshold = 125000.0
            return threshold

        required_fields = [
            # Part I - Additional Medicare Tax on Medicare Wages
            FloatField('1', lambda s, i, v: float(sum([v[f'w-2:{n}.box_5'] for n in range(i['1040.number_w-2'])]))),
            FloatField('2', lambda s, i, v: s.not_implemented() if i['other_medicare_income'] else None),
            FloatField('3', lambda s, i, v: s.not_implemented() if i['other_medicare_income'] else None),
            FloatField('4', lambda s, i, v: v['1'] + v['2'] + v['3']),
            FloatField('5', additional_medicare_threshold),
            FloatField('6', lambda s, i, v: max(0.0, v['4'] - v['5'])),
            FloatField('7', lambda s, i, v: v['6'] * 0.009),
        ]

        optional_fields = [
            # Part II - Additional Medicare Tax on Self-Employment Income
            FloatField('8', lambda s, i, v: s.not_implmented() if i['1040.self_employment_income'] else None),
            FloatField('9', additional_medicare_threshold),
            FloatField('10', lambda s, i, v: v['4']),
            FloatField('11', lambda s, i, v: max(0.0, v['9'] - v['10'])),
            FloatField('12', lambda s, i, v: max(0.0, v['8'] - v['11'])),
            FloatField('13', lambda s, i, v: v['12'] * 0.009),

            # Part III - Additional Medicare Tax on  Railroad Retirement Tax Act (RRTA) Compensation
            FloatField('14', lambda s, i, v: s.not_implmented() if i['1040.rrta_compensation'] else None),
            FloatField('15', additional_medicare_threshold),
            FloatField('16', lambda s, i, v: max(0.0, v['14'] - v['15'])),
            FloatField('17', lambda s, i, v: v['16'] * 0.009),

            # Part IV - Total Additional Medicare Tax
            FloatField('18', lambda s, i, v: v['7'] + v['13'] + v['17']),

            # Part V - Withholding Reconcilation
            FloatField('19', lambda s, i, v: float(sum([v[f'w-2:{n}.box_6'] for n in range(i['1040.number_w-2'])]))),
            FloatField('20', lambda s, i, v: v['1']),
            FloatField('21', lambda s, i, v: v['20'] * 0.0145),
            FloatField('22', lambda s, i, v: max(0.0, v['19'] - v['21'])),
            FloatField('23', lambda s, i, v: s.not_implmented() if i['1040.rrta_compensation'] else None),
            FloatField('24', lambda s, i, v: v['22'] + v['23']),
        ]

        pdf_fields = [
            TextPDFField('topmostSubform[0].Page1[0].f1_1[0]', '1040.full_names'),
            TextPDFField('topmostSubform[0].Page1[0].f1_2[0]', '1040.you_ssn', max_length=11),
            TextPDFField('topmostSubform[0].Page1[0].f1_3[0]', '1'),
            TextPDFField('topmostSubform[0].Page1[0].f1_4[0]', '2'),
            TextPDFField('topmostSubform[0].Page1[0].f1_5[0]', '3'),
            TextPDFField('topmostSubform[0].Page1[0].f1_6[0]', '4'),
            TextPDFField('topmostSubform[0].Page1[0].f1_7[0]', '5'),
            TextPDFField('topmostSubform[0].Page1[0].f1_8[0]', '6'),
            TextPDFField('topmostSubform[0].Page1[0].f1_9[0]', '7'),
            TextPDFField('topmostSubform[0].Page1[0].f1_10[0]', '8'),
            TextPDFField('topmostSubform[0].Page1[0].f1_11[0]', '9'),
            TextPDFField('topmostSubform[0].Page1[0].f1_12[0]', '10'),
            TextPDFField('topmostSubform[0].Page1[0].f1_13[0]', '11'),
            TextPDFField('topmostSubform[0].Page1[0].f1_14[0]', '12'),
            TextPDFField('topmostSubform[0].Page1[0].f1_15[0]', '13'),
            TextPDFField('topmostSubform[0].Page1[0].f1_16[0]', '14'),
            TextPDFField('topmostSubform[0].Page1[0].f1_17[0]', '15'),
            TextPDFField('topmostSubform[0].Page1[0].f1_18[0]', '16'),
            TextPDFField('topmostSubform[0].Page1[0].f1_19[0]', '17'),
            TextPDFField('topmostSubform[0].Page1[0].f1_20[0]', '18'),
            TextPDFField('topmostSubform[0].Page1[0].f1_21[0]', '19'),
            TextPDFField('topmostSubform[0].Page1[0].f1_22[0]', '20'),
            TextPDFField('topmostSubform[0].Page1[0].f1_23[0]', '21'),
            TextPDFField('topmostSubform[0].Page1[0].f1_24[0]', '22'),
            TextPDFField('topmostSubform[0].Page1[0].f1_25[0]', '23'),
            TextPDFField('topmostSubform[0].Page1[0].f1_26[0]', '24'),
        ]
        pdf_file = os.path.join(os.path.dirname(__file__), 'f8959.pdf')

        super().__init__(__class__, inputs, required_fields, optional_fields, pdf_fields=pdf_fields, pdf_file=pdf_file, **kwargs)

    def needs_filing(self, values):
        return True
