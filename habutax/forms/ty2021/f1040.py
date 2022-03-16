import os

import habutax.enum as enum
from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *
from habutax.pdf_fields import *

from habutax.forms.ty2021.f1040_figure_tax import figure_tax

class Form1040(Form):
    form_name = "1040"
    tax_year = 2021
    description = "Form 1040"
    long_description = "U.S. Individual Income Tax Return"
    jurisdiction = Jurisdiction.US
    sequence_no = 0

    def __init__(self, **kwargs):
        self.FILING_STATUS = enum.make('1040 Filing Status', {
            'Single': "single, unmarried, or legally separated",
            'MarriedFilingJointly': "married and filing a joint return",
            'MarriedFilingSeparately': "married and file a separate return",
            'HeadOfHousehold': "unmarried and provide a home for certain other person",
            'QualifyingWidowWidower': "generally filed if your spouse died in 2019 or 2020 and you didn't remarry before the end of 2021 and you have a child or stepchild whom you can claim as a dependent (see Form 1040 instructions for more)"})
        inputs = [
            EnumInput('filing_status', self.FILING_STATUS, description="Filing Status"),
            StringInput('first_name', description="Your first name"),
            StringInput('middle_initial', description="Your middle initial"),
            StringInput('last_name', description="Your last name"),
            SSNInput(f'you_ssn', description='Enter your Social Security number'),
            SSNInput(f'spouse_ssn', description='Enter your spouse\'s Social Security number'),
            StringInput('occupation', description="Your occupation"),
            StringInput('spouse_first_name', description="If joint return, spouse's first name"),
            StringInput('spouse_middle_initial', description="If joint return, spouse's middle initial"),
            StringInput('spouse_last_name', description="If joint return, spouse's last name"),
            StringInput('spouse_occupation', description="Spouse's occupation"),
            StringInput('phone_number', description="Your phone number"),
            StringInput('email_address', description="Your email address"),
            StringInput('home_address', description="Home address (number and street). If you have a P.O. box, see instructions."),
            StringInput('apartment_no', description="Apartment number"),
            StringInput('city', description="City, town, or post office."),
            EnumInput('state', enum.us_states, description="State"),
            StringInput('zip', description="Zip code"),
            StringInput('foreign_country', description="Foreign country name (if you have a foreign address)"),
            StringInput('foreign_province', description="Foreign province/state/county (if you have a foreign address)"),
            StringInput('foreign_postal_code', description="Foreign postal code (if you have a foreign address)"),
            BooleanInput('you_presidential_election', description="Check here if you want $3 to go to this fund. Checking a box below will not change your tax or refund."),
            BooleanInput('spouse_presidential_election', description="Check here if your spouse wants $3 to go to this fund. Checking a box below will not change your tax or refund."),
            BooleanInput('virtual_currency', description="At any time during 2021, did you receive, sell, exchange, or otherwise dispose of any financial interest in any virtual currency?"),
            IntegerInput('number_dependents', description="How many dependents can you claim for 2021? (See Form 1040 instructions)"),
            BooleanInput('claimed_as_dependent', description="Can anyone claim you (or your spouse if filing joint) as a dependent?"),
            BooleanInput('standard_deduction_exceptions', description="Are any of the following true?: Can anyone claim you (or your spouse if filing joint) as a dependent, is your spouse itemizing on a seperate return, are you a dual-status alien, were either you (or your spouse if filing joint) born before January 2, 1957 or blind?"),
            IntegerInput('number_w-2', description=f'How many, if any, forms W-2 were you provided with for {Form1040.tax_year}?'),
            BooleanInput('unhandled_income', description="Do you have any income you need to report which is *not* included in box 1 of your forms W-2? (see Form 1040 line 1 instructions)"),
            IntegerInput('number_1098', description=f'How many, if any, forms 1098 were you provided with for tax year {Form1040.tax_year}?'),
            IntegerInput('number_1099-g', description=f'How many, if any, forms 1099-G were you provided with for tax year {Form1040.tax_year}?'),
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
            BooleanInput('form_8949_required', description="Are you required to complete form 8949 (Sales and Other Dispositions of Capital Assets)? See the line 7 instructions for Form 1040 if you are not sure."),
            BooleanInput('schedule_1_additional_income', description="Do you need to report additional income on Schedule 1? This includes prior year tax refunds paid in 2021, alimony received, unemployment compensation, and more. See the instructions for Schedule 1 for Form 1040 if you are not sure."),
            BooleanInput('schedule_1_income_adjustments', description="Do you need to report adjustments to income on Schedule 1? This includes educator expenses, any HSA contributions you or your spouse made in 2021, self-employment tax, IRA deductions, student loan interest deductions, and more. See the instructions for Schedule 1 for Form 1040 if you are not sure."),
            BooleanInput('itemize', description="Would you like to itemize? In most cases, your federal income tax will be less if you take the larger of your itemized deductions or standard deduction. Standard deductions by filing status: Single or Married filing separately: $12,550, Married filing jointly or Qualifying widow(er): $25,100, Head of household: $18,800."),
            FloatInput('charitable_contributions_std_ded', description=f'Enter the total amount of any charitable cash contributions made in {Form1040.tax_year}'),
            BooleanInput('uncommon_tax', description="Do you need to report a child's interest or dividends, need to make a section 962 election, recapture an education credit, have anything to do with a section 1291 fund, need to repay any excess advance payments of the health coverage tax credit from Form 8885, have tax from tax from Form 8978, line 14 (relating to partner's audit liability under section 6226), any net tax liability deferred under section 965(i), or a triggering event under section 965(i), have any income from farming or fishing, or want to claim the foreign earned income exclusion, housing exclusion, or housing deduction on Form 2555? These are not common... see the instructions for line 16, Form 1040."),
            BooleanInput('need_8615', description="Do you need to use Form 8615 to figure your tax? It must generally be used to figure the tax on your unearned income over $2,200 if you are under age 18, and in certain situations if you are older. See the instructions for line 16, form 1040."),
            BooleanInput('need_8962', description="If you, your spouse with whom you are filing a joint return, or your dependent was enrolled in health insurance coverage purchased from the Marketplace, were advance payments of the premium tax credit made for the coverage in 2021?"),
            BooleanInput('need_schedule_3_part_i', description="Do you want to claim any nonrefundable credits on Schedule 3, part I? These include credit for child and dependent care expenses, education credits, retirement savings, residential energy credits, among others."),
            BooleanInput('need_schedule_3_part_ii', description="Do you want to claim any 'Other Payments and Refundable Credits' on Schedule 3, part I? These include Net premium tax credit, paying some tax with a request for tax filing extension, excess social security and tier 1 RRTA tax withheld, credit for federal tax on fuels, qualified sick and family leave credits, health coverage tax credits, credit for child and dependent care expenses, among others."),
            BooleanInput('need_schedule_2', description="Do you need to pay any less common additional taxes (self-employment, unreported tip income, additional medicare tax, etc.)? See the Form 1040, Schedule 2 instructions for more details."),
            FloatInput('estimated_tax_payments', description="Enter the total of any 2021 estimated tax payments and amount applied from your 2020 return."),
            BooleanInput('self_employment_income', description="Did you (or your spouse if married filing jointly) have any self-employment income to report?"),
            BooleanInput('rrta_compensation', description="Do you (or your spouse if married filing jointly) have any Railroad Retirement Tax Act compensation to report for 2021?"),
            BooleanInput('form_4797', description="Did you sell business property in 2021 or otherwise need to file Form 4797?"),
            BooleanInput('postsecondary_education_expenses', description="Did you pay any qualified education expenses to an eligible postsecondary educational institution in 2021? See instructions for Schedule 3, line 3 and Form 8863 for more information"),
            FloatInput('apply_to_estimated_tax', description="Enter the dollar amount of your refund you want to apply to your 2022 estimated tax. This will reduce your refund for this year."),
            RegexInput('routing_number', '^(0[1-9]|1[0-2]|2[1-9]|3[0-2])[0-9]{7}$', description="What is the routing number of the account in your name into which you want your refund deposited? (must be 9 digits)"),
            BooleanInput('checking_account', description="Is the account you want your refund deposited into a checking account? (savings account is assumed otherwise)"),
            RegexInput('account_number', '^[0-9A-Za-z\-]{1,17}$', description="What is the account number of the account in your name into which you want your refund deposited?"),
            FloatInput('tax_penalty', description="You may owe a tax penalty for not paying enough taxes. Please complete Form 2210 to determine if you owe a penalty (and the amount, if so) and enter the result here."),
        ]

        for n in range(4):
            inputs += [
                StringInput(f'dependent_{n}_name', description=f'Enter the first and last name for dependent {n+1}'),
                SSNInput(f'dependent_{n}_ssn', description=f'Enter the Social Security number for dependent {n+1}'),
                StringInput(f'dependent_{n}_relationship', description=f'What is the relationship of {n+1} to you?'),
                BooleanInput(f'dependent_{n}_ctc', description=f'Does dependent {n+1} qualify for the child tax credit? See the "Who Qualifies as Your Dependent" section in the instructions for Form 1040.'),
                BooleanInput(f'dependent_{n}_odc', description=f'Does dependent {n+1} qualify for the credit for other dependents? See the "Who Qualifies as Your Dependent" section in the instructions for Form 1040.'),
            ]

        def full_names(self, i, v):
            names = [f'{v["first_name"]} {v["last_name"]}']
            if i['filing_status'] == self.form().FILING_STATUS.MarriedFilingJointly:
                names.append(f'{v["spouse_first_name"]} {v["spouse_last_name"]}')
            return ", ".join(names)

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

            ira_distributions_you = sum([v[f'1099-r:{n}.box_1'] if v[f'1099-r:{n}.box_7_ira_sep_simple'] and v[f'1099-r:{n}.belongs_to'] == enum.taxpayer_or_spouse.taxpayer else 0.0 for n in range(i['number_1099-r'])])
            ira_distributions_spouse = sum([v[f'1099-r:{n}.box_1'] if v[f'1099-r:{n}.box_7_ira_sep_simple'] and v[f'1099-r:{n}.belongs_to'] ==enum.taxpayer_or_spouse.spouse else 0.0 for n in range(i['number_1099-r'])])

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

        def schedule_1_additional_income(self, i, v):
            mort_int_refund = sum([v[f'1098:{n}.box_4'] for n in range(i['number_1098'])])
            state_income_refund = sum([v[f'1099-g:{n}.box_2'] for n in range(i['number_1099-g'])])
            return (mort_int_refund + state_income_refund) > 0.001 or i['schedule_1_additional_income']

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

        def line_12a(self, i, v):
            if v['itemizing']:
                return v['1040_sa.17']
            elif i['standard_deduction_exceptions']:
                self.not_implemented()
            else:
                return standard_deduction(self, i)

        def line_12b(self, i, v):
            if v['itemizing']:
                return None
            max_contrib = 600.0 if i['filing_status'] == self.form().FILING_STATUS.MarriedFilingJointly else 300.0
            return min(i['charitable_contributions_std_ded'], max_contrib) if i['charitable_contributions_std_ded'] > 0.001 else None

        def line_13(self, i, v):
            section_199a = sum([v[f'1099-div:{n}.box_5'] for n in range(i['number_1099-div'])])

            statuses = self.form().FILING_STATUS
            income_limit = 164900.00
            if i['filing_status'] is statuses.MarriedFilingSeparately:
                income_limit = 64925.00
            elif i['filing_status'] is statuses.MarriedFilingJointly:
                income_limit = 329800.00

            if section_199a > 0.001:
                if (v['11'] - v['12c']) > income_limit:
                    self.not_implemented()
                return v['8995.15']
            return None

        def line_16(self, i, v):
            if i['uncommon_tax'] or i['need_8615'] or i['schedule_d_required']:
                self.not_implemented()
            if v['3a'] > 0.001 or v['7'] > 0.001:
                return v['1040_qualdiv_capgain_tax_wkst.25']
            return figure_tax(v['15'], i['filing_status'], self.form().FILING_STATUS)

        def line_19(self, i, v):
            if i['number_dependents'] > 4:
                self.not_implemented()
            elif i['number_dependents'] > 0:
                if v['1040_s8812.additional_tax'] > 0.001:
                    self.not_implemented()
                return v['1040_s8812.nonrefundable_ctc_or_odc']
            else:
                return None

        def line_20(self, i, v):
            foreign_tax = float(sum([v[f'1099-int:{n}.box_6'] for n in range(i['number_1099-int'])]))
            foreign_tax += float(sum([v[f'1099-div:{n}.box_7'] for n in range(i['number_1099-div'])]))
            if foreign_tax > 0.001 or i['need_schedule_3_part_i']:
                return v['1040_s3.8']
            return None

        def line_25b(self, i, v):
            withholding = float(sum([v[f'1099-r:{n}.box_4'] for n in range(i['number_1099-r'])]))
            withholding += float(sum([v[f'1099-div:{n}.box_4'] for n in range(i['number_1099-div'])]))
            withholding += float(sum([v[f'1099-int:{n}.box_4'] for n in range(i['number_1099-int'])]))
            if withholding > 0.001:
                return withholding
            return None

        def line_28(self, i, v):
            if i['number_dependents'] > 4:
                self.not_implemented()
            elif i['number_dependents'] > 0:
                if v['1040_s8812.additional_tax'] > 0.001:
                    self.not_implemented()
                return v['1040_s8812.refundable_ctc_or_additional_ctc']
            else:
                return None

        def form_8959_required(self, i, v):
            for n in range(i['number_w-2']):
                if v[f'w-2:{n}.box_5'] > 200000:
                    return True
            statuses = self.form().FILING_STATUS
            threshold = 200000.0
            if i['filing_status'] is statuses.MarriedFilingJointly:
                threshold = 250000.0
            elif i['filing_status'] is statuses.MarriedFilingSeparately:
                threshold = 125000.0

            medicare_wages_tips = float(sum([v[f'w-2:{n}.box_5'] for n in range(i['number_w-2'])]))

            if medicare_wages_tips > threshold:
                return True

            if i['rrta_compensation'] or i['self_employment_income']:
                self.not_implemented()
            return False

        def possible_eic(self, i, v):
            dependent_map = {
                # dependents: (non-MFJ filers, MarriedFilingJointly)
                3: (51464, 57414),
                2: (47915, 53865),
                1: (42158, 48108),
                0: (21430, 27380)
            }
            dependents = min(3, i['number_dependents'])
            filing_index = 1 if i['filing_status'] is self.form().FILING_STATUS.MarriedFilingJointly else 0
            eic_income_limit = dependent_map[dependents][filing_index]
            if v['11'] >= eic_income_limit:
                return False

            investment_income = v['2a'] + v['2b'] + v['3b'] + max(0, v['7'])
            if investment_income > 10000 and not i['form_4797']:
                return False
            return True

        def line_38(self, i, v):
            tax_shown = v['24'] - sum([v['27a'], v['28'], v['29'], v['30']])
            if i['need_schedule_3_part_ii']:
                tax_shown -= sum([v[f'1040_s3.{l}'] for l in ['9', '12', '13b', '13h']])
            if v['37'] >= 1000.0 and v['37'] > (0.1 * tax_shown):
                return i['tax_penalty']
            return None

        required_fields = [
            EnumField('filing_status', self.FILING_STATUS, lambda s, i, v: i['filing_status']),
            StringField('first_name', lambda s, i, v: f'{i["first_name"]} {i["middle_initial"]}'.strip()),
            StringField('last_name', lambda s, i, v: i['last_name']),
            StringField('you_ssn', lambda s, i, v: i['you_ssn']),
            StringField('spouse_first_name', lambda s, i, v: f'{i["spouse_first_name"]} {i["spouse_middle_initial"]}'.strip() if i['filing_status'] == s.form().FILING_STATUS.MarriedFilingJointly else None),
            StringField('spouse_last_name', lambda s, i, v: i['spouse_last_name'] if i['filing_status'] == s.form().FILING_STATUS.MarriedFilingJointly else None),
            StringField('spouse_ssn', lambda s, i, v: i['spouse_ssn'] if i['filing_status'] == s.form().FILING_STATUS.MarriedFilingJointly else None),
            StringField('full_names', full_names),
            StringField('home_address', lambda s, i, v: i['home_address']),
            StringField('apartment_no', lambda s, i, v: i['apartment_no']),
            StringField('city', lambda s, i, v: i['city']),
            StringField('state', lambda s, i, v: str(i['state'])),
            StringField('zip', lambda s, i, v: i['zip']),
            StringField('foreign_country', lambda s, i, v: i['foreign_country']),
            StringField('foreign_province', lambda s, i, v: i['foreign_province']),
            StringField('foreign_postal_code', lambda s, i, v: i['foreign_postal_code']),
            BooleanField('you_presidential_election', lambda s, i, v: i['you_presidential_election']),
            BooleanField('spouse_presidential_election', lambda s, i, v: i['spouse_presidential_election'] if i['filing_status'] == s.form().FILING_STATUS.MarriedFilingJointly else False),
            BooleanField('virtual_currency', lambda s, i, v: s.not_implemented() if i['virtual_currency'] else False),
            FloatField('1', line_1),
            FloatField('2a', lambda s, i, v: float(sum([v[f'1099-int:{n}.box_8'] for n in range(i['number_1099-int'])]))),
            FloatField('2b', line_2b),
            FloatField('3a', line_3a),
            FloatField('3b', line_3b),
            FloatField('4a', lambda s, i, v: line_4a_4b(s, i, v)[0]),
            FloatField('4b', lambda s, i, v: line_4a_4b(s, i, v)[1]),
            FloatField('5a', lambda s, i, v: s.not_implemented() if i['pensions_annuities'] else None),
            FloatField('5b', lambda s, i, v: s.not_implemented() if i['pensions_annuities'] else None),
            FloatField('6a', lambda s, i, v: s.not_implemented() if i['social_security_benefits'] else None),
            FloatField('6b', lambda s, i, v: s.not_implemented() if i['social_security_benefits'] else None),
            BooleanField('7_checkbox', lambda s, i, v: not i['schedule_d_required']),
            FloatField('7', lambda s, i, v: s.not_implemented() if i['schedule_d_required'] or i['form_8949_required'] else None),
            BooleanField('schedule_1_additional_income', lambda s, i, v: schedule_1_additional_income(s, i, v)),
            FloatField('8', lambda s, i, v: v['1040_s1.10'] if v['schedule_1_additional_income'] else None),
            FloatField('9', lambda s, i, v: v['1'] + v['2b'] + v['3b'] + v['4b'] + v['5b'] + v['6b'] + v['7'] + v['8']),
            FloatField('10', lambda s, i, v: v['1040_s1.26'] if i['schedule_1_income_adjustments'] else None),
            FloatField('11', lambda s, i, v: v['9'] - v['10']), # AGI
            BooleanField('itemizing', lambda s, i, v: i['itemize'] and (v['1040_sa.17'] >= standard_deduction(s, i) or v['1040_sa.itemize_though_less'])),
            FloatField('12a', line_12a),
            FloatField('12b', line_12b),
            FloatField('12c', lambda s, i, v: v['12a'] + v['12b']),
            FloatField('13', line_13),
            FloatField('14', lambda s, i, v: v['12c'] + v['13']),
            FloatField('15', lambda s, i, v: max(0.0, v['11'] - v['14'])), # Taxable income
            FloatField('16', line_16), # Tax
            BooleanField('schedule_2_part_i_needed', lambda s, i, v: i['need_8962'] or v['1040_s2_need_6251.need_6251']),
            FloatField('17', lambda s, i, v: v['1040_s2.3'] if v['schedule_2_part_i_needed'] else None),
            FloatField('18', lambda s, i, v: v['16'] + v['17']),
            FloatField('19', line_19),
            FloatField('20', line_20),
            FloatField('21', lambda s, i, v: v['19'] + v['20']),
            FloatField('22', lambda s, i, v: max(0.0, v['18'] - v['21'])),
            FloatField('23', lambda s, i, v: s.not_implemented() if i['need_schedule_2'] else None),
            FloatField('24', lambda s, i, v: v['22'] + v['23']),
            FloatField('25a', lambda s, i, v: sum([v[f'w-2:{n}.box_2'] for n in range(i['number_w-2'])]) if i['number_w-2'] > 0 else None),
            FloatField('25b', line_25b),
            FloatField('25c', lambda s, i, v: v['8959.24'] if form_8959_required(s, i, v) else None),
            FloatField('25d', lambda s, i, v: v['25a'] + v['25b'] + v['25c']),
            FloatField('26', lambda s, i, v: i['estimated_tax_payments']),
            FloatField('27a', lambda s, i, v: s.not_implemented("You may be able to claim the Earned Income Credit, but it is not implemented") if possible_eic(s, i, v) else None),
            BooleanField('27a_checkbox', lambda s, i, v: s.not_implemented("You may be able to claim the Earned Income Credit, but it is not implemented") if possible_eic(s, i, v) else False),
            FloatField('27b', lambda s, i, v: s.not_implemented("You may be able to claim the Earned Income Credit, but it is not implemented") if possible_eic(s, i, v) else None),
            FloatField('27c', lambda s, i, v: s.not_implemented("You may be able to claim the Earned Income Credit, but it is not implemented") if possible_eic(s, i, v) else None),
            FloatField('28', line_28),
            FloatField('29', lambda s, i, v: s.not_implemented("Form 8863 not implemented") if i['postsecondary_education_expenses'] else None),
            FloatField('30', lambda s, i, v: v['1040_recovery_rebate_credit_wkst.credit']),
            FloatField('31', lambda s, i, v: s.not_implemented() if i['need_schedule_3_part_ii'] else None),
            FloatField('32', lambda s, i, v: v['27a'] + v['28'] + v['29'] + v['30'] + v['31']),
            FloatField('33', lambda s, i, v: v['25d'] + v['26'] + v['32']),
            FloatField('34', lambda s, i, v: (v['33'] - v['24']) if v['33'] > v['24'] else None),
            FloatField('35a', lambda s, i, v: v['34'] - v['36'] if v['34'] > 0.001 else None),
            StringField('35b', lambda s, i, v: i['routing_number'] if v['35a'] > 0.001 else None),
            BooleanField('35c', lambda s, i, v: i['checking_account'] if v['35a'] > 0.001 else None),
            StringField('35d', lambda s, i, v: i['account_number'] if v['35a'] > 0.001 else None),
            FloatField('36', lambda s, i, v: min(v['34'], max(0.0, i['apply_to_estimated_tax'])) if v['34'] > 0.001 else None),
            FloatField('37', lambda s, i, v: None if v['33'] > v['24'] else v['24'] - v['33']),
            FloatField('38', line_38),
            BooleanField('designee', lambda s, i, v: False),
            StringField('occupation', lambda s, i, v: i['occupation']),
            StringField('spouse_occupation', lambda s, i, v: i['spouse_occupation'] if i['filing_status'] == s.form().FILING_STATUS.MarriedFilingJointly else ""),
            StringField('phone_number', lambda s, i, v: i['phone_number']),
            StringField('email_address', lambda s, i, v: i['email_address']),
        ]
        for n in range(4):
            required_fields += [
                StringField(f'dependent_{n}_name', lambda s, i, v, n=n: i[f'dependent_{n}_name'] if n < i['number_dependents'] else None),
                StringField(f'dependent_{n}_ssn', lambda s, i, v, n=n: i[f'dependent_{n}_ssn'] if n < i['number_dependents'] else None),
                StringField(f'dependent_{n}_relationship', lambda s, i, v, n=n: i[f'dependent_{n}_relationship'] if n < i['number_dependents'] else None),
                BooleanField(f'dependent_{n}_ctc', lambda s, i, v, n=n: i[f'dependent_{n}_ctc'] if n < i['number_dependents'] else None),
                BooleanField(f'dependent_{n}_odc', lambda s, i, v, n=n: i[f'dependent_{n}_odc'] if n < i['number_dependents'] and not v[f'dependent_{n}_ctc'] else None),
            ]

        pdf_fields = [
            ButtonPDFField('topmostSubform[0].Page1[0].FilingStatus[0].c1_01[0]', 'filing_status', '1', value_fn=lambda s, v, f: v == f.enum().Single),
            ButtonPDFField('topmostSubform[0].Page1[0].FilingStatus[0].c1_01[1]', 'filing_status', '2', value_fn=lambda s, v, f: v == f.enum().MarriedFilingJointly),
            ButtonPDFField('topmostSubform[0].Page1[0].FilingStatus[0].c1_01[2]', 'filing_status', '3', value_fn=lambda s, v, f: v == f.enum().MarriedFilingSeparately),
            ButtonPDFField('topmostSubform[0].Page1[0].FilingStatus[0].c1_01[3]', 'filing_status', '4', value_fn=lambda s, v, f: v == f.enum().HeadOfHousehold),
            ButtonPDFField('topmostSubform[0].Page1[0].FilingStatus[0].c1_01[4]', 'filing_status', '5', value_fn=lambda s, v, f: v == f.enum().QualifyingWidowWidower),
#            TextPDFField('topmostSubform[0].Page1[0].FilingStatus[0].f1_01[0]', 'other_spouse_dependent'),
            TextPDFField('topmostSubform[0].Page1[0].f1_02[0]', 'first_name'),
            TextPDFField('topmostSubform[0].Page1[0].f1_03[0]', 'last_name'),
            TextPDFField('topmostSubform[0].Page1[0].YourSocial[0].f1_04[0]', 'you_ssn', max_length=9),
            TextPDFField('topmostSubform[0].Page1[0].f1_05[0]', 'spouse_first_name'),
            TextPDFField('topmostSubform[0].Page1[0].f1_06[0]', 'spouse_last_name'),
            TextPDFField('topmostSubform[0].Page1[0].SpousesSocial[0].f1_07[0]', 'spouse_ssn', max_length=9),
            TextPDFField('topmostSubform[0].Page1[0].Address[0].f1_08[0]', 'home_address'),
            TextPDFField('topmostSubform[0].Page1[0].Address[0].f1_09[0]', 'apartment_no'),
            TextPDFField('topmostSubform[0].Page1[0].Address[0].f1_10[0]', 'city'),
            TextPDFField('topmostSubform[0].Page1[0].Address[0].f1_11[0]', 'state'),
            TextPDFField('topmostSubform[0].Page1[0].Address[0].f1_12[0]', 'zip'),
            TextPDFField('topmostSubform[0].Page1[0].Address[0].f1_13[0]', 'foreign_country'),
            TextPDFField('topmostSubform[0].Page1[0].Address[0].f1_14[0]', 'foreign_country'),
            TextPDFField('topmostSubform[0].Page1[0].Address[0].f1_15[0]', 'foreign_postal_code'),
            ButtonPDFField('topmostSubform[0].Page1[0].c1_02[0]', 'you_presidential_election', '1'),
            ButtonPDFField('topmostSubform[0].Page1[0].c1_03[0]', 'spouse_presidential_election', '1'),
            ButtonPDFField('topmostSubform[0].Page1[0].c1_04[0]', 'virtual_currency', '1'),
            ButtonPDFField('topmostSubform[0].Page1[0].c1_04[1]', 'virtual_currency', '2', value_fn=lambda s, v, f: not v),
#            ButtonPDFField('topmostSubform[0].Page1[0].c1_05[0]', 'you_as_dependent', '1'),
#            ButtonPDFField('topmostSubform[0].Page1[0].c1_06[0]', 'spouse_as_dependent', '1'),
#            ButtonPDFField('topmostSubform[0].Page1[0].c1_07[0]', 'spouse_itemize_or_alien', '1'),
#            ButtonPDFField('topmostSubform[0].Page1[0].c1_08[0]', 'old', '1'),
#            ButtonPDFField('topmostSubform[0].Page1[0].c1_09[0]', 'blind', '1'),
#            ButtonPDFField('topmostSubform[0].Page1[0].c1_10[0]', 'spouse_old', '1'),
#            ButtonPDFField('topmostSubform[0].Page1[0].c1_11[0]', 'spouse_blind', '1'),
#            ButtonPDFField('topmostSubform[0].Page1[0].Dependents_ReadOrder[0].c1_12[0]', 'more_than_4_dependents', '1'),
            TextPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row1[0].f1_16[0]', 'dependent_0_name'),
            TextPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row1[0].f1_17[0]', 'dependent_0_ssn', max_length=9),
            TextPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row1[0].f1_18[0]', 'dependent_0_relationship'),
            ButtonPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row1[0].c1_13[0]', 'dependent_0_ctc', '1'),
            ButtonPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row1[0].c1_14[0]', 'dependent_0_odc', '1'),
            TextPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row2[0].f1_19[0]', 'dependent_1_name'),
            TextPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row2[0].f1_20[0]', 'dependent_1_ssn', max_length=9),
            TextPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row2[0].f1_21[0]', 'dependent_1_relationship'),
            ButtonPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row2[0].c1_15[0]', 'dependent_1_ctc', '1'),
            ButtonPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row2[0].c1_16[0]', 'dependent_0_odc', '1'),
            TextPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row3[0].f1_22[0]', 'dependent_2_name'),
            TextPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row3[0].f1_23[0]', 'dependent_2_ssn', max_length=9),
            TextPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row3[0].f1_24[0]', 'dependent_2_relationship'),
            ButtonPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row3[0].c1_17[0]', 'dependent_2_ctc', '1'),
            ButtonPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row3[0].c1_18[0]', 'dependent_2_odc', '1'),
            TextPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row4[0].f1_25[0]', 'dependent_3_name'),
            TextPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row4[0].f1_26[0]', 'dependent_3_ssn', max_length=9),
            TextPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row4[0].f1_27[0]', 'dependent_3_relationship'),
            ButtonPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row4[0].c1_19[0]', 'dependent_3_ctc', '1'),
            ButtonPDFField('topmostSubform[0].Page1[0].Table_Dependents[0].Row4[0].c1_20[0]', 'dependent_3_odc', '1'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_28[0]', '1'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_29[0]', '2a'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_30[0]', '2b'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_31[0]', '3a'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_32[0]', '3b'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_33[0]', '4a'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_34[0]', '4b'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_35[0]', '5a'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_36[0]', '5b'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_37[0]', '6a'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_38[0]', '6b'),
            ButtonPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].c1_21[0]', '7_checkbox', '1'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_39[0]', '7'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_40[0]', '8'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_41[0]', '9'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_42[0]', '10'),
            TextPDFField('topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_43[0]', '11'),
            TextPDFField('topmostSubform[0].Page1[0].StandardDeductionBubble[0].f1_44[0]', '12a'),
            TextPDFField('topmostSubform[0].Page1[0].StandardDeductionBubble[0].f1_45[0]', '12b'),
            TextPDFField('topmostSubform[0].Page1[0].StandardDeductionBubble[0].f1_46[0]', '12c'),
            TextPDFField('topmostSubform[0].Page1[0].f1_47[0]', '13'),
            TextPDFField('topmostSubform[0].Page1[0].f1_48[0]', '14'),
            TextPDFField('topmostSubform[0].Page1[0].f1_49[0]', '15'),
#            ButtonPDFField('topmostSubform[0].Page2[0].c2_01[0]', '8814_required', '1'),
#            ButtonPDFField('topmostSubform[0].Page2[0].c2_02[0]', '4972_required', '1'),
#            ButtonPDFField('topmostSubform[0].Page2[0].c2_03[0]', 'other_form_required', '1'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_01[0]', 'other_form_writin'),
            TextPDFField('topmostSubform[0].Page2[0].f2_02[0]', '16'),
            TextPDFField('topmostSubform[0].Page2[0].f2_03[0]', '17'),
            TextPDFField('topmostSubform[0].Page2[0].f2_04[0]', '18'),
            TextPDFField('topmostSubform[0].Page2[0].f2_05[0]', '19'),
            TextPDFField('topmostSubform[0].Page2[0].f2_06[0]', '20'),
            TextPDFField('topmostSubform[0].Page2[0].f2_07[0]', '21'),
            TextPDFField('topmostSubform[0].Page2[0].f2_08[0]', '22'),
            TextPDFField('topmostSubform[0].Page2[0].f2_09[0]', '23'),
            TextPDFField('topmostSubform[0].Page2[0].f2_10[0]', '24'),
            TextPDFField('topmostSubform[0].Page2[0].f2_11[0]', '25a'),
            TextPDFField('topmostSubform[0].Page2[0].f2_12[0]', '25b'),
            TextPDFField('topmostSubform[0].Page2[0].f2_13[0]', '25c'),
            TextPDFField('topmostSubform[0].Page2[0].f2_14[0]', '25d'),
            TextPDFField('topmostSubform[0].Page2[0].f2_15[0]', '26'),
            TextPDFField('topmostSubform[0].Page2[0].f2_16[0]', '27a'),
            ButtonPDFField('topmostSubform[0].Page2[0].c2_04[0]', '27a_checkbox', '1'),
            TextPDFField('topmostSubform[0].Page2[0].f2_17[0]', '27b'),
            TextPDFField('topmostSubform[0].Page2[0].f2_18[0]', '27c'),
            TextPDFField('topmostSubform[0].Page2[0].f2_19[0]', '28'),
            TextPDFField('topmostSubform[0].Page2[0].f2_20[0]', '29'),
            TextPDFField('topmostSubform[0].Page2[0].f2_21[0]', '30'),
            TextPDFField('topmostSubform[0].Page2[0].f2_22[0]', '31'),
            TextPDFField('topmostSubform[0].Page2[0].f2_23[0]', '32'),
            TextPDFField('topmostSubform[0].Page2[0].f2_24[0]', '33'),
            TextPDFField('topmostSubform[0].Page2[0].f2_25[0]', '34'),
#            ButtonPDFField('topmostSubform[0].Page2[0].c2_05[0]', 'form_8888', '1'),
            TextPDFField('topmostSubform[0].Page2[0].f2_26[0]', '35a'),
            TextPDFField('topmostSubform[0].Page2[0].RoutingNo[0].f2_27[0]', '35b', max_length=9),
            ButtonPDFField('topmostSubform[0].Page2[0].c2_06[0]', '35c', '1'),
            ButtonPDFField('topmostSubform[0].Page2[0].c2_06[1]', '35c', '2', lambda s, v, f: not v),
            TextPDFField('topmostSubform[0].Page2[0].AccountNo[0].f2_28[0]', '35d', max_length=17),
            TextPDFField('topmostSubform[0].Page2[0].f2_29[0]', '36'),
            TextPDFField('topmostSubform[0].Page2[0].f2_30[0]', '37'),
            TextPDFField('topmostSubform[0].Page2[0].f2_31[0]', '38'),
            ButtonPDFField('topmostSubform[0].Page2[0].c2_7[0]', 'designee', '1'),
            ButtonPDFField('topmostSubform[0].Page2[0].c2_7[1]', 'designee', '2', value_fn=lambda s, v, f: not v),
#            TextPDFField('topmostSubform[0].Page2[0].f2_32[0]', 'designee_name'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_33[0]', 'designee_phone'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_34[0]', 'depin', max_length=5),
            TextPDFField('topmostSubform[0].Page2[0].f2_35[0]', 'occupation'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_36[0]', 'youpin', max_length=6),
            TextPDFField('topmostSubform[0].Page2[0].f2_37[0]', 'spouse_occupation'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_38[0]', 'spouse_pin', max_length=6),
            TextPDFField('topmostSubform[0].Page2[0].f2_39[0]', 'phone_number'),
            TextPDFField('topmostSubform[0].Page2[0].f2_40[0]', 'email_address'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_41[0]', 'preparer_name'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_42[0]', 'ptin', max_length=11),
#            ButtonPDFField('topmostSubform[0].Page2[0].c2_08[0]', 'preparer_self-employed', '1'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_43[0]', 'preparer_firm'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_44[0]', 'preparer_ph'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_45[0]', 'preparer_firm'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_46[0]', 'prep_ein', max_length=10),
        ]
        pdf_file = os.path.join(os.path.dirname(__file__), 'f1040.pdf')

        super().__init__(__class__, inputs, required_fields, [], pdf_fields=pdf_fields, pdf_file=pdf_file, **kwargs)

    def needs_filing(self, values):
        return True
