from habutax.enum import filing_status as status
from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *

from habutax.forms.ty2023.f1040_figure_tax import figure_tax

class Form1040QualDivCapGainTaxWkst(Form):
    form_name = "1040_qualdiv_capgain_tax_wkst"
    tax_year = 2023
    description = "Qualified Dividends and Capital Gain Tax Worksheet (Form 1040)"
    long_description = "Line 16"
    jurisdiction = Jurisdiction.US

    def __init__(self, **kwargs):
        thresholds = {
            'line_6': {
                (status.Single, status.MarriedFilingSeparately):                 44625.0,
                (status.MarriedFilingJointly, status.QualifyingSurvivingSpouse): 89250.0,
                status.HeadOfHousehold:                                          59750.0,
            },
            'line_13': {
                status.Single:                                                   492300.0,
                status.MarriedFilingSeparately:                                  276900.0,
                (status.MarriedFilingJointly, status.QualifyingSurvivingSpouse): 553850.0,
                status.HeadOfHousehold:                                          523050.0
            },
        }

        inputs = [
            BooleanInput('form_2555', description="Do you need to fill out Form 2555 (relating to foreign earned income)?"),
        ]

        optional_fields = [
            FloatField('1', lambda s, i, v: s.not_implemented() if i['form_2555'] else v['1040.15']),
            FloatField('2', lambda s, i, v: s.not_implemented() if i['form_2555'] else v['1040.3a']),
            FloatField('3', lambda s, i, v: s.not_implemented() if i['1040.schedule_d_required'] else v['1040.7']),
            FloatField('4', lambda s, i, v: v['2'] + v['3']),
            FloatField('5', lambda s, i, v: max(0.0, v['1'] - v['4'])),
            FloatField('6', lambda s, i, v: s.threshold('line_6', i['1040.filing_status'])),
            FloatField('7', lambda s, i, v: min(v['1'], v['6'])),
            FloatField('8', lambda s, i, v: min(v['5'], v['7'])),
            FloatField('9', lambda s, i, v: v['7'] - v['8']),
            FloatField('10', lambda s, i, v: min(v['1'], v['4'])),
            FloatField('11', lambda s, i, v: v['9']),
            FloatField('12', lambda s, i, v: v['10'] - v['11']),
            FloatField('13', lambda s, i, v: s.threshold('line_13', i['1040.filing_status'])),
            FloatField('14', lambda s, i, v: min(v['1'], v['13'])),
            FloatField('15', lambda s, i, v: v['5'] + v['9']),
            FloatField('16', lambda s, i, v: max(0.0, v['14'] - v['15'])),
            FloatField('17', lambda s, i, v: min(v['12'], v['16'])),
            FloatField('18', lambda s, i, v: v['17'] * 0.15),
            FloatField('19', lambda s, i, v: v['9'] + v['17']),
            FloatField('20', lambda s, i, v: v['10'] - v['19']),
            FloatField('21', lambda s, i, v: v['20'] * 0.20),
            FloatField('22', lambda s, i, v: figure_tax(v['5'], i['1040.filing_status'])),
            FloatField('23', lambda s, i, v: v['18'] + v['21'] + v['22']),
            FloatField('24', lambda s, i, v: figure_tax(v['1'], i['1040.filing_status'])),
            FloatField('25', lambda s, i, v: min(v['23'], v['24'])),
        ]

        super().__init__(__class__, inputs, [], optional_fields,
                         thresholds=thresholds, **kwargs)

    def needs_filing(self, values):
        return False
