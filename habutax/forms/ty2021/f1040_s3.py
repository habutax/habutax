from habutax.form import Form
from habutax.inputs import *
from habutax.fields import *

class Form1040S3(Form):
    form_name = "1040_s3"
    tax_year = 2021

    def __init__(self, **kwargs):
        inputs = [
            BooleanInput('other_foreign_gross_income', description="Do you have any foreign source gross income *not* from interest and dividends or any foreign tax paid on that income not reported to you on Form 1099-INT, Form 1099-DIV?"),
            BooleanInput('child_dependent_care', description="Did you pay expenses for the care of a qualifying individual (child or other dependent) to enable you (and your spouse, if filing a joint return) to work or actively look for work?"),
            BooleanInput('education_credit', description="Did you (or your dependent) pay qualified expenses in 2021 for yourself, your spouse, or your dependent to enroll in or attend an eligible educational institution? If so, do you need to claim an education credit on Form 8863?"),
            BooleanInput('retirement_savings_contributions', description="Did you, or your spouse if filing jointly, made (a) contributions, other than rollover contributions, to a retirement plan in 2021?"),
            BooleanInput('residential_energy_credit', description="Did you pay for any energy-efficient upgrades to your home in 2021? This might be things like installing solar panels, wind energy installations, adding insulation or high-efficiency HVAC units."),
            BooleanInput('other_nonrefundable_credits', description="Do you have any less common nonrefundable credits to claim? These include general business credits (Form 3800), prior year minimum tax (Form 8801), adoption credit (Form 8839), credit for the elderly or disabled (Schedule R), alternative motor vehicle credit (Form 8910), qualified plug-in motor vehicle credit (Form 8936), mortgage interest credit (Form 8396), District of Columbia first-time homebuyer credit (Form 8859), qualified electric vehicle credit (Form 8834), alternative fuel vehicle refueling property credit (Form 8911),  credit to holders of tax credit bonds (Form 8912), amount on Form 8978, line 14 (reporting for partnership income), or any other nonrefundable tax credits."),
        ]

        def line_1(self, i, v):
            foreign_tax = float(sum([v[f'1099-int:{n}.box_6'] for n in range(i['1040.number_1099-int'])]))
            foreign_tax += float(sum([v[f'1099-div:{n}.box_7'] for n in range(i['1040.number_1099-div'])]))
            f1116_limit = 600.0 if i['1040.filing_status'] is self.form('1040').FILING_STATUS.MarriedFilingJointly else 300.0
            if i['other_foreign_gross_income'] or foreign_tax > f1116_limit:
                return self.not_implemented()
            return foreign_tax if foreign_tax > 0.001 else None

        def retirement_savings_limit(self, i, v):
            statuses = self.form('1040').FILING_STATUS
            if i['1040.filing_status'] is statuses.MarriedFilingJointly:
                return 66000.0
            elif i['1040.filing_status'] is statuses.HeadOfHousehold:
                return 49500.0
            else:
                return 33000.0

        optional_fields = [
            FloatField('1', line_1),
            FloatField('2', lambda s, i, v: s.not_implemented() if i['child_dependent_care'] else None), # Form 2441, line 11
            FloatField('3', lambda s, i, v: s.not_implemented() if i['education_credit'] else None), # Form 8863, line 19
            FloatField('4', lambda s, i, v: s.not_implemented() if v['1040.11'] <= retirement_savings_limit(s, i, v) and i['retirement_savings_contributions'] else None), # Form 8880
            FloatField('5', lambda s, i, v: s.not_implemented() if i['residential_energy_credit'] else None), # Form 5695
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
            FloatField('6z', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Other nonrefundable credits
            FloatField('7', lambda s, i, v: sum([v[f'6{l}'] for l in "abcdefghijklz"])),
            FloatField('8', lambda s, i, v: sum([v[f'{n}'] for n in range(1,5+1)]) + v['7']),
        ]
        required_fields = [
            StringField('6z_type', lambda s, i, v: s.not_implemented() if i['other_nonrefundable_credits'] else None), # Type of any nonrefundable credits
        ]

        super().__init__(__class__, inputs, required_fields, optional_fields, **kwargs)
