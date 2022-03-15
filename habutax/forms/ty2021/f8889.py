import os

from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *
from habutax.pdf_fields import *

class Form8889(Form):
    form_name = "8889"
    tax_year = 2021
    description = "Form 8889"
    long_description = "Health Savings Accounts (HSAs)"
    jurisdiction = Jurisdiction.US
    sequence_no = 52
    valid_instances = ['you', 'spouse']

    def __init__(self, **kwargs):
        instance = kwargs['instance']
        assert(instance in ['you', 'spouse'])
        you = "you" if instance == "you" else "your spouse"
        your = "your" if instance == "you" else "your spouse's"
        your_spouses = "your spouse's" if instance == "you" else "your"

        inputs = [
            BooleanInput('part_2_needed', description=f'Do {you} need to fill out part 2 of Form 8999? Part 2 is used to report HSA distributions.'),
            BooleanInput('part_3_needed', description=f'Do {you} need to fill out part 3 of Form 8999? Part 3 is used to report cases when you fail to maintain high-deductible health plan (HDHP) coverage for the entire year.  See instructions.'),
            BooleanInput('hdhp_plan_family', description=f'Were you covered under a *family* high-deductible health plan (HDHP) during 2021 (as opposed to self-only coverage)? If {you} were covered, or considered covered, by a self-only high-deductible health plan (HDHP) and a family HDHP at different times during the year, answer "yes" only if the family plan was in effect for a longer period. If {you} were covered by both a self-only HDHP and a family HDHP at the same time, {you} are treated as having family coverage during that period. If, on the first day of the last month of {your} tax year (December 1 for most taxpayers), {you} had family coverage, answer "yes". Were you covered under a high-deductible *family* plan during 2021?'),
            FloatInput('hsa_contributions', description=f'Enter HSA contributions {you} made for 2021 (or those made on {your} behalf), including those made from January 1, 2022, through April 15, 2022, that were for 2021. Do not include employer contributions, contributions through a cafeteria plan, or rollovers. See instructions for Form 8889, line 2.'),
            BooleanInput('age_under_55', description=f'Were {you} under the age of 55 at the end of 2021?'),
            BooleanInput('hsa_full_year', description=f'Did {you} have a HDHP medical plan for the first day of every month during the 2021 year?'),
            FloatInput('archer_msa', description=f'Enter the amount {you} and {your} employer contributed to {your} Archer MSAs for 2021 from Form 8853, lines 1 and 2. If you or your spouse had family coverage under an HDHP at any time during 2021, also include any amount contributed to {your_spouses} Archer MSAs'),
            BooleanInput('qualified_distribution', description=f'Did {you} take a distribution from {your} traditional IRA or Roth IRA to {your} HSA in a direct trustee-to-trustee transfer?'),
            FloatInput('employer_contribution', description=f'Employer contributions made to {your} HSAs for 2021? NOTE: This number should match the sum of all {your} your forms W-2, box 12, code W.'),
        ]

        def calc_contribution_max(self, i, v):
            if i['age_under_55'] and i['hsa_full_year']:
                return 7200 if v['1'] else 3600
            else:
                self.not_implemented()

        # All fields are optional. Form 1040s1 13 should include both you and
        # your spouse hsa_deductions
        optional_fields = [
            BooleanField('1', lambda s, i, v: i['hdhp_plan_family']),
            FloatField('2', lambda s, i, v: i['hsa_contributions']),
            IntegerField('3', calc_contribution_max),
            FloatField('4', lambda s, i, v:  self.not_implemented() if i['archer_msa'] else 0.0),
            FloatField('5', lambda s, i, v: max(v['3'] - v['4'], 0.0)),
            FloatField('6', lambda s, i, v: self.not_implemented() if i['1040_s1.hsa_contribution_you'] and i['1040_s1.hsa_contribution_spouse'] and i['hdhp_plan_family'] else v['5']),
            FloatField('7', lambda s, i, v: self.not_implemented() if not i['age_under_55'] and (i['hdhp_plan_family'] or i['8889:spouse.hdhp_plan_family']) else None),
            FloatField('8', lambda s, i, v: v['6'] + v['7']),
            FloatField('9', lambda s, i, v: i['employer_contribution']),
            FloatField('10', lambda s, i, v: self.not_implemented() if i['qualified_distribution'] else None),
            FloatField('11', lambda s, i, v: v['9'] + v['10']),
            FloatField('12', lambda s, i, v: max(v['8'] - v['11'], 0.0)),
            FloatField('13', lambda s, i, v: min(v['2'], v['12'])),
            FloatField('hsa_deduction', lambda s, i, v: self.not_implemented() if i['part_2_needed'] or i['part_3_needed'] or v['2'] > v['13'] else v['13']),
        ]

        def name_field(self, i, v):
            if self.form().instance() == 'spouse':
                return f'{v["1040.spouse_first_name"]} {v["1040.spouse_last_name"]}'
            else:
                return f'{v["1040.first_name"]} {v["1040.last_name"]}'

        required_fields = [
            StringField('name', name_field),
            StringField('ssn', lambda s, i, v: v[f'1040.{s.form().instance()}_ssn']),
        ]

        pdf_fields = [
            TextPDFField('topmostSubform[0].Page1[0].f1_01[0]', 'name'),
            TextPDFField('topmostSubform[0].Page1[0].f1_02[0]', 'ssn', max_length=11),
            ButtonPDFField('topmostSubform[0].Page1[0].c1_1[0]', '1', '1', value_fn=lambda s, v, f: not v),
            ButtonPDFField('topmostSubform[0].Page1[0].c1_1[1]', '1', '2'),
            TextPDFField('topmostSubform[0].Page1[0].f1_03[0]', '2'),
            TextPDFField('topmostSubform[0].Page1[0].f1_04[0]', '3'),
            TextPDFField('topmostSubform[0].Page1[0].f1_05[0]', '4'),
            TextPDFField('topmostSubform[0].Page1[0].f1_06[0]', '5'),
            TextPDFField('topmostSubform[0].Page1[0].f1_07[0]', '6'),
            TextPDFField('topmostSubform[0].Page1[0].f1_08[0]', '7'),
            TextPDFField('topmostSubform[0].Page1[0].f1_09[0]', '8'),
            TextPDFField('topmostSubform[0].Page1[0].f1_10[0]', '9'),
            TextPDFField('topmostSubform[0].Page1[0].f1_11[0]', '10'),
            TextPDFField('topmostSubform[0].Page1[0].f1_12[0]', '11'),
            TextPDFField('topmostSubform[0].Page1[0].f1_13[0]', '12'),
            TextPDFField('topmostSubform[0].Page1[0].f1_14[0]', '13'),
            # parts II, III unimplemented
#            TextPDFField('topmostSubform[0].Page1[0].f1_15[0]', '14a'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_16[0]', '14b'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_17[0]', '14c'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_18[0]', '15'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_19[0]', '16'),
#            ButtonPDFField('topmostSubform[0].Page1[0].c1_2[0]', '17a', '1'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_20[0]', '17b'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_21[0]', '18'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_22[0]', '19'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_23[0]', '20'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_24[0]', '21'),
        ]
        pdf_file = os.path.join(os.path.dirname(__file__), 'f8889.pdf')

        super().__init__(__class__, inputs, required_fields, optional_fields, pdf_fields=pdf_fields, pdf_file=pdf_file, **kwargs)

    def needs_filing(self, values):
        return True
