from math import ceil
import os

from habutax.enum import filing_status
from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *
from habutax.pdf_fields import *


class Form1040S8812(Form):
    form_name = "1040_s8812"
    tax_year = 2023
    description = "Schedule 8812 (Form 1040)"
    long_description = "Credits for Qualifying Children and Other Dependents"
    jurisdiction = Jurisdiction.US
    sequence_no = 47

    def __init__(self, **kwargs):
        thresholds = {
            # Form 1040, Schedule 8812, line 9 instructions
            '9_amount': {
                filing_status.MarriedFilingJointly: 400000.0,
                (filing_status.Single, filing_status.MarriedFilingSeparately,
                 filing_status.QualifyingSurvivingSpouse,
                 filing_status.HeadOfHousehold): 200000.0,
            },
            # Form 1040, Schedule 8812, line 16b instructions
            'max_additional_child_tax_credit': 1600.0,
            # Form 1040, Schedule 8812, line 20 instructions
            '20_comparison': 4800.0,
        }

        inputs = [
            BooleanInput('pr_income_forms_2555_4563', description="Did you exclude any income from Puerto Rico, or require Forms 2555 or 2563?"),
            IntegerInput('number_under_17', description="How many of your dependents eligible for the child tax credit with the required social security number were under age 17 with the required social security number at the end of 2023?"),
            BooleanInput('credit_limit_ws_b_maybe_needed', description='Are you using forms 5695, 8396, 8839, 8859 to report credits?'),
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
            IntegerField('6', lambda s, i, v: sum([v[f'1040.dependent_{n}_odc'] for n in range(i['1040.number_dependents'])])),
            FloatField('7', lambda s, i, v: v['6'] * 500.0),
            FloatField('8', lambda s, i, v: v['5'] + v['7']),
            FloatField('9', lambda s, i, v: s.threshold('9_amount', i['1040.filing_status'])),
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
            FloatField('16b', lambda s, i, v: v['4'] * s.threshold('max_additional_child_tax_credit')),
            FloatField('17', lambda s, i, v: min(v['16a'], v['16b'])),

            # Part II-C: Additional Child Tax Credit
            FloatField('27', line_27),
        ]

        def line_clwkst_a_2(self, i, v):
            if not v['1040.need_schedule_3_part_i']:
                return None

            if i['1040_s3.residential_energy_credit']:
                self.not_implemented()

            amounts = sum([v[f'1040_s3.{l}'] for l in ['1', '2', '3', '4', '6d', '6e', '6f', '6l']])
            return None if amounts < 0.001 else amounts

        optional_fields += [
            # Credit Limit Worksheet A
            FloatField('clwkst_a_1', lambda s, i, v: v['1040.18']),
            FloatField('clwkst_a_2', line_clwkst_a_2),
            FloatField('clwkst_a_3', lambda s, i, v: v['clwkst_a_1'] - v['clwkst_a_2']),
            FloatField('clwkst_a_4', lambda s, i, v: s.not_implemented() if i['credit_limit_ws_b_maybe_needed'] else 0.0),
            FloatField('clwkst_a_5', lambda s, i, v: v['clwkst_a_3'] - v['clwkst_a_4']),
        ]

        required_fields = [
            BooleanField('dependents_match', lambda s, i, v: True if sum([v[f'1040.dependent_{n}_ctc'] for n in range(i['1040.number_dependents'])]) == v['4'] else s.not_implemented()), # TODO would be more user-friendly to be reported as some type of error rather than "not implemented"
        ]

        pdf_fields = [
            TextPDFField('topmostSubform[0].Page1[0].f1_1[0]', '1040.full_names'),
            TextPDFField('topmostSubform[0].Page1[0].f1_2[0]', '1040.you_ssn', max_length=11),
            TextPDFField('topmostSubform[0].Page1[0].f1_3[0]', '1'),
            TextPDFField('topmostSubform[0].Page1[0].f1_4[0]', '2a'),
            TextPDFField('topmostSubform[0].Page1[0].f1_5[0]', '2b'),
            TextPDFField('topmostSubform[0].Page1[0].f1_6[0]', '2c'),
            TextPDFField('topmostSubform[0].Page1[0].f1_7[0]', '2d'),
            TextPDFField('topmostSubform[0].Page1[0].f1_8[0]', '3'),
            TextPDFField('topmostSubform[0].Page1[0].f1_9[0]', '4'),
            TextPDFField('topmostSubform[0].Page1[0].f1_10[0]', '5'),
            TextPDFField('topmostSubform[0].Page1[0].Line6ReadOrder[0].f1_11[0]', '6'),
            TextPDFField('topmostSubform[0].Page1[0].f1_12[0]', '7'),
            TextPDFField('topmostSubform[0].Page1[0].f1_13[0]', '8'),
            TextPDFField('topmostSubform[0].Page1[0].f1_14[0]', '9'),
            TextPDFField('topmostSubform[0].Page1[0].f1_15[0]', '10'),
            TextPDFField('topmostSubform[0].Page1[0].f1_16[0]', '11'),
            TextPDFField('topmostSubform[0].Page1[0].f1_17[0]', '12'),
            ButtonPDFField('topmostSubform[0].Page1[0].c1_1[0]', '8_gt_11', '1', lambda s, v, f: not v),
            ButtonPDFField('topmostSubform[0].Page1[0].c1_1[1]', '8_gt_11', '2', lambda s, v, f: v),
            TextPDFField('topmostSubform[0].Page1[0].f1_18[0]', '13'),
            TextPDFField('topmostSubform[0].Page1[0].f1_19[0]', '14'),
#            ButtonPDFField('topmostSubform[0].Page2[0].c2_1[0]', 'do_not_want_to_claim_additional_ctc', '1'),
            TextPDFField('topmostSubform[0].Page2[0].f2_1[0]', '16a'),
            TextPDFField('topmostSubform[0].Page2[0].f2_2[0]', '4'), # number of qualifying children for 16b
            TextPDFField('topmostSubform[0].Page2[0].f2_3[0]', '16b'),
            TextPDFField('topmostSubform[0].Page2[0].f2_4[0]', '17'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_5[0]', '18a'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_6[0]', '18b'),
#            ButtonPDFField('topmostSubform[0].Page2[0].c2_2[0]', 'unknown', '1'),
#            ButtonPDFField('topmostSubform[0].Page2[0].c2_2[1]', 'unknown', '2'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_7[0]', '19'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_8[0]', '20'),
#            ButtonPDFField('topmostSubform[0].Page2[0].c2_3[0]', 'unknown', '1'),
#            ButtonPDFField('topmostSubform[0].Page2[0].c2_3[1]', 'unknown', '2'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_9[0]', '21'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_10[0]', '22'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_11[0]', '23'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_12[0]', '24'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_13[0]', '25'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_14[0]', '26'),
            TextPDFField('topmostSubform[0].Page2[0].f2_15[0]', '27'),
        ]

        pdf_file = os.path.join(os.path.dirname(__file__), 'f1040s8.pdf')
        super().__init__(__class__, inputs, required_fields, optional_fields,
                         thresholds=thresholds, pdf_fields=pdf_fields,
                         pdf_file=pdf_file, **kwargs)

    def needs_filing(self, values):
        return True
