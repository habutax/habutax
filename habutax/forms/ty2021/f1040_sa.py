from habutax.form import Form
from habutax.inputs import *
from habutax.fields import *

class Form1040SA(Form):
    form_name = "1040_sa"
    tax_year = 2021

    def __init__(self, **kwargs):
        inputs = [
            BooleanInput('itemize_though_less', description="Do you want to itemize deductions even though they are less than your standard deduction?"),
            FloatInput('medical_dental_expenses', description="Enter the total amount of medical and dental expenses you are allowed to deduct for 2021. This can include insurance premiums for medical and dental care, prescription medicines or insulin, medical specialists, examinations, or other medical care. See the instructions for Form 1040, Schedule A for a detailed explanation of the limitations and restrictions"),
            BooleanInput('general_sales_tax', description="Do you want to deduct general sales tax instead of state and local income tax? (You must choose one, and choosing to deduct general sales tax means your return is not supported by Habutax)"),
            FloatInput('state_local_real_estate_taxes', description="Enter the sum of any state and local taxes you paid in 2021 (either directly or through your mortgage company) on real estate you own that wasn't used for business. See instructions for Form 1040, Schedule A, line 5b for details of what can and cannot be claimed."),
            FloatInput('state_local_personal_property_taxes', description="Enter the sum of any state and local personal property taxes you paid in 2021, but only if the taxes were based on value alone and were imposed on a yearly basis. If you paid a yearly fee for the registration of your car and part of that fee was based on the car's value and part was based on its weight, you can deduct only the part of the fee that was based on the car's value."),
            FloatInput('other_taxes_amount', description="Enter the total amount of any 'other taxes' you want to deduct. You may include income taxes you paid to a foreign country and generation skipping tax (GST) imposed on certain income distributions, but you may want to take a credit for the foreign tax instead of a deduction. See the instructions for Schedule 3 (Form 1040), line 1, for details."),
            StringInput('other_taxes_type', description="Enter the 'type' of each 'other taxes' you are deducting."),
            BooleanInput('loan_limitations', description="Do you have mortgage loans taken out after October 13, 1987, that exceed $750,000 ($375,000 if you are married filing separately, loans exceeding the fair market value of the home, or loan proceeds not used to buy, build, or substantially improve your home?").
            FloatInput('other_mortgage_interest', description="Enter any home mortgage interest not reported to you on Form 1098."),
            StringInput('other_mortgage_interest_desc', description="If the home interest you are claiming that was not reported to you on 1098 was paid to the person from whom you bought the home, see instructions and enter that person’s name, identifying no., and address here"),
            FloatInput('other_mortgage_points', description="Enter any home mortgage points not reported to you on Form 1098. Limits may apply, see Pub. 936 for details."),
            BooleanInput('mortgage_insurance_premiums_special', description="Did you share the costs for mortgage insurance premiums reported on form 1098 with someone (other than your spouse if married filing jointly), or pay mortgage insurance premiums in 2021 for a year other than 2021?"),
            BooleanInput('investment_interest', description="Did you pay interest on money you borrowed that is allocable to property held for investment in 2021?"),
        ]

        def line_5a(self, i, v):
            # TODO If we implement Schedules C, E, or F, we must reduce the
            # amount calculated here by any amounts of these withheld taxes
            # which are deducted on one of those forms (or elsewhere)
            state_local_income_taxes = sum(v[f'w-2:{n}.box_17'] + v[f'w-2:{n}.box_19'] for n in range(i['number_w-2']))
            state_local_income_taxes += sum(v[f'1099-div:{n}.box_16_1'] + v[f'1099-div:{n}.box_16_2'] for n in range(i['number_1099-div']))
            state_local_income_taxes += sum(v[f'1099-int:{n}.box_17_1'] + v[f'1099-int:{n}.box_17_2'] for n in range(i['number_1099-int']))
            state_local_income_taxes += sum(v[f'1099-r:{n}.box_14_1'] + v[f'1099-r:{n}.box_14_2'] + v[f'1099-r:{n}.box_17_1'] + v[f'1099-r:{n}.box_17_2'] for n in range(i['number_1099-r']))
            return state_local_income_taxes

        def line_8a(self, i, v):
            mortgage_interest_points = sum([v[f'1098:{n}.box_1'] for n in range(i['number_1098'])])
            mortgage_interest_points += sum([v[f'1098:{n}.box_6'] for n in range(i['number_1098'])])
            if mortgage_interest_points > 0.001 and i['loan_limitations']:
                self.not_implemented()
            return mortgage_interest_points

        def line_8d(self, i, v):
            mortgage_insurance_premiums = sum([v[f'1098:{n}.box_5'] for n in range(i['number_1098'])])
            if mortgage_insurance_premiums < 0.001:
                return None
            premium_limit = 50000 if i['1040.filing_status'] == self.form('1040').FILING_STATUS.MarriedFilingSeparately else 100000
            if mortgage_insurance_premiums > 0.001 and i['mortgage_insurance_premiums_special'] and v['1040:11'] > premium_limit:
                self.not_implemented()
            return mortgage_insurance_premiums

        def line_18(self, i, v):
            penalties = sum([v[f'1099-int:{n}.box_2'] for n in range(i['number_1099-int'])])
            penalties += sum([v[f'1099-oid:{n}.box_3'] for n in range(i['number_1099-oid'])])
            if penalties > 0.01:
                return penalties
            return ""

        optional_fields = [
            # Medical and Dental Expenses
            FloatField('1', lambda s, i, v: i['medical_dental_expenses']),
            FloatField('2', lambda s, i, v: v['1040.11']),
            FloatField('3', lambda s, i, v: 0.075 * v['2']),
            FloatField('4', lambda s, i, v: 0 if v['3'] > v['1'] else v['3'] - v['1']),

            # Taxes you paid
            BooleanField('5a_checkbox', lambda s, i, v: False if not i['general_sales_taxes'] else s.not_implemented()),
            FloatField('5a', line_5a),
            FloatField('5b', lambda s, i, v: i['state_local_real_estate_taxes']),
            FloatField('5c', lambda s, i, v: i['state_local_personal_property_taxes']),
            FloatField('5d', lambda s, i, v: v['5a'] + v['5b'] + v['5c']),
            FloatField('5e', lambda s, i, v: min(5000 if i['1040.filing_status'] == self.form('1040').FILING_STATUS.MarriedFilingSeparately else 10000, v['5d'])),
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
            # TODO
            # Casualty and Theft Losses
            # TODO
            # Other Itemized Deductions
            # TODO

            # Total Itemized Deductions
            FloatField('17', lambda s, i, v: v['4'] + v['7'] + v['10'] + v['14'] + v['15'] + v['16']),
            BooleanField('18', lambda s, i, v: i['itemize_though_less']),
        ]
        required_fields = [
            FloatField('6_type', lambda s, i, v: i['other_taxes_type'] if i['other_taxes_amount'] > 0.001 else None),
            FloatField('8b_desc', lambda s, i, v: i['other_mortgage_interest_desc'] if i['other_mortgage_interest'] > 0.001 and not i['loan_limitations'] else None),
        ]

        super().__init__(__class__, inputs, required_fields, optional_fields, **kwargs)
