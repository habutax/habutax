from habutax.enum import filing_status as status
from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *

class Form1040S2Need6251(Form):
    form_name = "1040_s2_need_6251"
    tax_year = 2023
    description = "Worksheet To See if You Should Fill in Form 6251 (Form 1040)"
    long_description = "Schedule 2, Line 1"
    jurisdiction = Jurisdiction.US

    def __init__(self, **kwargs):
        thresholds = {
            'line_6': {
                (status.Single, status.HeadOfHousehold):                          81300.0,
                (status.MarriedFilingJointly, status.QualifyingSurvivingSpouse): 126500.0,
                status.MarriedFilingSeparately:                                   63250.0,
            },
            'line_8': {
                (status.Single, status.HeadOfHousehold):                          578150.0,
                (status.MarriedFilingJointly, status.QualifyingSurvivingSpouse): 1156300.0,
                status.MarriedFilingSeparately:                                   578150.0,
            },
            'line_12_comparison': {
                (status.Single, status.HeadOfHousehold,
                 status.MarriedFilingJointly,
                 status.QualifyingSurvivingSpouse): 220700.0,
                status.MarriedFilingSeparately:     110350.0,
            }
        }

        inputs = [
            BooleanInput('schedule_j_needed', description="Do you need to fill our Schedule J? (Income Averaging for Farmers and Fishermen)"),
            BooleanInput('form_4972_needed', description="Do you need to fill out Form 4972? (Tax on Lump-Sum Distributions From Qualified Plans of Participants Born Before January 2, 1936)"),
        ]

        def line_13(self, i, v):
            if i['schedule_j_needed'] or i['form_4972_needed']:
                self.not_implemented()
            amount = v['1040.16']
            if i['1040.need_8962']:
                amount += v['1040_s2.2']
            return amount

        def need_6251(self, i, v):
            if not v['5'] > v['6']:
                return False
            elif v['11'] > self.threshold('line_12_comparison', i['1040.filing_status']):
                return True
            return v['12'] > v['13']

        optional_fields = [
            FloatField('1', lambda s, i, v: s.not_implemented() if not v['1040.itemizing'] else v['1040.15']),
            FloatField('2', lambda s, i, v: s.not_implemented() if not v['1040.itemizing'] else v['1040_sa.7']),
            FloatField('3', lambda s, i, v: v['1040.11'] - v['1040.13'] if not v['1040.itemizing'] else v['1'] + v['2']),
            FloatField('4', lambda s, i, v: v['1040_s1.1'] + v['1040_s1.8z'] if v['1040.schedule_1_additional_income'] else None),
            FloatField('5', lambda s, i, v: v['3'] - v['4']),
            FloatField('6', lambda s, i, v: s.threshold('line_6', i['1040.filing_status'])),
            FloatField('7', lambda s, i, v: v['5'] - v['6']),
            FloatField('8', lambda s, i, v: s.threshold('line_8', i['1040.filing_status'])),
            FloatField('9', lambda s, i, v: 0.0 if v['5'] > v['8'] else v['5'] - v['8']),
            FloatField('10', lambda s, i, v: min(v['6'], v['9'] * 0.25)),
            FloatField('11', lambda s, i, v: v['7'] + v['10'] if v['5'] > v['8'] else v['7']),
            FloatField('12', lambda s, i, v: v['11'] * 0.26),
            FloatField('13', line_13),
            BooleanField('need_6251', need_6251),
        ]

        super().__init__(__class__, inputs, [], optional_fields,
                         thresholds=thresholds, **kwargs)

    def needs_filing(self, values):
        return False
