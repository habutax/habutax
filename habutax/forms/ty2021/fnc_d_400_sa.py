import os

from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *
from habutax.pdf_fields import *

class FormNCD400SA(Form):
    form_name = "nc_d-400_sa"
    tax_year = 2021
    description = "D-400 Schedule A"
    long_description = "N.C. Itemized Deductions"
    jurisdiction = Jurisdiction.NC
    sequence_no = 2

    def __init__(self, **kwargs):
        inputs = [
            FloatInput('claim_of_right_income', description="Enter any 'Repayment of Claim of Right Income' which you can claim a NC deduction for (this is not common). See the instructions for NC D-400 Schedule A, line 8 for more information"),
        ]

        def nc_standard_deduction(self, i, v):
            statuses = self.form('1040').FILING_STATUS
            if i['1040.filing_status'] in [statuses.MarriedFilingJointly, statuses.QualifyingWidowWidower]:
                return 21500.0
            elif i['1040.filing_status'] == statuses.HeadOfHousehold:
                return 16125.0
            elif i['1040.filing_status'] == statuses.Single:
                return 10750.0
            elif i['1040.filing_status'] == statuses.MarriedFilingSeparately and not i['1040.standard_deduction_exceptions']:
                return 10750.0
            self.not_implemented()

        def line_1(self, i, v):
            mortgage_interest_points = sum([v[f'1098:{n}.box_1'] for n in range(i['1040.number_1098'])])
            mortgage_interest_points += sum([v[f'1098:{n}.box_6'] for n in range(i['1040.number_1098'])])
            return mortgage_interest_points

        def real_estate_tax_limit(self, i, v):
            return 5000.0 if i['1040.filing_status'] == self.form('1040').FILING_STATUS.MarriedFilingSeparately else 10000.0

        optional_fields = [
            FloatField('nc_standard_deduction', nc_standard_deduction, places=0),
            FloatField('1', line_1, places=0),
            FloatField('2', lambda s, i, v: min(i['1040_sa.state_local_real_estate_taxes'], real_estate_tax_limit(s, i, v)), places=0),
            FloatField('3', lambda s, i, v: v['1'] + v['2'], places=0),
            FloatField('4', lambda s, i, v: 20000.0, places=0),
            FloatField('5', lambda s, i, v: min(v['3'], v['4']), places=0),
            FloatField('6', lambda s, i, v: min(i['1040_sa.charitable_cash_check'] + i['1040_sa.charitable_other_than_cash_check'], v['1040.11'] * 0.6), places=0),
            FloatField('7a', lambda s, i, v: i['1040_sa.medical_dental_expenses'], places=0),
            FloatField('7b', lambda s, i, v: v['nc_d-400.6'], places=0),
            FloatField('7c', lambda s, i, v: max(0.0, v['7b'] * 0.075), places=0),
            FloatField('7d', lambda s, i, v: 0.0 if v['7c'] > v['7a'] else v['7a'] - v['7c'], places=0),
            FloatField('8', lambda s, i, v: i['claim_of_right_income'], places=0),
            FloatField('9', lambda s, i, v: 0.0, places=0), # "reserved for future use"
            FloatField('10', lambda s, i, v: v['5'] + v['6'] + v['7d'] + v['8'] + v['9'], places=0),
        ]

        required_fields = [
            StringField('last_name', lambda s, i, v: i['1040.last_name'][:10]),
            StringField('ssn', lambda s, i, v: i['1040.you_ssn'][:3] + "-" + i['1040.you_ssn'][3:5] + "-" + i['1040.you_ssn'][5:]),
            FloatField('deduction', lambda s, i, v: max(v['nc_standard_deduction'], v['10']), places=0),
        ]

        pdf_fields = [
            TextPDFField('y_d400_sch_a_wf_lname', 'last_name', max_length=10),
            TextPDFField('y_d400_sch_a_wf_ssn', 'ssn'),
            TextPDFField('y_d400_sch_a_wf_li1', '1', max_length=8),
            TextPDFField('y_d400_sch_a_wf_li2', '2', max_length=8),
            TextPDFField('y_d400_sch_a_wf_li3', '3', max_length=8),
#            TextPDFField('y_d400_sch_a_wf_li4', '20000'),
            TextPDFField('y_d400_sch_a_wf_li5', '5', max_length=8),
            TextPDFField('y_d400_sch_a_wf_li6', '6', max_length=8),
            TextPDFField('y_d400_sch_a_wf_li7a', '7a', max_length=8),
            TextPDFField('y_d400_sch_a_wf_li7b', '7b', max_length=9),
            TextPDFField('y_d400_sch_a_wf_li7c', '7c', max_length=8),
            TextPDFField('y_d400_sch_a_wf_li7d', '7d', max_length=8),
            TextPDFField('y_d400_sch_a_wf_li8', '8', max_length=8),
#            TextPDFField('y_d400_sch_a_wf_reserved', 'reserved_for_future_use', max_length=30),
#            TextPDFField('y_d400_sch_a_wf_li9', '9', max_length=8),
            TextPDFField('y_d400_sch_a_wf_li10', '10', max_length=8),
            #OptionlessButtonPDFField('z_d400schswf_clear', 'unknown'),
            #OptionlessButtonPDFField('z_d400_sch_a_wf_print', 'unknown'),
        ]
        pdf_file = os.path.join(os.path.dirname(__file__), 'fnc_d-400_sa.pdf')

        super().__init__(__class__, inputs, required_fields, optional_fields, pdf_fields=pdf_fields, pdf_file=pdf_file, **kwargs)

    def needs_filing(self, values):
        if 'nc_d-400_sa.deduction' not in values:
            return False
        return values['nc_d-400_sa.10'] > values['nc_d-400_sa.nc_standard_deduction']
