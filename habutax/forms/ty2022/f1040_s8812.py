from math import ceil
import os

from habutax.enum import filing_status
from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *
from habutax.pdf_fields import *

class Form1040S8812(Form):
    form_name = "1040_s8812"
    tax_year = 2021
    description = "Schedule 8812 (Form 1040)"
    long_description = "Credits for Qualifying Children and Other Dependents"
    jurisdiction = Jurisdiction.US
    sequence_no = 47

    def __init__(self, **kwargs):
        inputs = [
            BooleanInput('pr_income_forms_2555_4563', description="Did you exclude any income from Puerto Rico, or require Forms 2555 or 2563?"),
            IntegerInput('number_under_17', description="How many of your dependents eligible for the child tax credit with the required social security number were under age 17 with the required social security number at the end of 2022?"),
            BooleanInput('credit_limit_ws_credits', description='Are you using Schedule 3 or forms 5695, 8910, 8396, 8839, 8859 or Schedule R to report credits?'),
        ]

        def line_10(self, i, v):
            res = v['3'] - v['9']
            if res <= 0.001:
                return 0.0
            return ceil(res / 1000.0) * 1000.0

        def line_27(self, i, v):
            if not v['8_gt_11']:
                return 0.0
            if v['16a'] < 0.001:
                return 0.0
            if v['16b'] < 0.01:
                return 0.0
            return self.not_implemented("Schedule 8812 has not implemented the 'Additional Child Tax Credit for All Filers'")

        optional_fields = [
            # Part I-A: Child Tax Credit and Credit for Other Dependents
            FloatField('1', lambda s, i, v: v['1040.11']),
            FloatField('2a', lambda s, i, v: s.not_implemented() if i['pr_income_forms_2555_4563'] else None),
            FloatField('2b', lambda s, i, v: s.not_implemented() if i['pr_income_forms_2555_4563'] else None),
            FloatField('2c', lambda s, i, v: s.not_implemented() if i['pr_income_forms_2555_4563'] else None),
            FloatField('2d', lambda s, i, v: v['2a'] + v['2b'] + v['2c']),
            FloatField('3', lambda s, i, v: v['1'] + v['2d']),
            IntegerField('4', lambda s, i, v: i['number_under_17']),
            FloatField('5', lambda s, i, v: v['4'] * 2000.0),
            IntegerField('6', lambda s, i, v: sum([v[f'1040.dependent_{n}_odc'] for n in range(i['1040.number_dependents'])]) - v['4']),
            FloatField('7', lambda s, i, v: v['6'] * 500.0),
            FloatField('8', lambda s, i, v: v['5'] + v['7']),
            FloatField('9', lambda s, i, v: 400000.0 if i['1040.filing_status'] is filing_status.MarriedFilingJointly else 200000.0),
            FloatField('10', line_10),
            FloatField('11', lambda s, i, v: v['10'] * 0.05),
            BooleanField('8_gt_11', lambda s, i, v: v['8'] > v['11']),
            FloatField('12', lambda s, i, v: v['8'] - v['11'] if v['8_gt_11'] else None),
            FloatField('13', lambda s, i, v: v['clwkst_a_5']),
            FloatField('14', lambda s, i, v: min(v['12'], v['13']) if v['8_gt_11'] else 0.0),

            # Note: we are omitting most of II-A and all of II-B. The
            # implementation of line_27 checks to make sure we're not hitting
            # these cases

            # Part II-A: Additional Child Tax Credit for All Filers
            FloatField('16a', lambda s, i, v: v['12'] - v['14']),
            FloatField('16b', lambda s, i, v: v['4'] * 1500.0),
            FloatField('17', lambda s, i, v: min(v['16a'], v['16b'])),

            # Part II-C: Additional Child Tax Credit
            FloatField('27', line_27),
        ]

        optional_fields += [
            # Credit Limit Worksheet A
            FloatField('clwkst_a_1', lambda s, i, v: v['1040.18']),
            FloatField('clwkst_a_2', lambda s, i, v: s.not_implemented() if i['credit_limit_ws_credits'] else None),
            FloatField('clwkst_a_3', lambda s, i, v: s.not_implemented() if i['credit_limit_ws_credits'] else v['clwkst_a_1'] - v['clwkst_a_2']),
            FloatField('clwkst_a_4', lambda s, i, v: s.not_implemented() if i['credit_limit_ws_credits'] else 0.0),
            FloatField('clwkst_a_5', lambda s, i, v: v['clwkst_a_3'] - v['clwkst_a_4']),
        ]

        required_fields = [
            BooleanField('dependents_match', lambda s, i, v: True if sum([v[f'1040.dependent_{n}_ctc'] for n in range(i['1040.number_dependents'])]) == v['4a'] else s.not_implemented()), # TODO would be more user-friendly to be reported as some type of error rather than "not implemented"
        ]

        pdf_fields = [
            TextPDFField('topmostSubform[0].Page1[0].f1_01[0]', '1040.full_names'),
            TextPDFField('topmostSubform[0].Page1[0].f1_02[0]', '1040.you_ssn', max_length=11),
            TextPDFField('topmostSubform[0].Page1[0].f1_03[0]', '1'),
            TextPDFField('topmostSubform[0].Page1[0].f1_04[0]', '2a'),
            TextPDFField('topmostSubform[0].Page1[0].f1_05[0]', '2b'),
            TextPDFField('topmostSubform[0].Page1[0].f1_06[0]', '2c'),
            TextPDFField('topmostSubform[0].Page1[0].f1_07[0]', '2d'),
            TextPDFField('topmostSubform[0].Page1[0].f1_08[0]', '3'),
            TextPDFField('topmostSubform[0].Page1[0].f1_09[0]', '4a'),
            TextPDFField('topmostSubform[0].Page1[0].f1_10[0]', '4b'),
            TextPDFField('topmostSubform[0].Page1[0].f1_11[0]', '4c'),
            TextPDFField('topmostSubform[0].Page1[0].f1_12[0]', '5'),
            TextPDFField('topmostSubform[0].Page1[0].f1_13[0]', '6'),
            TextPDFField('topmostSubform[0].Page1[0].f1_14[0]', '7'),
            TextPDFField('topmostSubform[0].Page1[0].f1_15[0]', '8'),
            TextPDFField('topmostSubform[0].Page1[0].f1_16[0]', '9'),
            TextPDFField('topmostSubform[0].Page1[0].f1_17[0]', '10'),
            TextPDFField('topmostSubform[0].Page1[0].f1_18[0]', '11'),
            TextPDFField('topmostSubform[0].Page1[0].f1_19[0]', '12'),
            ButtonPDFField('topmostSubform[0].Page1[0].Line13_ReadOrder[0].c1_1[0]', '13a', '1'),
            ButtonPDFField('topmostSubform[0].Page1[0].Line13_ReadOrder[0].c1_2[0]', '13b', '1'),
            TextPDFField('topmostSubform[0].Page1[0].f1_20[0]', '14a'),
            TextPDFField('topmostSubform[0].Page1[0].f1_21[0]', '14b'),
            TextPDFField('topmostSubform[0].Page1[0].f1_22[0]', '14c'),
            TextPDFField('topmostSubform[0].Page1[0].f1_23[0]', '14d'),
            TextPDFField('topmostSubform[0].Page1[0].f1_24[0]', '14e'),
            TextPDFField('topmostSubform[0].Page1[0].f1_25[0]', '14f'),
            TextPDFField('topmostSubform[0].Page1[0].f1_26[0]', '14g'),
            TextPDFField('topmostSubform[0].Page1[0].f1_27[0]', '14h'),
            TextPDFField('topmostSubform[0].Page1[0].f1_28[0]', '14i'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_01[0]', '15a'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_02[0]', '15b'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_03[0]', '15c'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_04[0]', '15d'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_05[0]', '15e'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_06[0]', '15f'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_07[0]', '15g'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_08[0]', '15h'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_09[0]', '16a'),
#            TextPDFField('topmostSubform[0].Page2[0].Line16b_ReadOrder[0].f2_10[0]', '16b_num_qualifying_children'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_11[0]', '16b'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_12[0]', '17'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_13[0]', '18a'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_14[0]', '18b'),
#            ButtonPDFField('topmostSubform[0].Page2[0].c2_1[0]', '19_no', '1'),
#            ButtonPDFField('topmostSubform[0].Page2[0].c2_1[1]', '19_yes', '2'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_15[0]', '19'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_16[0]', '20'),
#            ButtonPDFField('topmostSubform[0].Page2[0].c2_2[0]', '20_no', '1'),
#            ButtonPDFField('topmostSubform[0].Page2[0].c2_2[1]', '20_yes', '2'),
#            TextPDFField('topmostSubform[0].Page2[0].Line21_ReadOrder[0].f2_17[0]', '21'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_18[0]', '22'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_19[0]', '23'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_20[0]', '24'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_21[0]', '25'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_22[0]', '26'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_23[0]', '27'),
            TextPDFField('topmostSubform[0].Page3[0].f3_01[0]', '28a'),
            TextPDFField('topmostSubform[0].Page3[0].f3_02[0]', '28b'),
            TextPDFField('topmostSubform[0].Page3[0].f3_03[0]', '29'),
            TextPDFField('topmostSubform[0].Page3[0].f3_04[0]', '30'),
            TextPDFField('topmostSubform[0].Page3[0].f3_05[0]', '31'),
            TextPDFField('topmostSubform[0].Page3[0].f3_06[0]', '32'),
            TextPDFField('topmostSubform[0].Page3[0].f3_07[0]', '33'),
            TextPDFField('topmostSubform[0].Page3[0].f3_08[0]', '34'),
            TextPDFField('topmostSubform[0].Page3[0].f3_09[0]', '35'),
            TextPDFField('topmostSubform[0].Page3[0].f3_10[0]', '36'),
            TextPDFField('topmostSubform[0].Page3[0].f3_11[0]', '37'),
            TextPDFField('topmostSubform[0].Page3[0].f3_12[0]', '38'),
            TextPDFField('topmostSubform[0].Page3[0].f3_13[0]', '39'),
            TextPDFField('topmostSubform[0].Page3[0].f3_14[0]', '40'),
        ]

        pdf_file = os.path.join(os.path.dirname(__file__), 'f1040s8.pdf')
        super().__init__(__class__, inputs, required_fields, optional_fields, pdf_fields=pdf_fields, pdf_file=pdf_file, **kwargs)

    def needs_filing(self, values):
        return True