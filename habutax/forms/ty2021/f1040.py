import habutax.enum as enum
from habutax.form import Form
from habutax.inputs import *
from habutax.fields import *

from habutax.forms.ty2021.f1040_figure_tax import figure_tax

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
            BooleanInput('you_presidential_election', description="Check here if you want $3 to go to this fund. Checking a box below will not change your tax or refund."),
            BooleanInput('spouse_presidential_election', description="Check here if your spouse wants $3 to go to this fund. Checking a box below will not change your tax or refund."),
            BooleanInput('virtual_currency', description="At any time during 2021, did you receive, sell, exchange, or otherwise dispose of any financial interest in any virtual currency"),
            IntegerInput('number_dependents', description="How many dependents can you claim for 2021? (See Form 1040 instructions)"),
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
            BooleanInput('form_8949_required', description="Are you required to complete form 8949? See the line 7 instructions for Form 1040 if you are not sure."),
            BooleanInput('schedule_1_additional_income', description="Do you need to report additional income on Schedule 1? See the instructions for Schedule 1 for Form 1040 if you are not sure."),
            BooleanInput('schedule_1_income_adjustments', description="Do you need to report adjustments to income on Schedule 1? See the instructions for Schedule 1 for Form 1040 if you are not sure."),
            BooleanInput('itemize', description="Would you like to itemize? In most cases, your federal income tax will be less if you take the larger of your itemized deductions or standard deduction. Standard deductions by filing status: Single or Married filing separately: $12,550, Married filing jointly or Qualifying widow(er): $25,100, Head of household: $18,800."),
            FloatInput('charitable_contributions_std_ded', description=f'Enter the total amount of any charitable cash contributions made in {Form1040.tax_year}'),
            BooleanInput('uncommon_tax', description="Do you need to report a child's interest or dividends, need to make a section 962 election, recapture an education credit, have anything to do with a section 1291 fund, need to repay any excess advance payments of the health coverage tax credit from Form 8885, have tax from tax from Form 8978, line 14 (relating to partner's audit liability under section 6226), any net tax liability deferred under section 965(i), or a triggering event under section 965(i), have any income from farming or fishing, or want to claim the foreign earned income exclusion, housing exclusion, or housing deduction on Form 2555? These are not common... see the instructions for line 16, Form 1040."),
            BooleanInput('need_8615', description="Do you need to use Form 8615 to figure your tax? It must generally be used to figure the tax on your unearned income over $2,200 if you are under age 18, and in certain situations if you are older. See the instructions for line 16, form 1040."),
            BooleanInput('need_8962', description="If you, your spouse with whom you are filing a joint return, or your dependent was enrolled in health insurance coverage purchased from the Marketplace, were advance payments of the premium tax credit made for the coverage in 2021?"),
            BooleanInput('need_schedule_3_part_i', description="Do you want to claim any nonrefundable credits on Schedule 3, part I? These include credit for child and dependent care expenses, education credits, retirement savings, residential energy credits, among others."),
            BooleanInput('need_schedule_2', description="Do you need to pay any less common additional taxes (self-employment, unreported tip income, additional medicate tax, etc.)? See the Form 1040, Schedule 2 instructions for more details."),
        ]

        for n in range(4):
            inputs += [
                StringInput(f'dependent_{n}_name', description=f'Enter the first and last name for dependent {n+1}'),
                SSNInput(f'dependent_{n}_ssn', description=f'Enter the Social security number for dependent {n+1}'),
                StringInput(f'dependent_{n}_relationship', description=f'What is the relationship of {n+1} to you?'),
                BooleanInput(f'dependent_{n}_ctc', description=f'Does dependent {n+1} qualify for the child tax credit? See the "Who Qualifies as Your Dependent" section in the instructions for Form 1040.'),
                BooleanInput(f'dependent_{n}_odc', description=f'Does dependent {n+1} qualify for the credit for other dependents? See the "Who Qualifies as Your Dependent" section in the instructions for Form 1040.'),
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

        def schedule_1_additional_income(self, i, v):
            mort_int_refund = sum([v[f'1098:{n}.box_4'] for n in range(i['number_1098'])])
            state_income_refund = sum([v[f'1099-g:{n}.box_3'] for n in range(i['number_1099-g'])])
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

        required_fields = [
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
            FloatField('15', lambda s, i, v: max(0, v['11'] - v['14'])), # Taxable income
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
            FloatField('25c', lambda s, i, v: s.not_implemented()),
            FloatField('25d', lambda s, i, v: v['25a'] + v['25b'] + v['25c']),
            # TODO 26
            # TODO 27
#            FloatField('28', line_28),
        ]
        for n in range(4):
            required_fields += [
                StringField(f'dependent_{n}_name', lambda s, i, v, n=n: i[f'dependent_{n}_name'] if n < i['number_dependents'] else None),
                StringField(f'dependent_{n}_ssn', lambda s, i, v, n=n: i[f'dependent_{n}_ssn'] if n < i['number_dependents'] else None),
                StringField(f'dependent_{n}_relationship', lambda s, i, v, n=n: i[f'dependent_{n}_relationship'] if n < i['number_dependents'] else None),
                BooleanField(f'dependent_{n}_ctc', lambda s, i, v, n=n: i[f'dependent_{n}_ctc'] if n < i['number_dependents'] else None),
                BooleanField(f'dependent_{n}_odc', lambda s, i, v, n=n: i[f'dependent_{n}_odc'] if n < i['number_dependents'] and not v[f'dependent_{n}_ctc'] else None),
            ]
        super().__init__(__class__, inputs, required_fields, [], **kwargs)
