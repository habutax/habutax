import os

from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *
from habutax.pdf_fields import *

class Form1040SA(Form):
    form_name = "1040_sa"
    tax_year = 2021
    description = "Schedule A (Form 1040)"
    long_description = "Itemized Deductions"
    jurisdiction = Jurisdiction.US
    sequence_no = 7

    def __init__(self, **kwargs):
        inputs = [
            BooleanInput('itemize_though_less', description="Do you want to itemize deductions even though they are less than your standard deduction?"),
            FloatInput('medical_dental_expenses', description="Enter the total amount of medical and dental expenses you are allowed to deduct for 2021. This can include insurance premiums for medical and dental care, prescription medicines or insulin, medical specialists, examinations, or other medical care. See the instructions for Form 1040, Schedule A for a detailed explanation of the limitations and restrictions"),
            BooleanInput('general_sales_tax', description="Do you want to deduct general sales tax instead of state and local income tax? (You must choose one, and choosing to deduct general sales tax means your return is not supported by Habutax)"),
            FloatInput('state_local_real_estate_taxes', description="Enter the sum of any state and local taxes you paid in 2021 (either directly or through your mortgage company) on real estate you own that wasn't used for business. See instructions for Form 1040, Schedule A, line 5b for details of what can and cannot be claimed."),
            FloatInput('state_local_personal_property_taxes', description="Enter the sum of any state and local personal property taxes you paid in 2021, but only if the taxes were based on value alone and were imposed on a yearly basis. If you paid a yearly fee for the registration of your car and part of that fee was based on the car's value and part was based on its weight, you can deduct only the part of the fee that was based on the car's value."),
            FloatInput('other_taxes_amount', description="Enter the total amount of any 'other taxes' you want to deduct. You may include income taxes you paid to a foreign country and generation skipping tax (GST) imposed on certain income distributions, but you may want to take a credit for the foreign tax instead of a deduction. See the instructions for Schedule 3 (Form 1040), line 1, for details."),
            StringInput('other_taxes_type', description="Enter the 'type' of each 'other taxes' you are deducting."),
            BooleanInput('loan_limitations', description="Do you have mortgage loans taken out after October 13, 1987, that exceed $750,000 ($375,000 if you are married filing separately, loans exceeding the fair market value of the home, or loan proceeds not used to buy, build, or substantially improve your home?"),
            FloatInput('other_mortgage_interest', description="Enter any home mortgage interest not reported to you on Form 1098."),
            StringInput('other_mortgage_interest_desc', description="If the home interest you are claiming that was not reported to you on 1098 was paid to the person from whom you bought the home, see instructions and enter that person’s name, identifying no., and address here"),
            FloatInput('other_mortgage_points', description="Enter any home mortgage points not reported to you on Form 1098. Limits may apply, see Pub. 936 for details."),
            BooleanInput('mortgage_insurance_premiums_special', description="Did you share the costs for mortgage insurance premiums reported on form 1098 with someone (other than your spouse if married filing jointly), or pay mortgage insurance premiums in 2021 for a year other than 2021?"),
            BooleanInput('investment_interest', description="Did you pay interest on money you borrowed that is allocable to property held for investment in 2021?"),
            FloatInput('charitable_cash_check', description="Enter the total amount of all charitable gifts to Qualified Charitable Organizations you made in 2021 via cash or check. Ensure you have (and save for your records) contempotaneous written acknowledgement of any individual gift over $250. See the instructions for line 11 of Form 1040, Schedule A if you have any questions."),
            FloatInput('charitable_other_than_cash_check', description="Enter the total amount of all charitable gifts to Qualified Charitable Organizations you made in 2021 via methods *other than* cash or check. Ensure you have (and save for your records) contempotaneous written acknowledgement of any individual gift over $250. See the instructions for line 12 of Form 1040, Schedule A and/or Pub. 526 if you have any questions."),
            BooleanInput('filling_8283', description="You indicated you gave total noncash charitable gifts of over $500 in 2021. You must file one or more Forms 8283 if the amount of your deduction for each noncash contribution is more than $500. You must also file Form 8283 if you have a group of similar items for which a total deduction of over $500 is claimed. Do you agree to fill out Form(s) 8283 as appropriate and include them with your tax return (you will *not* be reminded again)? See the instructions for line 12 of Form 1040, Schedule A and Pub. 526."),
            FloatInput('charitable_carryover', description="Enter any carryover for any charitable giving you were not allowed to deduct in the previous 5 years because it exceeded the amount you were allowed to decuct. See the instructions for line 12 of Form 1040, Schedule A and Pub. 526."),
            BooleanInput('casualty_theft', description="Do you have any casualty and theft loss(es) from a federally declared disaster (other than net qualified disaster losses) to report?"),
            FloatInput('other_itemized', description="Enter the amount of any other itemized deductions you want to claim. See instructions for Form 1040, Schedule A, line 13"),
            StringInput('other_itemized_type', description="Enter the type of any other itemized deductions you are claiming. See instructions for Form 1040, Schedule A, line 13"),
        ]

        def line_5a(self, i, v):
            # TODO If we implement Schedules C, E, or F, we must reduce the
            # amount calculated here by any amounts of these withheld taxes
            # which are deducted on one of those forms (or elsewhere)
            state_local_income_taxes = sum(v[f'w-2:{n}.box_17'] + v[f'w-2:{n}.box_19'] for n in range(i['1040.number_w-2']))
            state_local_income_taxes += sum(v[f'1099-div:{n}.box_16_1'] + v[f'1099-div:{n}.box_16_2'] for n in range(i['1040.number_1099-div']))
            state_local_income_taxes += sum(v[f'1099-int:{n}.box_17_1'] + v[f'1099-int:{n}.box_17_2'] for n in range(i['1040.number_1099-int']))
            state_local_income_taxes += sum(v[f'1099-r:{n}.box_14_1'] + v[f'1099-r:{n}.box_14_2'] + v[f'1099-r:{n}.box_17_1'] + v[f'1099-r:{n}.box_17_2'] for n in range(i['1040.number_1099-r']))
            return state_local_income_taxes

        def line_8a(self, i, v):
            mortgage_interest_points = sum([v[f'1098:{n}.box_1'] for n in range(i['1040.number_1098'])])
            mortgage_interest_points += sum([v[f'1098:{n}.box_6'] for n in range(i['1040.number_1098'])])
            if mortgage_interest_points > 0.001 and i['loan_limitations']:
                self.not_implemented()
            return mortgage_interest_points

        def line_8d(self, i, v):
            mortgage_insurance_premiums = sum([v[f'1098:{n}.box_5'] for n in range(i['1040.number_1098'])])
            if mortgage_insurance_premiums < 0.001:
                return None
            premium_limit = 50000 if i['1040.filing_status'] == self.form('1040').FILING_STATUS.MarriedFilingSeparately else 100000
            if mortgage_insurance_premiums > 0.001 and i['mortgage_insurance_premiums_special'] and v['1040:11'] > premium_limit:
                self.not_implemented()
            return mortgage_insurance_premiums

        def line_12(self, i, v):
            if i['charitable_other_than_cash_check'] > 500 and not i['filling_8283']:
                self.not_implemented()
            return i['charitable_other_than_cash_check']

        def line_18(self, i, v):
            penalties = sum([v[f'1099-int:{n}.box_2'] for n in range(i['1040.number_1099-int'])])
            penalties += sum([v[f'1099-oid:{n}.box_3'] for n in range(i['1040.number_1099-oid'])])
            if penalties > 0.01:
                return penalties
            return ""

        optional_fields = [
            # Medical and Dental Expenses
            FloatField('1', lambda s, i, v: i['medical_dental_expenses']),
            FloatField('2', lambda s, i, v: v['1040.11']),
            FloatField('3', lambda s, i, v: 0.075 * v['2']),
            FloatField('4', lambda s, i, v: 0.0 if v['3'] > v['1'] else v['3'] - v['1']),

            # Taxes you paid
            BooleanField('5a_checkbox', lambda s, i, v: False if not i['general_sales_taxes'] else s.not_implemented()),
            FloatField('5a', line_5a),
            FloatField('5b', lambda s, i, v: i['state_local_real_estate_taxes']),
            FloatField('5c', lambda s, i, v: i['state_local_personal_property_taxes']),
            FloatField('5d', lambda s, i, v: v['5a'] + v['5b'] + v['5c']),
            FloatField('5e', lambda s, i, v: min(5000.0 if i['1040.filing_status'] == s.form('1040').FILING_STATUS.MarriedFilingSeparately else 10000.0, v['5d'])),
            FloatField('6', lambda s, i, v: i['other_taxes_amount']),
            FloatField('7', lambda s, i, v: v['5e'] + v['6']),

            # Interest you paid
            FloatField('8a', line_8a),
            FloatField('8b', lambda s, i, v: i['other_mortgage_interest'] if i['other_mortgage_interest'] > 0.001 and not i['loan_limitations'] else None),
            FloatField('8c', lambda s, i, v: i['other_mortgage_points'] if i['other_mortgage_points'] > 0.001 and not i['loan_limitations'] else None),
            FloatField('8d', line_8d),
            FloatField('8e', lambda s, i, v: v['8a'] + v['8b'] + v['8c'] + v['8d']),
            FloatField('9', lambda s, i, v: s.not_implemented() if i['investment_interest'] else None),
            FloatField('10', lambda s, i, v: v['8e'] + v['9']),

            # Gifts to Charity
            FloatField('11', lambda s, i, v: i['charitable_cash_check']),
            FloatField('12', line_12),
            FloatField('13', lambda s, i, v: i['charitable_carryover'] if i['charitable_carryover'] > 0.001 else None),
            FloatField('14', lambda s, i, v: v['11'] + v['12'] + v['13']),

            # Casualty and Theft Losses
            FloatField('15', lambda s, i, v: s.not_implemented() if i['casualty_theft'] else None),

            # Other Itemized Deductions
            FloatField('16', lambda s, i, v: i['other_itemized'] if i['other_itemized']  > 0.001 else None),

            # Total Itemized Deductions
            FloatField('17', lambda s, i, v: v['4'] + v['7'] + v['10'] + v['14'] + v['15'] + v['16']),
            BooleanField('18', lambda s, i, v: i['itemize_though_less']),
        ]
        required_fields = [
            FloatField('6_type', lambda s, i, v: i['other_taxes_type'] if i['other_taxes_amount'] > 0.001 else None),
            FloatField('8b_desc', lambda s, i, v: i['other_mortgage_interest_desc'] if i['other_mortgage_interest'] > 0.001 and not i['loan_limitations'] else None),
            FloatField('16_type', lambda s, i, v: i['other_itemized_type'] if i['other_itemized'] > 0.001 else None),
        ]

        pdf_fields = [
            TextPDFField('topmostSubform[0].Page1[0].f1_1[0]', '1040.full_names'),
            TextPDFField('topmostSubform[0].Page1[0].f1_2[0]', '1040.you_ssn', max_length=11),
            TextPDFField('topmostSubform[0].Page1[0].f1_3[0]', '1'),
            TextPDFField('topmostSubform[0].Page1[0].f1_4[0]', '2'),
            TextPDFField('topmostSubform[0].Page1[0].f1_5[0]', '3'),
            TextPDFField('topmostSubform[0].Page1[0].f1_6[0]', '4'),
#            ButtonPDFField('topmostSubform[0].Page1[0].c1_1[0]', '5a_checkbox', '1'),
            TextPDFField('topmostSubform[0].Page1[0].f1_7[0]', '5a'),
            TextPDFField('topmostSubform[0].Page1[0].f1_8[0]', '5b'),
            TextPDFField('topmostSubform[0].Page1[0].f1_9[0]', '5c'),
            TextPDFField('topmostSubform[0].Page1[0].f1_10[0]', '5d'),
            TextPDFField('topmostSubform[0].Page1[0].f1_11[0]', '5e'),
            TextPDFField('topmostSubform[0].Page1[0].f1_12[0]', '6_type'),
            TextPDFField('topmostSubform[0].Page1[0].f1_13[0]', '6_type'),
            TextPDFField('topmostSubform[0].Page1[0].f1_14[0]', '6'),
            TextPDFField('topmostSubform[0].Page1[0].f1_15[0]', '7'),
#            ButtonPDFField('topmostSubform[0].Page1[0].Line8_ReadOrder[0].c1_2[0]', '8', '1'), # If you didn’t use all of your home mortgage loan(s) to buy, build, or improve your home, see instructions and check this box
            TextPDFField('topmostSubform[0].Page1[0].f1_16[0]', '8a'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_17[0]', '8b_person'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_18[0]', '8b_person'),
            TextPDFField('topmostSubform[0].Page1[0].f1_19[0]', '8b'),
            TextPDFField('topmostSubform[0].Page1[0].f1_20[0]', '8c'),
            TextPDFField('topmostSubform[0].Page1[0].f1_21[0]', '8d'),
            TextPDFField('topmostSubform[0].Page1[0].f1_22[0]', '8e'),
            TextPDFField('topmostSubform[0].Page1[0].f1_23[0]', '9'),
            TextPDFField('topmostSubform[0].Page1[0].f1_24[0]', '10'),
            TextPDFField('topmostSubform[0].Page1[0].f1_25[0]', '11'),
            TextPDFField('topmostSubform[0].Page1[0].f1_26[0]', '12'),
            TextPDFField('topmostSubform[0].Page1[0].f1_27[0]', '13'),
            TextPDFField('topmostSubform[0].Page1[0].f1_28[0]', '14'),
            TextPDFField('topmostSubform[0].Page1[0].f1_29[0]', '15'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_30[0]', '16_type'),
            TextPDFField('topmostSubform[0].Page1[0].f1_31[0]', '16_type'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_32[0]', '16_type'),
            TextPDFField('topmostSubform[0].Page1[0].f1_33[0]', '16'),
            TextPDFField('topmostSubform[0].Page1[0].f1_34[0]', '17'),
            ButtonPDFField('topmostSubform[0].Page1[0].Line18_ReadOrder[0].c1_3[0]', '18', '1'),
        ]

        pdf_file = os.path.join(os.path.dirname(__file__), 'f1040sa.pdf')
        super().__init__(__class__, inputs, required_fields, optional_fields, pdf_fields=pdf_fields, pdf_file=pdf_file, **kwargs)

    def needs_filing(self, values):
        return values['1040.itemizing']
