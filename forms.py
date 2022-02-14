from inputs import *
from fields import *

class Form(object):
    def __init__(self, inputs, required_fields, optional_fields=[]):
        self._inputs = inputs
        self._required_fields = required_fields
        self._optional_fields = optional_fields

    def inputs(self):
        return self._inputs

    def required_fields(self):
        return self._required_fields

    def fields(self):
        return self.required_fields() + self._optional_fields

class Form1040(Form):
    FILING_STATUS = EnumInput('f1040', 'filing_status', ['Single', 'MarriedFilingJointly', 'MarriedFilingSeparately', 'HeadOfHousehold', 'QualifyingWidow(er)'], description="Filing Status")
    INPUTS = [
        FILING_STATUS,
        StringInput('f1040', 'first_name_middle_initial', description="Your first name and middle initial"),
        StringInput('f1040', 'last_name', description="Your last name"),
        StringInput('f1040', 'spouse_first_name_middle_initial', description="If joint return, spouse's first name and middle initial"),
        StringInput('f1040', 'spouse_last_name', description="If joint return, spouse's last name"),
        BooleanInput('f1040', 'you_presidential_election', description="Check here if you, or your spouse if filing jointly, want $3 to go to this fund. Checking a box below will not change your tax or refund."),
        BooleanInput('f1040', 'you_presidential_election', description="Check here if you, or your spouse if filing jointly, want $3 to go to this fund. Checking a box below will not change your tax or refund."),
        IntegerInput('f1040', 'wages_salaries_tips', description="Wages, salaries, tips, etc. Attach Form(s) W-2"),
        IntegerInput('f1040', 'tax-exempt_interest'),
        IntegerInput('f1040', 'taxable_interest'),
        IntegerInput('f1040', 'qualified_dividends'),
        IntegerInput('f1040', 'ordinary_dividends'),
        IntegerInput('f1040', 'ira_distributions'),
        IntegerInput('f1040', 'ira_taxable_amount'),
        IntegerInput('f1040', 'pensions_annuities'),
        IntegerInput('f1040', 'pensions_annuities_taxable_amount'),
        IntegerInput('f1040', 'social_security_benefits'),
        IntegerInput('f1040', 'social_security_taxable_amount'),
    ]
    def __init__(self):
        fields = [
            SimpleField('1040.first_name', lambda i, v: i['first_name_middle_initial']),
            SimpleField('1040.last_name', lambda i, v: i['last_name']),
            SimpleField('1040.spouse_first_name', lambda i, v: i['spouse_first_name_middle_initial'] if i['filing_status'] == Form1040.FILING_STATUS.MarriedFilingJointly else ""),
            SimpleField('1040.spouse_last_name', lambda i, v: i['spouse_last_name'] if i['filing_status'] == Form1040.FILING_STATUS.MarriedFilingJointly else ""),
            SimpleField('1040.spouse_last_name', lambda i, v: i['last_name']),
            SimpleField('1040.1', lambda i, v: i['wages_salaries_tips']),
            SimpleField('1040.2a', lambda i, v: i['tax-exempt_interest']),
            SimpleField('1040.2b', lambda i, v: i['taxable_interest']),
            SimpleField('1040.3a', lambda i, v: i['qualified_dividends']),
            SimpleField('1040.3b', lambda i, v: i['ordinary_dividends']),
            SimpleField('1040.4a', lambda i, v: i['ira_distributions']),
            SimpleField('1040.4b', lambda i, v: i['ira_taxable_amount']),
            SimpleField('1040.5a', lambda i, v: i['pensions_annuities']),
            SimpleField('1040.5b', lambda i, v: i['pensions_annuities_taxable_amount']),
            SimpleField('1040.6a', lambda i, v: i['social_security_benefits']),
            SimpleField('1040.6b', lambda i, v: i['social_security_taxable_amount']),
            #Add lines 1, 2b, 3b, 4b, 5b, 6b, 7, and 8. This is your total income
            SimpleField('1040.9', lambda i, v: v['1040.1'] + v['1040.2b'] + v['1040.3b'] + v['1040.4b'] + v['1040.5b'] + v['1040.6b'] + v['1040.7'] + v['1040.8']),
        ]
        super().__init__(Form1040.INPUTS, fields)
