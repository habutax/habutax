import os

from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *

class FormNCD400ChildDeductionWkst(Form):
    form_name = "nc_d-400_child_deduction_wkst"
    tax_year = 2021
    description = "Child Deduction Worksheet (NC Form D-400)"
    long_description = "Line 10b"
    jurisdiction = Jurisdiction.NC

    def __init__(self, **kwargs):
        inputs = [
        ]

        def deduction_per_child(self, i, v):
            statuses = self.form('1040').FILING_STATUS
            status = i['1040.filing_status']
            federal_agi = v['2']

            if status in [statuses.MarriedFilingJointly, statuses.QualifyingWidowWidower]:
                if federal_agi <= 40000:
                    return 2500.0
                elif federal_agi <= 60000:
                    return 2000.0
                elif federal_agi <= 80000:
                    return 1500.0
                elif federal_agi <= 100000:
                    return 1000.0
                elif federal_agi <= 120000:
                    return 500.0
                else:
                    return 0.0
            elif status == statuses.HeadOfHousehold:
                if federal_agi <= 30000:
                    return 2500.0
                elif federal_agi <= 45000:
                    return 2000.0
                elif federal_agi <= 60000:
                    return 1500.0
                elif federal_agi <= 75000:
                    return 1000.0
                elif federal_agi <= 90000:
                    return 500.0
                else:
                    return 0.0
            elif status in [statuses.Single, statuses.MarriedFilingSeparately]:
                if federal_agi <= 20000:
                    return 2500.0
                elif federal_agi <= 30000:
                    return 2000.0
                elif federal_agi <= 40000:
                    return 1500.0
                elif federal_agi <= 50000:
                    return 1000.0
                elif federal_agi <= 60000:
                    return 500.0
                else:
                    return 0.0
            else:
                self.not_implemented()

        optional_fields = [
            StringField('1', lambda s, i, v: str(i['1040.filing_status'])),
            FloatField('2', lambda s, i, v: v['nc_d-400.6'], places=0),
            IntegerField('3', lambda s, i, v: sum([v[f'1040.dependent_{n}_ctc'] for n in range(i['1040.number_dependents'])])),
            FloatField('4', deduction_per_child, places=0),
            FloatField('5', lambda s, i, v: v['3'] * v['4'], places=0),
        ]

        required_fields = [
        ]

        super().__init__(__class__, inputs, required_fields, optional_fields, **kwargs)

    def needs_filing(self, values):
        return False
