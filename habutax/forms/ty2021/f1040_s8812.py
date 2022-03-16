from math import ceil
import os

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
            IntegerInput('number_under_18', description="How many of your dependents eligible for the child tax credit with the required social security number were under age 18 at the end of 2021?"),
            IntegerInput('number_under_6', description="How many of your dependents eligible for the child tax credit with the required social security number were under age 6 at the end of 2021?"),
            BooleanInput('principal_abode_us', description="Did you (or your spouse if married filing jointly) have a principal place of abode in the United States for more than half of 2021?"),
            BooleanInput('resident_puerto_rico', description="Were you (or your spouse of married filing jointly) a bona fide resident of Puerto Rico for 2021?"),
            FloatInput('advance_ctc_payments', description="Enter the aggregate amount of advance child tax credit payments you (and your spouse if filing jointly) received for 2021. See your Letter(s) 6419 for the amounts to include)"),
            BooleanInput('credit_limit_ws_credits', description='Are you using Schedule 3 to report any nonrefundable credits, Forms 5695, 8910, 8936, or Schedule R?'),
            IntegerInput('number_children_letter', description="Enter the number of qualifying children taken into account in determining the annual advance child tax credit amount you received for 2021. See your Letter 6419 for this number. If you are missing your Letter 6419, you are filing a joint return, or you received more than one Letter 6419, see the instructions before entering a number"),
        ]

        def line_5_ws_6(self, i, v):
            statuses = self.form('1040').FILING_STATUS
            if i['1040.filing_status'] is statuses.MarriedFilingJointly:
                return 12500.0
            elif i['1040.filing_status'] is statuses.QualifyingWidowWidower:
                return 2500.0
            elif i['1040.filing_status'] is statuses.HeadOfHousehold:
                return 4375.0
            else:
                return 6250.0

        def line_5_ws_8(self, i, v):
            statuses = self.form('1040').FILING_STATUS
            if i['1040.filing_status'] in [statuses.MarriedFilingJointly, statuses.QualifyingWidowWidower]:
                return 150000.0
            elif i['1040.filing_status'] is statuses.HeadOfHousehold:
                return 112500.0
            else:
                return 75000.0

        def line_5_ws_9(self, i, v):
            res = v['3'] - v['5_ws_8']
            if res <= 0.001:
                return 0.0
            return ceil(res / 1000.0) * 1000.0

        def line_10(self, i, v):
            res = v['3'] - v['9']
            if res <= 0.001:
                return 0.0
            return ceil(res / 1000.0) * 1000.0

        def line_33(self, i, v):
            statuses = self.form('1040').FILING_STATUS
            if i['1040.filing_status'] in [statuses.MarriedFilingJointly, statuses.QualifyingWidowWidower]:
                return 60000.0
            elif i['1040.filing_status'] is statuses.HeadOfHousehold:
                return 50000.0
            else:
                return 40000.0

        def line_40(self, i, v):
            if v['32'] < 0.001 and v['32'] > -0.001:
                return v['29']
            return max(0.0, v['29'] - v['39'])

        def additional_tax(self, i, v):
            if v['29'] < 0.001 and v['29'] > -0.001:
                return 0.0
            return v['40']

        optional_fields = [
            # Part I-A: Child Tax Credit and Credit for Other Dependents
            FloatField('1', lambda s, i, v: v['1040.11']),
            FloatField('2a', lambda s, i, v: s.not_implemented() if i['pr_income_forms_2555_4563'] else None),
            FloatField('2b', lambda s, i, v: s.not_implemented() if i['pr_income_forms_2555_4563'] else None),
            FloatField('2c', lambda s, i, v: s.not_implemented() if i['pr_income_forms_2555_4563'] else None),
            FloatField('2d', lambda s, i, v: v['2a'] + v['2b'] + v['2c']),
            FloatField('3', lambda s, i, v: v['1'] + v['2d']),
            IntegerField('4a', lambda s, i, v: i['number_under_18']),
            IntegerField('4b', lambda s, i, v: i['number_under_6']),
            IntegerField('4c', lambda s, i, v: v['4a'] - v['4b']),
            FloatField('5', lambda s, i, v: v['5_ws_12'] if v['4a'] > 0 else 0.0),
            IntegerField('6', lambda s, i, v: sum([v[f'1040.dependent_{n}_odc'] for n in range(i['1040.number_dependents'])])),
            FloatField('7', lambda s, i, v: v['6'] * 500.0),
            FloatField('8', lambda s, i, v: v['5'] + v['7']),
            FloatField('9', lambda s, i, v: 400000.0 if i['1040.filing_status'] is s.form('1040').FILING_STATUS.MarriedFilingJointly else 200000.0),
            FloatField('10', line_10),
            FloatField('11', lambda s, i, v: v['10'] * 0.05),
            FloatField('12', lambda s, i, v: max(0.0, v['8'] - v['11'])),
            BooleanField('13a', lambda s, i, v: i['principal_abode_us']),
            BooleanField('13b', lambda s, i, v: i['resident_puerto_rico']),

            # Part I-B: Filers Who Check a Box on Line 13
            FloatField('14a', lambda s, i, v: min(v['7'], v['12'])),
            FloatField('14b', lambda s, i, v: v['12'] -  v['14a']),
            FloatField('14c', lambda s, i, v: 0.0 if v['14a'] < 0.001 else v['clwkst_a_5']),
            FloatField('14d', lambda s, i, v: min(v['14a'], v['14c'])),
            FloatField('14e', lambda s, i, v: v['14b'] + v['14d']),
            FloatField('14f', lambda s, i, v: i['advance_ctc_payments']),
            FloatField('14g', lambda s, i, v: max(0.0, v['14e'] - v['14f'])),
            FloatField('14h', lambda s, i, v: 0.0 if v['14g'] < 0.001 else min(v['14d'], v['14g'])),
            FloatField('14i', lambda s, i, v: 0.0 if v['14g'] < 0.001 else v['14g'] - v['14h']),

            FloatField('nonrefundable_ctc_or_odc', lambda s, i, v: v['14h'] if v['13a'] or v['13b'] else s.not_implemented()), # -> Form 1040, line 19
            FloatField('refundable_ctc_or_additional_ctc', lambda s, i, v: v['14i'] if v['13a'] or v['13b'] else s.not_implemented()), # -> Form 1040, line 28

            # Omitting Parts I-C, II-A, II-B, II-C - they are only used if you did *not* check a box on line 13
            FloatField('28a', lambda s, i, v: v['14f'] if v['13a'] or v['13b'] else v['15e']),
            FloatField('28b', lambda s, i, v: v['14e'] if v['13a'] or v['13b'] else v['15d']),
            FloatField('29', lambda s, i, v: v['28a'] - v['28b']),

            IntegerField('30', lambda s, i, v: i['number_children_letter']),
            IntegerField('31', lambda s, i, v: min(v['4a'], v['30'])),
            IntegerField('32', lambda s, i, v: v['30'] - v['31']),
            FloatField('33', line_33),
            FloatField('34', lambda s, i, v: max(0.0, v['3'] - v['33'])),
            FloatField('35', lambda s, i, v: v['33']),
            FloatField('36', lambda s, i, v: ceil((v['34'] / v['35']) / 1000.0) * 1000.0),
            FloatField('37', lambda s, i, v: v['32'] * 2000),
            FloatField('38', lambda s, i, v: v['37'] * v['36']),
            FloatField('39', lambda s, i, v: v['37'] - v['38']),
            FloatField('40', line_40),
            FloatField('additional_tax', additional_tax), # -> Schedule 2 (Form 1040), line 19
        ]

        optional_fields += [
            # Line 5 Worksheet from Schedule 8812 instructions
            FloatField('5_ws_1', lambda s, i, v: v['4b'] * 3600.0),
            FloatField('5_ws_2', lambda s, i, v: v['4c'] * 3000.0),
            FloatField('5_ws_3', lambda s, i, v: v['5_ws_1'] + v['5_ws_2']),
            FloatField('5_ws_4', lambda s, i, v: v['4a'] * 2000.0),
            FloatField('5_ws_5', lambda s, i, v: v['5_ws_3'] - v['5_ws_4']),
            FloatField('5_ws_6', line_5_ws_6),
            FloatField('5_ws_7', lambda s, i, v: min(v['5_ws_5'], v['5_ws_6'])),
            FloatField('5_ws_8', line_5_ws_8),
            FloatField('5_ws_9', line_5_ws_9),
            FloatField('5_ws_10', lambda s, i, v: v['5_ws_9'] * 0.05),
            FloatField('5_ws_11', lambda s, i, v: min(v['5_ws_7'], v['5_ws_10'])),
            FloatField('5_ws_12', lambda s, i, v: v['5_ws_3'] - v['5_ws_11']),

            # Credit Limit Worksheet A
            FloatField('clwkst_a_1', lambda s, i, v: v['1040.18']),
            FloatField('clwkst_a_2', lambda s, i, v: s.not_implemented() if i['credit_limit_ws_credits'] else None),
            FloatField('clwkst_a_3', lambda s, i, v: s.not_implemented() if not v['13a'] and not v['13b'] else v['clwkst_a_1'] - v['clwkst_a_2']),
            FloatField('clwkst_a_4', lambda s, i, v: s.not_implemented() if not v['13a'] and not v['13b'] else 0.0),
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
            TextPDFField('topmostSubform[0].Page1[0].f1_27[0]', '14b'),
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
