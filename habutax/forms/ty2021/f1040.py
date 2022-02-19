from habutax.form import Form
from habutax.inputs import *
from habutax.fields import *

class Form1040(Form):
    form_name = "1040"
    tax_year = 2021

    def __init__(self, **kwargs):
        self.FILING_STATUS = EnumInput('filing_status', ['Single', 'MarriedFilingJointly', 'MarriedFilingSeparately', 'HeadOfHousehold', 'QualifyingWidow(er)'], description="Filing Status")
        inputs = [
            self.FILING_STATUS,
            StringInput('first_name_middle_initial', description="Your first name and middle initial"),
            StringInput('last_name', description="Your last name"),
            StringInput('spouse_first_name_middle_initial', description="If joint return, spouse's first name and middle initial"),
            StringInput('spouse_last_name', description="If joint return, spouse's last name"),
            BooleanInput('you_presidential_election', description="Check here if you, or your spouse if filing jointly, want $3 to go to this fund. Checking a box below will not change your tax or refund."),
            BooleanInput('you_presidential_election', description="Check here if you, or your spouse if filing jointly, want $3 to go to this fund. Checking a box below will not change your tax or refund."),
            IntegerInput('wages_salaries_tips', description="Wages, salaries, tips, etc. Attach Form(s) W-2"),
            IntegerInput('number_1099-int', description='How many, if any, form 1099-INT were you provided with for this year?'),
            IntegerInput('qualified_dividends'),
            IntegerInput('ordinary_dividends'),
            IntegerInput('ira_distributions'),
            IntegerInput('ira_taxable_amount'),
            IntegerInput('pensions_annuities'),
            IntegerInput('pensions_annuities_taxable_amount'),
            IntegerInput('social_security_benefits'),
            IntegerInput('social_security_taxable_amount'),
            BooleanInput('schedule_d_required', description="Are you required to complete Schedule D? See the line 7 instructions for form 1040 if you are not sure."),
            BooleanInput('form_8949_required', description="Are you required to complete form 8949? See the line 7 instructions for form 1040 if you are not sure."),
        ]

        fields = [
            SimpleField('first_name', lambda s, i, v: i['first_name_middle_initial']),
            SimpleField('last_name', lambda s, i, v: i['last_name']),
            SimpleField('spouse_first_name', lambda s, i, v: i['spouse_first_name_middle_initial'] if i['filing_status'] == s.form.FILING_STATUS.MarriedFilingJointly else ""),
            SimpleField('spouse_last_name', lambda s, i, v: i['spouse_last_name'] if i['filing_status'] == s.form.FILING_STATUS.MarriedFilingJointly else ""),
            SimpleField('spouse_last_name', lambda s, i, v: i['last_name']),
            SimpleField('1', lambda s, i, v: i['wages_salaries_tips']),
            SimpleField('2a', lambda s, i, v: sum([v[f'1099-int:{i}.box_8'] for i in range(i['number_1099-int'])])),
            SimpleField('2b', lambda s, i, v: sum([v[f'1099-int:{i}.box_1'] for i in range(i['number_1099-int'])])),
            SimpleField('3a', lambda s, i, v: i['qualified_dividends']),
            SimpleField('3b', lambda s, i, v: i['ordinary_dividends']),
            SimpleField('4a', lambda s, i, v: i['ira_distributions']),
            SimpleField('4b', lambda s, i, v: i['ira_taxable_amount']),
            SimpleField('5a', lambda s, i, v: i['pensions_annuities']),
            SimpleField('5b', lambda s, i, v: i['pensions_annuities_taxable_amount']),
            SimpleField('6a', lambda s, i, v: i['social_security_benefits']),
            SimpleField('6b', lambda s, i, v: i['social_security_taxable_amount']),
            SimpleField('7', lambda s, i, v: s.not_implemented()),
            SimpleField('8', lambda s, i, v: s.not_implemented()),
            #Add lines 1, 2b, 3b, 4b, 5b, 6b, 7, and 8. This is your total income
            SimpleField('9', lambda s, i, v: v['1'] + v['2b'] + v['3b'] + v['4b'] + v['5b'] + v['6b'] + v['7'] + v['8']),
        ]
        super().__init__(__class__, inputs, fields, [], **kwargs)
