from collections.abc import Mapping

from pytax.inputs import *
from pytax.fields import *

class Form(object):
    def __init__(self,
                 child_cls,
                 inputs,
                 required_fields,
                 optional_fields,
                 instance=None):

        self._name = child_cls.form_name
        assert("." not in self._name)
        self._tax_year = child_cls.tax_year
        self._inputs = inputs
        self._required_fields = required_fields
        self._optional_fields = optional_fields
        self._instance = instance

        for i in self._inputs:
            i.__form_init__(self)
        for f in self._required_fields + self._optional_fields:
            f.__form_init__(self)

    def name(self):
        return self._name

    def inputs(self):
        return self._inputs

    def required_fields(self):
        return self._required_fields

    def fields(self):
        return self.required_fields() + self._optional_fields

class FormAccessor(Mapping):
    def __init__(self, mapping, form):
        self.form = form
        self.mapping = mapping

    def __getitem__(self, key):
        if "." not in key:
            key = f'{self.form.name()}.{key}'
        return self.mapping[key]

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)

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
            IntegerInput('tax-exempt_interest'),
            IntegerInput('taxable_interest'),
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
            SimpleField('2a', lambda s, i, v: i['tax-exempt_interest']),
            SimpleField('2b', lambda s, i, v: i['taxable_interest']),
            SimpleField('3a', lambda s, i, v: i['qualified_dividends']),
            SimpleField('3b', lambda s, i, v: i['ordinary_dividends']),
            SimpleField('4a', lambda s, i, v: i['ira_distributions']),
            SimpleField('4b', lambda s, i, v: i['ira_taxable_amount']),
            SimpleField('5a', lambda s, i, v: i['pensions_annuities']),
            SimpleField('5b', lambda s, i, v: i['pensions_annuities_taxable_amount']),
            SimpleField('6a', lambda s, i, v: i['social_security_benefits']),
            SimpleField('6b', lambda s, i, v: i['social_security_taxable_amount']),
            #Add lines 1, 2b, 3b, 4b, 5b, 6b, 7, and 8. This is your total income
            SimpleField('9', lambda s, i, v: v['1'] + v['2b'] + v['3b'] + v['4b'] + v['5b'] + v['6b'] + v['7'] + v['8']),
        ]
        super().__init__(__class__, inputs, fields, [], **kwargs)

available = {
    2021: [
        Form1040,
    ]
}
