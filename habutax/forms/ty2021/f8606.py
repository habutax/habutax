import os

from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *
from habutax.pdf_fields import *

class Form8606(Form):
    form_name = "8606"
    tax_year = 2021
    description = "Form 8606"
    long_description = "Nondeductible IRAs"
    jurisdiction = Jurisdiction.US
    sequence_no = 48
    valid_instances = ['you', 'spouse']

    def __init__(self, **kwargs):
        instance = kwargs['instance']
        assert(instance in ['you', 'spouse'])
        you = "you" if instance == "you" else "your spouse"
        your = "your" if instance == "you" else "your spouse's"

        inputs = [
            BooleanInput('part_1_needed', description=f'Do {you} need to fill out part 1 of Form 8606? This is required if one or more of the following apply: 1) {you} made nondeductible contributions to a traditional IRA for 2021, 2) {you} took distributions from a traditional, SEP, or SIMPLE IRA in 2021 and {you} made nondeductible contributions to a traditional IRA in 2021 or an earlier year, 3) {you} converted part, but not all, of {your} traditional, SEP, and SIMPLE IRAs to Roth IRAs in 2021 and {you} made nondeductible contributions to a traditional IRA in 2021 or an earlier year. See Form 8606 instructions for more information.'),
            FloatInput('nondeductible_contributions', description=f'Enter {your} nondeductible contributions to traditional IRAs for 2021, including those made for 2021 from January 1, 2022, through April 18, 2022'),
            FloatInput('traditional_basis', description=f'Enter {your} total basis in traditional IRAs. See instructions'),
            BooleanInput('distribution_or_roth_conversion', description=f'In {Form8606.tax_year}, did {you} take a distribution from traditional, SEP, or SIMPLE IRAs, or make a Roth IRA conversion?'),
            FloatInput('nondeductible_contributions_next_year', description=f'Enter {your} nondeductible contributions to traditional IRAs for 2021 made from January 1, 2022 through April 18, 2022'),
            FloatInput('year_end_value_non_roth', description=f'Enter the value of *all* {your} traditional, SEP, and SIMPLE IRAs as of December 31, 2021, plus any outstanding rollovers. Subtract any repayments of qualified disaster distributions (see 2021 Forms 8915-D and 8915-F)'),
            FloatInput('distributions_2021', description=f'Enter {your} distributions from traditional, SEP, and SIMPLE IRAs in 2021. Do *not* include rollovers (other than repayments of qualified disaster distributions (see 2021 Forms 8915-D and 8915-F)), qualified charitable distributions, a one-time distribution to fund an HSA, conversions to a Roth IRA, certain returned contributions, or recharacterizations of traditional IRA contributions (see instructions)'),
            BooleanInput('qualified_disaster_distributions', description=f'Are any of {your} distributions from traditional, SEP, and Simple IRAs in 2021 qualified disaster distributions?'),
            FloatInput('net_converted', description=f'Enter the net amount {you} converted from traditional, SEP, and SIMPLE IRAs to Roth IRAs in 2021.'),
            BooleanInput('part_2_needed', description=f'Did {you} convert part or all of {your} traditional, SEP, and SIMPLE IRAs to a Roth IRA in {Form8606.tax_year}?'),
            FloatInput('converted_cost_basis', description=f'Enter {your} cost basis for the net amount {you} converted from traditional, SEP, and SIMPLE IRAs to Roth IRAs in {Form8606.tax_year}'),
            BooleanInput('part_3_needed', description=f'Did {you} take a distribution from a Roth IRA in 2021?'),
            FloatInput('total_nonqualified_distributions', description=f'Enter {your} total nonqualified distributions from Roth IRAs in 2021, including any qualified first-time homebuyer distributions, and any qualified disaster distributions (see instructions). Also, see 2021 Forms 8915-D and 8915-F'),
            FloatInput('qualified_homebuyer', description=f'Qualified first-time homebuyer expenses (see instructions). Do not enter more than $10,000 reduced by the total of all {your} prior qualified first-time homebuyer distributions'),
            FloatInput('roth_ira_contributions_basis', description=f'Enter {your} basis in Roth IRA contributions (see instructions)'),
        ]

        # All fields are optional. Form 1040/1040-SR/1040-NR should include the
        # sum of 'taxable_amount' fields from all forms 8606 on line 4b.
        optional_fields = [
            FloatField('1', lambda s, i, v: i['nondeductible_contributions']),
            FloatField('2', lambda s, i, v: i['traditional_basis']),
            FloatField('3', lambda s, i, v: v['1'] + v['2']),
            FloatField('4', lambda s, i, v: i['nondeductible_contributions_next_year']),
            FloatField('5', lambda s, i, v: v['3'] - v['4']),
            FloatField('6', lambda s, i, v: i['year_end_value_non_roth']),
            FloatField('7', lambda s, i, v: i['distributions_2021']),
            FloatField('8', lambda s, i, v: i['net_converted']),
            FloatField('9', lambda s, i, v: v['6'] + v['7'] + v['8']),
            FloatField('10', lambda s, i, v: min(1.000, float(v['5']) / float(v['9']), 1.000), places=5),
            FloatField('11', lambda s, i, v: v['8'] * v['10']),
            FloatField('12', lambda s, i, v: v['7'] * v['10']),
            FloatField('13', lambda s, i, v: v['11'] + v['12']),
            FloatField('14', lambda s, i, v: v['3'] if i['distribution_or_roth_conversion'] else v['3'] - v['13']),
            FloatField('15a', lambda s, i, v: v['7'] - v['12']),
            FloatField('15b', lambda s, i, v: self.not_implemented() if i['qualified_disaster_distributions'] else None),
            FloatField('15c', lambda s, i, v: v['15a'] - v['15b']),
            FloatField('16', lambda s, i, v: i['net_converted']),
            FloatField('17', lambda s, i, v: v['11'] if i['part_1_needed'] else i['converted_cost_basis']),
            FloatField('18', lambda s, i, v: v['16'] - v['17']),
            FloatField('19', lambda s, i, v: i['total_nonqualified_distributions']),
            FloatField('20', lambda s, i, v: i['qualified_homebuyer']),
            FloatField('21', lambda s, i, v: max(0.0, v['19'] - v['20'])),
            FloatField('22', lambda s, i, v: i['roth_ira_contributions_basis']),
            FloatField('23', lambda s, i, v: max(0.0, v['21'] - v['22'])),
        ]

        # Check the (part_1_needed, part_2_needed, part_3_needed inputs
        # from this form and pull the needed values (lines 15c, 18, and/or
        # 25c) directly to cause those sections to be calculated
        def taxable_amount(self, i, v):
            total = 0.0
            if i['part_1_needed']:
                if i['distribution_or_roth_conversion']:
                    total += v['15c']
                else:
                    v['14'] # Not returned, but needs to be populated
            if i['part_2_needed']:
                total += v['18']
            if i['part_3_needed']:
                if v['21'] < 0.001:
                    v['22'] # Not returned, but needs to be populated
                elif v['23'] >= 0.001:
                    # Generally, there is an additional 10% tax on 2021
                    # distributions from a Roth IRA that are shown on line 23.
                    # You will need to complete lines 1 through 4 of Form 5329
                    # to determine the amounts from the Roth IRAs that are
                    # subject to the additional tax. See the instructions for
                    # Form 5329, Part I, for details and exceptions.
                    self.not_implemented()
            return total

        def name_field(self, i, v):
            if self.form().instance() == 'spouse':
                return f'{v["1040.spouse_first_name"]} {v["1040.spouse_last_name"]}'
            else:
                return f'{v["1040.first_name"]} {v["1040.last_name"]}'

        required_fields = [
            StringField('name', name_field),
            StringField('ssn', lambda s, i, v: v[f'1040.{s.form().instance()}_ssn']),
            FloatField('taxable_amount', taxable_amount),
        ]

        pdf_fields = [
            TextPDFField('topmostSubform[0].Page1[0].f1_1[0]', 'name'),
            TextPDFField('topmostSubform[0].Page1[0].f1_2[0]', 'ssn', max_length=11),
            # only if filling form by itself
#            TextPDFField('topmostSubform[0].Page1[0].f1_3[0]', 'unknown'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_4[0]', 'unknown'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_5[0]', 'unknown'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_6[0]', 'unknown'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_7[0]', 'unknown'),
#            TextPDFField('topmostSubform[0].Page1[0].f1_8[0]', 'unknown'),
            TextPDFField('topmostSubform[0].Page1[0].f1_9[0]', '1'),
            TextPDFField('topmostSubform[0].Page1[0].f1_10[0]', '2'),
            TextPDFField('topmostSubform[0].Page1[0].f1_11[0]', '3'),
            TextPDFField('topmostSubform[0].Page1[0].f1_12[0]', '4'),
            TextPDFField('topmostSubform[0].Page1[0].f1_13[0]', '5'),
            TextPDFField('topmostSubform[0].Page1[0].f1_14[0]', '6'),
            TextPDFField('topmostSubform[0].Page1[0].f1_15[0]', '7'),
            TextPDFField('topmostSubform[0].Page1[0].f1_16[0]', '8'),
            TextPDFField('topmostSubform[0].Page1[0].f1_17[0]', '9'),
            TextPDFField('topmostSubform[0].Page1[0].f1_18[0]', '10', max_length=1, value_fn=lambda s, v, f: 1 if v > 1 else 0),
            TextPDFField('topmostSubform[0].Page1[0].f1_19[0]', '10', value_fn=lambda s, v, f: int(round((v % 1) * 100000, 0))),
            TextPDFField('topmostSubform[0].Page1[0].f1_20[0]', '11'),
            TextPDFField('topmostSubform[0].Page1[0].f1_21[0]', '12'),
            TextPDFField('topmostSubform[0].Page1[0].f1_22[0]', '13'),
            TextPDFField('topmostSubform[0].Page1[0].f1_23[0]', '14'),
            TextPDFField('topmostSubform[0].Page1[0].f1_24[0]', '15a'),
            TextPDFField('topmostSubform[0].Page1[0].f1_25[0]', '15b'),
            TextPDFField('topmostSubform[0].Page1[0].f1_26[0]', '15c'),
            TextPDFField('topmostSubform[0].Page2[0].f2_1[0]', '16'),
            TextPDFField('topmostSubform[0].Page2[0].f2_2[0]', '17'),
            TextPDFField('topmostSubform[0].Page2[0].f2_3[0]', '18'),
            TextPDFField('topmostSubform[0].Page2[0].f2_4[0]', '19'),
            TextPDFField('topmostSubform[0].Page2[0].f2_5[0]', '20'),
            TextPDFField('topmostSubform[0].Page2[0].f2_6[0]', '21'),
            TextPDFField('topmostSubform[0].Page2[0].f2_7[0]', '22'),
            TextPDFField('topmostSubform[0].Page2[0].f2_8[0]', '23'),
            # unimplemented
#            TextPDFField('topmostSubform[0].Page2[0].f2_9[0]', '24'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_10[0]', '25a'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_11[0]', '25b'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_12[0]', '25c'),
            # only if filling form by itself
#            TextPDFField('topmostSubform[0].Page2[0].f2_13[0]', 'unknown'),
#            ButtonPDFField('topmostSubform[0].Page2[0].c2_1[0]', 'unknown', '1'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_14[0]', 'unknown', max_length=11),
#            TextPDFField('topmostSubform[0].Page2[0].f2_15[0]', 'unknown'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_16[0]', 'unknown', max_length=10),
#            TextPDFField('topmostSubform[0].Page2[0].f2_17[0]', 'unknown'),
#            TextPDFField('topmostSubform[0].Page2[0].f2_18[0]', 'unknown'),
        ]
        pdf_file = os.path.join(os.path.dirname(__file__), 'f8606.pdf')

        super().__init__(__class__, inputs, required_fields, optional_fields, pdf_fields=pdf_fields, pdf_file=pdf_file, **kwargs)

    def needs_filing(self, values):
        return True
