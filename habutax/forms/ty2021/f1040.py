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
            IntegerInput('number_w-2', description=f'How many, if any, forms W-2 were you provided with for {Form1040.tax_year}?'),
            BooleanInput('unhandled_income', description="Do you have any income you need to report which is *not* included in box 1 of your forms W-2? (see Form 1040 line 1 instructions)"),
            IntegerInput('number_1099-int', description=f'How many, if any, forms 1099-INT were you provided with for tax year {Form1040.tax_year}?'),
            IntegerInput('number_1099-oid', description=f'How many, if any, forms 1099-OID were you provided with for tax year {Form1040.tax_year}?'),
            IntegerInput('number_1099-div', description=f'How many, if any, forms 1099-DIV were you provided with for tax year {Form1040.tax_year}?'),
            BooleanInput('qualified_dividends_incorrect', description=f'Are any of the dividends reported on box 1b of any of your tax year {Form1040.tax_year} Form(s) 1099-DIV not qualified dividends? (see Form 1040 instructions for line 3a)'),
            BooleanInput('ordinary_dividends_incorrect', description=f'Are any of the dividends reported on box 1a of any of your tax year {Form1040.tax_year} Form(s) 1099-DIV not ordinary dividends belonging to you? (see Form 1040 instructions for line 3b)'),
            IntegerInput('ira_distributions'),
            IntegerInput('ira_taxable_amount'),
            BooleanInput('pensions_annuities', description=f'Did you receive any pension or annuity payments in tax year {Form1040.tax_year}? These would likely have been reported on Form(s) 1099-R.'),
            BooleanInput('social_security_benefits', description=f'Did you receive any Social Security benefits in tax year {Form1040.tax_year}? These would likely have been reported on Form(s) SSA-1099 or RRB-1099.'),
            BooleanInput('schedule_d_required', description="Are you required to complete Schedule D? See the line 7 instructions for Form 1040 if you are not sure."),
            BooleanInput('form_8949_required', description="Are you required to complete form 8949? See the line 7 instructions for Form 1040 if you are not sure."),
            BooleanInput('schedule_1_required', description="Are you required to complete Schedule 1? See the instructions for Schedule 1 for Form 1040 if you are not sure."),
        ]

        def box_1(self, i, v):
            """tax-exempt interest"""
            statutory = False
            for n in range(i['number_w-2']):
                if v[f'w-2:{n}.box_13_statutory']:
                    statutory = True
            if i['unhandled_income'] or statutory:
                s.not_implemented()
            return sum([v[f'w-2:{n}.box_1'] for n in range(i['number_w-2'])])

        def box_2b(self, i, v):
            """taxable interest"""
            total = sum([v[f'1099-int:{n}.box_1'] for n in range(i['number_1099-int'])])
            if total > 1500.0 or i['number_1099-oid'] > 0:
                # Schedule B
                self.not_implemented()
            return total

        def box_3a(self, i, v):
            """qualified dividends"""
            total = sum([v[f'1099-div:{n}.box_1b'] for n in range(i['number_1099-div'])])
            if total > 0.0 and i['qualified_dividends_incorrect']:
                self.not_implemented()
            return total

        def box_3b(self, i, v):
            """ordinary dividends"""
            total = sum([v[f'1099-div:{n}.box_1a'] for n in range(i['number_1099-div'])])
            if total > 1500.0 or i['ordinary_dividends_incorrect']:
                # Schedule B
                self.not_implemented()
            return total

        fields = [
            SimpleField('first_name', lambda s, i, v: i['first_name_middle_initial']),
            SimpleField('last_name', lambda s, i, v: i['last_name']),
            SimpleField('spouse_first_name', lambda s, i, v: i['spouse_first_name_middle_initial'] if i['filing_status'] == s.form.FILING_STATUS.MarriedFilingJointly else ""),
            SimpleField('spouse_last_name', lambda s, i, v: i['spouse_last_name'] if i['filing_status'] == s.form.FILING_STATUS.MarriedFilingJointly else ""),
            SimpleField('spouse_last_name', lambda s, i, v: i['last_name']),
            SimpleField('1', box_1),
            SimpleField('2a', lambda s, i, v: sum([v[f'1099-int:{n}.box_8'] for n in range(i['number_1099-int'])])),
            SimpleField('2b', box_2b),
            SimpleField('3a', box_3a),
            SimpleField('3b', box_3b),
            SimpleField('4a', lambda s, i, v: i['ira_distributions']),
            SimpleField('4b', lambda s, i, v: i['ira_taxable_amount']),
            SimpleField('5a', lambda s, i, v: s.not_implemented() if i['pensions_annuities'] else 0),
            SimpleField('5b', lambda s, i, v: s.not_implemented() if i['pensions_annuities'] else 0),
            SimpleField('6a', lambda s, i, v: s.not_implemented() if i['social_security_benefits'] else 0),
            SimpleField('6b', lambda s, i, v: s.not_implemented() if i['social_security_benefits'] else 0),
            SimpleField('7', lambda s, i, v: s.not_implemented() if i['schedule_d_required'] or i['form_8949_required'] else 0),
            SimpleField('8', lambda s, i, v: v['1040_s1.10'] if i['schedule_1_required'] else 0),
            #Add lines 1, 2b, 3b, 4b, 5b, 6b, 7, and 8. This is your total income
            SimpleField('9', lambda s, i, v: v['1'] + v['2b'] + v['3b'] + v['4b'] + v['5b'] + v['6b'] + v['7'] + v['8']),
            SimpleField('10', lambda s, i, v: v['1040_s1.26'] if i['schedule_1_required'] else 0),
            SimpleField('11', lambda s, i, v: v['9'] - v['10']),
        ]
        super().__init__(__class__, inputs, fields, [], **kwargs)
