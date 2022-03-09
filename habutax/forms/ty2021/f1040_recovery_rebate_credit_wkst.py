from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *

class Form1040RecoveryRebateCreditWkst(Form):
    form_name = "1040_recovery_rebate_credit_wkst"
    tax_year = 2021
    description = "Recovery Rebate Credit Worksheet (Form 1040)"
    long_description = "Line 30"
    jurisdiction = Jurisdiction.US

    def __init__(self, **kwargs):
        inputs = [
            BooleanInput('ssn_before_due_date', description="Does your 2021 return include a social security number that was issued on or before the due date of your 2021 return (including extensions) for you and, if filing a joint return, your spouse?"),
            BooleanInput('armed_forces', description="Was at least one of you or your spouse a member of the U.S. Armed Forces at any time during 2021, and does at least one of you have a social security number that was issued on or before the due date of your 2021 return (including extensions)?"),
            BooleanInput('either_ssn_before_due_date', description="Does one of you or your spouse have a social security number that was issued on or before the due date of your 2021 return (including extensions)?"),
            IntegerInput('dependents_ssn_before_due_date', description="How many dependents listed in the Dependents section on page 1 of Form 1040 or 1040-SR have a social security number that was issued on or before the due date of your 2021 return (including extensions) or an adoption taxpayer identification number?"),
            FloatInput('eip_3_amount', description="Enter the amount, if any, of EIP 3 that was issued to you. If filing a joint return, include the amount, if any, of your spouse’s EIP 3. You may refer to Notice 1444-C or your tax account information at IRS.gov/Account for the amount to enter here. Don’t include on line 13 any amount you received but later returned to the IRS."),
        ]

        def can_take_credit(self, i, v):
            if v['1']:
                return False
            if not v['2']:
                if i['1040.filing_status'] is self.form('1040').FILING_STATUS.MarriedFilingJointly:
                    if not v['3'] and not v['4'] and not v['5']:
                        return False
                elif not v['5']:
                    return False
            if v['10_checkbox']:
                return False
            return True

        def line_6(self, i, v):
            amount = 1400.0
            if i['1040.filing_status'] is self.form('1040').FILING_STATUS.MarriedFilingJointly and (v['2'] or v['3']):
                amount = 2800.0
            if not v['2']:
                if i['1040.filing_status'] is self.form('1040').FILING_STATUS.MarriedFilingJointly:
                    if not v['3'] and not v['4'] and v['5']:
                        amount = 0.0
                elif v['5']:
                    amount = 0.0
            return amount

        def line_9_checkbox(self, i, v):
            statuses = self.form('1040').FILING_STATUS
            amount = 0
            if i['1040.filing_status'] in [statuses.Single, statuses.MarriedFilingSeparately]:
                amount = 75000.0
            elif i['1040.filing_status'] in [statuses.MarriedFilingJointly, statuses.QualifyingWidowWidower]:
                amount = 150000.0
            elif i['1040.filing_status'] == statuses.HeadOfHousehold:
                amount = 112.500
            else:
                self.not_implemented()
            return v['1040.11'] > amount

        def line_10_amount(self, i, v):
            statuses = self.form('1040').FILING_STATUS
            if i['1040.filing_status'] in [statuses.Single, statuses.MarriedFilingSeparately]:
                return 80000.0
            elif i['1040.filing_status'] in [statuses.MarriedFilingJointly, statuses.QualifyingWidowWidower]:
                return 160000.0
            elif i['1040.filing_status'] == statuses.HeadOfHousehold:
                return 120000.0
            else:
                self.not_implemented()

        def line_10_checkbox(self, i, v):
            return v['9'] > line_10_amount(self, i, v)

        def line_11(self, i, v):
            statuses = self.form('1040').FILING_STATUS
            if i['1040.filing_status'] in [statuses.Single, statuses.MarriedFilingSeparately]:
                amount = 5000.0
            elif i['1040.filing_status'] in [statuses.MarriedFilingJointly, statuses.QualifyingWidowWidower]:
                amount = 10000.0
            elif i['1040.filing_status'] == statuses.HeadOfHousehold:
                amount = 75000.0
            else:
                self.not_implemented()
            return v['10'] / amount

        optional_fields = [
            BooleanField('1', lambda s, i, v: False if i['1040.filing_status'] is s.form('1040').FILING_STATUS.MarriedFilingJointly else i['1040.claimed_as_dependent']),
            BooleanField('2', lambda s, i, v: i['ssn_before_due_date']),
            BooleanField('3', lambda s, i, v: i['armed_forces']),
            BooleanField('4', lambda s, i, v: i['either_ssn_before_due_date']),
            BooleanField('5', lambda s, i, v: i['dependents_ssn_before_due_date'] > 0),
            FloatField('6', line_6),
            FloatField('7', lambda s, i, v: 1400.0 * i['dependents_ssn_before_due_date']),
            FloatField('8', lambda s, i, v: v['6'] + v['7']),
            BooleanField('9_checkbox', line_9_checkbox),
            FloatField('9', lambda s, i, v: v['1040.11']),
            BooleanField('10_checkbox', line_10_checkbox),
            FloatField('10', lambda s, i, v: s.not_implemented() if v['9'] > line_10_amount(s, i, v) else line_10_amount(s, i, v) - v['9']),
            FloatField('11', line_11),
            FloatField('12', lambda s, i, v: (v['8'] * v['11']) if v['9_checkbox'] else v['8']),
            FloatField('13', lambda s, i, v: i['eip_3_amount']),
            FloatField('14', lambda s, i, v: max(0.0, v['12'] - v['13'])),
            FloatField('credit', lambda s, i, v: v['14'] if can_take_credit(s, i, v) else None),
        ]

        super().__init__(__class__, inputs, [], optional_fields, **kwargs)

    def needs_filing(self, values):
        return False
