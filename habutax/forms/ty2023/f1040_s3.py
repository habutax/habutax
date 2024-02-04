import os

from habutax.enum import filing_status
from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *
from habutax.pdf_fields import *

class Form1040S3(Form):
    form_name = "1040_s3"
    tax_year = 2023
    description = "Schedule 3 (Form 1040)"
    long_description = "Additional Credits and Payments"
    jurisdiction = Jurisdiction.US
    sequence_no = 3

    def __init__(self, **kwargs):
        thresholds = {
            # Must file Form 1116 if your total foreign tax was more than this
            # threshold. Form 1040, Schedule 3, Line 1 instructions.
            'form_1116_foreign_tax': {
                filing_status.MarriedFilingJointly:  600.0,
                (status.Single, status.MarriedFilingSeparately,
                 status.QualifyingSurvivingSpouse,
                 filing_status.HeadOfHousehold):     300.0,
            },
            # Cannot claim Retirement Savings Contributions Credit if your
            # income is over this threshold. Form 1040, Schedule 3, line 4
            # instructions
            'retirement_savings_limit': {
                filing_status.MarriedFilingJointly: 73000.0,
                filing_status.HeadOfHousehold:      54750.0,
                (status.Single, status.MarriedFilingSeparately,
                 status.QualifyingSurvivingSpouse): 36500.0
            },
        }

        inputs = [
            BooleanInput('other_foreign_gross_income', description="Do you have any foreign source gross income *not* from interest and dividends or any foreign tax paid on that income not reported to you on Form 1099-INT, Form 1099-DIV?"),
            BooleanInput('child_dependent_care', description="Did you pay expenses for the care of a qualifying individual (child or other dependent) to enable you (and your spouse, if filing a joint return) to work or actively look for work?"),
            BooleanInput('education_credit', description="Did you (or your dependent) pay qualified expenses in 2023 for yourself, your spouse, or your dependent to enroll in or attend an eligible educational institution? If so, do you need to claim an education credit on Form 8863?"),
            BooleanInput('retirement_savings_contributions', description="Did you, or your spouse if filing jointly, make (a) contributions, other than rollover contributions, to a traditional or Roth IRA; (b) elective deferrals to a 401(k) or 403(b) plan (including designated Roth contributions) or to a governmental 457, SEP, or SIMPLE plan; (c) voluntary employee contributions to a qualified retirement plan (including the federal Thrift Savings Plan); (d) contributions to a 501(c)(18)(D) plan; or (e) contributions to an ABLE account by the designated beneficiary, as defined in section 529A?"),
            BooleanInput('residential_energy_credit', description="Did you pay for any energy-efficient upgrades to your home in 2023 or can you claim any clean energy credits? This might be things like installing solar panels, wind energy installations, adding insulation or high-efficiency HVAC units."),
            BooleanInput('other_nonrefundable_credits', description="Do you have any less common nonrefundable credits to claim? These include general business credits (Form 3800), prior year minimum tax (Form 8801), adoption credit (Form 8839), credit for the elderly or disabled (Schedule R), alternative motor vehicle credit (Form 8910), qualified plug-in motor vehicle credit (Form 8936), mortgage interest credit (Form 8396), District of Columbia first-time homebuyer credit (Form 8859), qualified electric vehicle credit (Form 8834), alternative fuel vehicle refueling property credit (Form 8911), credit to holders of tax credit bonds (Form 8912), amount on Form 8978, line 14 (reporting for partnership income), credit for previously owned clean vehicles (Form 8936), or any other nonrefundable tax credits."),
        ]

        def line_1(self, i, v):
            foreign_tax = float(sum([v[f'1099-int:{n}.box_6'] for n in range(i['1040.number_1099-int'])]))
            foreign_tax += float(sum([v[f'1099-div:{n}.box_7'] for n in range(i['1040.number_1099-div'])]))
            if i['other_foreign_gross_income'] or foreign_tax > s.threshold('form_1116_foreign_tax', i['1040.filing_status']):
                return self.not_implemented()
            return foreign_tax if foreign_tax > 0.001 else None

        optional_fields = [
            FloatField('1', line_1),
            FloatField('2', lambda s, i, v: s.not_implemented() if i['child_dependent_care'] else None), # Form 2441, line 11
            FloatField('3', lambda s, i, v: s.not_implemented() if i['education_credit'] else None), # Form 8863, line 19
            FloatField('4', lambda s, i, v: s.not_implemented() if v['1040.11'] <= s.threshold('retirement_savings_limit', i['1040.filing_status']) and i['retirement_savings_contributions'] else None), # Form 8880
            FloatField('5a', lambda s, i, v: s.not_implemented() if i['residential_energy_credit'] else None), # Form 5695
            FloatField('5b', lambda s, i, v: s.not_implemented() if i['residential_energy_credit'] else None), # Form 5695
            FloatField('6a', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Form 3800
            FloatField('6b', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Form 8801
            FloatField('6c', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Form 8839
            FloatField('6d', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Form Schedule R
            FloatField('6e', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Form 8901
            FloatField('6f', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Form 8936
            FloatField('6g', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Form 8396
            FloatField('6h', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Form 8859
            FloatField('6i', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Form 8834
            FloatField('6j', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Form 8911
            FloatField('6k', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Form 8912
            FloatField('6l', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Form 8978, line 14
            FloatField('6m', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Form 8936
            FloatField('6z', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Other nonrefundable credits
            FloatField('7', lambda s, i, v: sum([v[f'6{l}'] for l in "abcdefghijklmz"])),
            FloatField('8', lambda s, i, v: sum([v[f'{n}'] for n in range(1, 4+1)]) + v['5a'] + v['5b'] + v['7']),
        ]
        required_fields = [
            StringField('6z_type', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Type of any nonrefundable credits
        ]

        pdf_fields = [
#            TextPDFField('topmostSubform[0].Page1[0].f1_01[0]', '1040.full_names'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_02[0]', '1040.you_ssn', max_length=11),
#            TextPDFField('topmostSubform[0].Page1[0].f1_03[0]', '1'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_04[0]', '2'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_05[0]', '3'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_06[0]', '4'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_07[0]', '5'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_08[0]', '6a'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_09[0]', '6b'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_10[0]', '6c'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_11[0]', '6d'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_12[0]', '6e'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_13[0]', '6f'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_14[0]', '6g'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_15[0]', '6h'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_16[0]', '6i'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_17[0]', '6j'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_18[0]', '6k'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_19[0]', '6l'),
#            TextPDFField('topmostSubform[0].Page1[0].Line6z_ReadOrder[0].f1_20[0]', '6z_type'),
#            TextPDFField('topmostSubform[0].Page1[0].Line6z_ReadOrder[0].f1_21[0]', '6z_type'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_22[0]', '6z'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_23[0]', '7'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_24[0]', '8'),
##            TextPDFField('topmostSubform[0].Page2[0].f2_01[0]', '9'),
##            TextPDFField('topmostSubform[0].Page2[0].f2_02[0]', '10'),
##            TextPDFField('topmostSubform[0].Page2[0].f2_03[0]', '11'),
##            TextPDFField('topmostSubform[0].Page2[0].f2_04[0]', '12'),
##            TextPDFField('topmostSubform[0].Page2[0].Line13_ReadOrder[0].f2_05[0]', '13a'),
##            TextPDFField('topmostSubform[0].Page2[0].f2_06[0]', '13b'),
##            TextPDFField('topmostSubform[0].Page2[0].f2_07[0]', '13c'), #"Reserved for future use"
##            TextPDFField('topmostSubform[0].Page2[0].f2_08[0]', '13d'),
##            TextPDFField('topmostSubform[0].Page2[0].f2_09[0]', '13e'), #"Reserved for future use"
##            TextPDFField('topmostSubform[0].Page2[0].f2_10[0]', '13f'),
##            TextPDFField('topmostSubform[0].Page2[0].f2_11[0]', '13g'), #"Reserved for future use"
##            TextPDFField('topmostSubform[0].Page2[0].f2_12[0]', '13h'),
##            TextPDFField('topmostSubform[0].Page2[0].Line13z_ReadOrder[0].f2_14[0]', '13z_type'),
##            TextPDFField('topmostSubform[0].Page2[0].f2_15[0]', '13z'),
##            TextPDFField('topmostSubform[0].Page2[0].f2_16[0]', '14'),
##            TextPDFField('topmostSubform[0].Page2[0].f2_17[0]', '15'),
        ]
        pdf_file = os.path.join(os.path.dirname(__file__), 'f1040s3.pdf')

        super().__init__(__class__, inputs, required_fields, optional_fields,
                         thresholds=thresholds, pdf_fields=pdf_fields,
                         pdf_file=pdf_file, **kwargs)

    def needs_filing(self, values):
        return True
