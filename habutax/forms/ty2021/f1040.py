import habutax.enum as enum
from habutax.form import Form
from habutax.inputs import *
from habutax.fields import *

class Form1040(Form):
    form_name = "1040"
    tax_year = 2021

    def __init__(self, **kwargs):
        self.FILING_STATUS = enum.make('1040 Filing Status', {
            'Single': "single, unmarried, or legally separated",
            'MarriedFilingJointly': "married and filing a joint return",
            'MarriedFilingSeparately': "married and file a separate return",
            'HeadOfHousehold': "unmarried and provide a home for certain other person",
            'QualifyingWidowWidower': "generally filed if your spouse died in 2019 or 2020 and you didn't remarry before the end of 2021 and you have a child or stepchild whom you can claim as a dependent (see Form 1040 instructions for more)"})
        inputs = [
            EnumInput('filing_status', self.FILING_STATUS, description="Filing Status"),
            StringInput('first_name_middle_initial', description="Your first name and middle initial"),
            StringInput('last_name', description="Your last name"),
            StringInput('spouse_first_name_middle_initial', description="If joint return, spouse's first name and middle initial"),
            StringInput('spouse_last_name', description="If joint return, spouse's last name"),
            StringInput('home_address', description="Home address (number and street). If you have a P.O. box, see instructions."),
            StringInput('apartment_no', description="Apartment number"),
            StringInput('city', description="City, town, or post office."),
            StringInput('state', description="State"),
            StringInput('zip', description="Zip code"),
            StringInput('foreign_country', description="Foreign country name (if you live have a foreign address)"),
            StringInput('foreign_province', description="Foreign province/state/county (if you live have a foreign address)"),
            StringInput('foreign_postal_code', description="Foreign postal code (if you live have a foreign address)"),
            BooleanInput('virtual_currency', description="At any time during 2021, did you receive, sell, exchange, or otherwise dispose of any financial interest in any virtual currency"),
            BooleanInput('standard_deduction_exceptions', description="Are any of the following true?: Can anyone claim you (or your spouse if filing joint) as a dependent, is your spouse itemizing on a seperate return, are you a dual-status alien, were either you (or your spouse if filing joint) born before January 2, 1957 or blind?"),
            BooleanInput('you_presidential_election', description="Check here if you want $3 to go to this fund. Checking a box below will not change your tax or refund."),
            BooleanInput('spouse_presidential_election', description="Check here if your spouse wants $3 to go to this fund. Checking a box below will not change your tax or refund."),
            IntegerInput('number_w-2', description=f'How many, if any, forms W-2 were you provided with for {Form1040.tax_year}?'),
            BooleanInput('unhandled_income', description="Do you have any income you need to report which is *not* included in box 1 of your forms W-2? (see Form 1040 line 1 instructions)"),
            IntegerInput('number_1099-int', description=f'How many, if any, forms 1099-INT were you provided with for tax year {Form1040.tax_year}?'),
            IntegerInput('number_1099-oid', description=f'How many, if any, forms 1099-OID were you provided with for tax year {Form1040.tax_year}?'),
            IntegerInput('number_1099-div', description=f'How many, if any, forms 1099-DIV were you provided with for tax year {Form1040.tax_year}?'),
            BooleanInput('qualified_dividends_incorrect', description=f'Are any of the dividends reported on box 1b of any of your tax year {Form1040.tax_year} Form(s) 1099-DIV not qualified dividends? (see Form 1040 instructions for line 3a)'),
            BooleanInput('ordinary_dividends_incorrect', description=f'Are any of the dividends reported on box 1a of any of your tax year {Form1040.tax_year} Form(s) 1099-DIV not ordinary dividends belonging to you? (see Form 1040 instructions for line 3b)'),
            IntegerInput('number_1099-r', description=f'How many, if any, forms 1099-R were you provided with for tax year {Form1040.tax_year}?'),
            BooleanInput('ira_exception1_you', description='Did you roll over part or all of your IRA distributions from either 1) one Roth IRA to another Roth IRA or 2) one IRA (other than a Roth IRA) to a qualified plan or another IRA (other than a Roth IRA)? Your spouse will be handled separately.'),
            BooleanInput('ira_exception1_you_total', description='Did you roll over *all* of your IRA distributions this year? Your spouse will be handled separately'),
            BooleanInput('ira_exception2_you', description='Do you need to file Form 8606? You might need to if you converted part or all of a traditional, SEP, or SIMPLE IRA to a Roth IRA, you received a distribution from an IRA (other than a Roth IRA) and you made nondeductible contributions to any of your traditional or SEP IRAs for this or an earlier year, received a distribution from a Roth IRA, made excess contributions, had a contribution returned to you, or recharacterized an IRA contribution. See Form 1040 instructions for more cases. Your spouse will be handled separately'),
            BooleanInput('ira_exception3_you', description='Is all or part of your IRA distributions a qualified charitable distribution (QCD)? Your spouse will be handled separately'),
            BooleanInput('ira_exception3_you_total', description='Was the total amount of your IRA distribution a qualified charitable distribution (QCD)? Your spouse will be handled separately'),
            BooleanInput('ira_exception4_you', description='Is all of part of your IRA distributions a health savings account (HSA) funding distribution (HFD)? Your spouse will be handled separately'),
            BooleanInput('ira_exception1_spouse', description='Did your spouse roll over part or all of their IRA distributions from either 1) one Roth IRA to another Roth IRA or 2) one IRA (other than a Roth IRA) to a qualified plan or another IRA (other than a Roth IRA)? You will be handled separately.'),
            BooleanInput('ira_exception1_spouse_total', description='Did your spouse roll over *all* of their IRA distributions this year? You will be handled separately'),
            BooleanInput('ira_exception2_spouse', description='Does your spouse need to file Form 8606? They might need to if they converted part or all of a traditional, SEP, or SIMPLE IRA to a Roth IRA, they received a distribution from an IRA (other than a Roth IRA) and they made nondeductible contributions to any of their traditional or SEP IRAs for this or an earlier year, received a distribution from a Roth IRA, made excess contributions, had a contribution returned to them, or recharacterized an IRA contribution. See Form 1040 instructions for more cases. You will be handled separately'),
            BooleanInput('ira_exception3_spouse', description='Is all or part of your spouse\'s IRA distributions a qualified charitable distribution (QCD)? You will be handled separately'),
            BooleanInput('ira_exception3_spouse_total', description='Was the total amount of your spouse\'s IRA distribution a qualified charitable distribution (QCD)? You will be handled separately'),
            BooleanInput('ira_exception4_spouse', description='Is all of part of your spouse\'s IRA distributions a health savings account (HSA) funding distribution (HFD)? You will be handled separately'),
            BooleanInput('pensions_annuities', description=f'Did you receive any pension or annuity payments in tax year {Form1040.tax_year}? These would likely have been reported on Form(s) 1099-R.'),
            BooleanInput('social_security_benefits', description=f'Did you receive any Social Security benefits in tax year {Form1040.tax_year}? These would likely have been reported on Form(s) SSA-1099 or RRB-1099.'),
            BooleanInput('schedule_d_required', description="Are you required to complete Schedule D? See the line 7 instructions for Form 1040 if you are not sure."),
            BooleanInput('form_8949_required', description="Are you required to complete form 8949? See the line 7 instructions for Form 1040 if you are not sure."),
            BooleanInput('schedule_1_additional_income', description="Do you need to report additional income on Schedule 1? See the instructions for Schedule 1 for Form 1040 if you are not sure."),
            BooleanInput('schedule_1_income_adjustments', description="Do you need to report adjustments to income on Schedule 1? See the instructions for Schedule 1 for Form 1040 if you are not sure."),
            BooleanInput('itemize', description="Would you like to itemize? In most cases, your federal income tax will be less if you take the larger of your itemized deductions or standard deduction. Standard deductions by filing status: Single or Married filing separately: $12,550, Married filing jointly or Qualifying widow(er): $25,100, Head of household: $18,800."),
            FloatInput('charitable_contributions_std_ded', description=f'Enter the total amount of any charitable cash contributions made in {Form1040.tax_year}'),
        ]

        def line_1(self, i, v):
            """Wages, salaries, tips, etc."""
            statutory = False
            for n in range(i['number_w-2']):
                if v[f'w-2:{n}.box_13_statutory']:
                    statutory = True
            if i['unhandled_income'] or statutory:
                s.not_implemented()
            return sum([v[f'w-2:{n}.box_1'] for n in range(i['number_w-2'])]) if i['number_w-2'] > 0 else None

        def line_2b(self, i, v):
            """taxable interest"""
            total = sum([v[f'1099-int:{n}.box_1'] + v[f'1099-int:{n}.box_3'] for n in range(i['number_1099-int'])])
            if total > 1500.0:
                return v['1040_sb.4'] # Schedule B
            elif i['number_1099-oid'] > 0:
                self.not_implemented()
            else:
                return total if i['number_1099-int'] + i['number_1099-oid'] > 0 else None

        def line_3a(self, i, v):
            """qualified dividends"""
            total = sum([v[f'1099-div:{n}.box_1b'] for n in range(i['number_1099-div'])])
            if total > 0.0 and i['qualified_dividends_incorrect']:
                self.not_implemented()
            return total if i['number_1099-div'] > 0 else None

        def line_3b(self, i, v):
            """ordinary dividends"""
            total = sum([v[f'1099-div:{n}.box_1a'] for n in range(i['number_1099-div'])])
            if total > 1500.0:
                return v['1040_sb.6'] # Schedule B
            elif i['ordinary_dividends_incorrect']:
                self.not_implemented()
            return total if i['number_1099-div'] > 0 else None

        def line_4a_4b(self, i, v):
            line_4a = 0.0
            line_4b = 0.0

            ira_distributions_you = sum([v[f'1099-r:{n}.box_1'] if v[f'1099-r:{n}.box_7_ira_sep_simple'] and v[f'1099-r:{n}.for_you'] else 0.0 for n in range(i['number_1099-r'])])
            ira_distributions_spouse = sum([v[f'1099-r:{n}.box_1'] if v[f'1099-r:{n}.box_7_ira_sep_simple'] and not v[f'1099-r:{n}.for_you'] else 0.0 for n in range(i['number_1099-r'])])

            if ira_distributions_you > 0.001:
                if sum([i['ira_exception1_you'], i['ira_exception2_you'], i['ira_exception3_you'], i['ira_exception4_you']]) > 1:
                    self.not_implemented()
                if i['ira_exception1_you']:
                    if not i['ira_exception1_you_total']:
                        self.not_implemented()
                    line_4a += ira_distributions_you
                elif i['ira_exception2_you']:
                    line_4a += ira_distributions_you
                    line_4b += v['8606:you.taxable_amount']
                elif i['ira_exception3_you']:
                    if not i['ira_exception3_you_total'] or ira_distributions_you > 1000000:
                        self.not_implemented()
                    line_4a += ira_distributions_you
                elif i['ira_exception4_you']:
                    self.not_implemented()
                else:
                    line_4b += ira_distributions_you

            if ira_distributions_spouse > 0.001:
                if sum([i['ira_exception1_spouse'], i['ira_exception2_spouse'], i['ira_exception3_spouse'], i['ira_exception4_spouse']]) > 1:
                    self.not_implemented()
                if i['ira_exception1_spouse']:
                    if not i['ira_exception1_spouse_total']:
                        self.not_implemented()
                    line_4a += ira_distributions_spouse
                elif i['ira_exception2_spouse']:
                    line_4a += ira_distributions_spouse
                    line_4b += v['8606:spouse.taxable_amount']
                elif i['ira_exception3_spouse']:
                    if not i['ira_exception3_spouse_total'] or ira_distributions_spouse > 1000000:
                        self.not_implemented()
                    line_4a += ira_distributions_spouse
                elif i['ira_exception4_spouse']:
                    self.not_implemented()
                else:
                    line_4b += ira_distributions_spouse

            return (line_4a, line_4b) if ira_distributions_you + ira_distributions_spouse > 0.001 else (None, None)

        def standard_deduction(self, i):
            statuses = self.form().FILING_STATUS
            if i['filing_status'] in [statuses.Single, statuses.MarriedFilingSeparately]:
                return 12550.00
            elif i['filing_status'] in [statuses.MarriedFilingJointly, statuses.QualifyingWidowWidower]:
                return 25100.00
            elif i['filing_status'] == statuses.HeadOfHousehold:
                return 18800.00
            else:
                self.not_implemented()

        def itemizing(self, i, v):
            return i['itemize'] and (v['1040_sa.17'] >= standard_deduction(self, i) or v['1040_sa.itemize_though_less'])

        def line_12a(self, i, v):
            if itemizing(self, i, v):
                return v['1040_sa.17']
            elif i['standard_deduction_exceptions']:
                self.not_implemented()
            else:
                return standard_deduction(self, i)

        def line_12b(self, i, v):
            if itemizing(self, i, v):
                return 0
            max_contrib = 600 if i['filing_status'] == self.form().FILING_STATUS.MarriedFilingJointly else 300
            return min(i['charitable_contributions_std_ded'], max_contrib) if i['charitable_contributions_std_ded'] > 0.001 else None

        fields = [
            StringField('first_name', lambda s, i, v: i['first_name_middle_initial']),
            StringField('last_name', lambda s, i, v: i['last_name']),
            StringField('spouse_first_name', lambda s, i, v: i['spouse_first_name_middle_initial'] if i['filing_status'] == s.form().FILING_STATUS.MarriedFilingJointly else ""),
            StringField('spouse_last_name', lambda s, i, v: i['spouse_last_name'] if i['filing_status'] == s.form().FILING_STATUS.MarriedFilingJointly else ""),
            FloatField('1', line_1),
            FloatField('2a', lambda s, i, v: sum([v[f'1099-int:{n}.box_8'] for n in range(i['number_1099-int'])])),
            FloatField('2b', line_2b),
            FloatField('3a', line_3a),
            FloatField('3b', line_3b),
            FloatField('4a', lambda s, i, v: line_4a_4b(s, i, v)[0]),
            FloatField('4b', lambda s, i, v: line_4a_4b(s, i, v)[1]),
            FloatField('5a', lambda s, i, v: s.not_implemented() if i['pensions_annuities'] else None),
            FloatField('5b', lambda s, i, v: s.not_implemented() if i['pensions_annuities'] else None),
            FloatField('6a', lambda s, i, v: s.not_implemented() if i['social_security_benefits'] else None),
            FloatField('6b', lambda s, i, v: s.not_implemented() if i['social_security_benefits'] else None),
            FloatField('7', lambda s, i, v: s.not_implemented() if i['schedule_d_required'] or i['form_8949_required'] else None),
            FloatField('8', lambda s, i, v: v['1040_s1.10'] if i['schedule_1_additional_income'] else None),
            FloatField('9', lambda s, i, v: v['1'] + v['2b'] + v['3b'] + v['4b'] + v['5b'] + v['6b'] + v['7'] + v['8']),
            FloatField('10', lambda s, i, v: v['1040_s1.26'] if i['schedule_1_income_adjustments'] else None),
            FloatField('11', lambda s, i, v: v['9'] - v['10']), # AGI
            FloatField('12a', line_12a),
            FloatField('12b', line_12b),
            FloatField('12c', lambda s, i, v: v['12a'] + v['12b']),
            FloatField('13', lambda s, i, v: s.not_implemented()),
            FloatField('14', lambda s, i, v: v['12c'] + v['13']),
            FloatField('15', lambda s, i, v: max(0, v['11'] - v['14'])), # Taxable income
        ]
        super().__init__(__class__, inputs, fields, [], **kwargs)
