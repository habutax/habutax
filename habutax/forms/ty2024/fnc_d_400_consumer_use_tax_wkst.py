from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *

class FormNCD400ConsumerUseTaxWkst(Form):
    form_name = "nc_d-400_consumer_use_tax_wkst"
    tax_year = 2023
    description = "Consumer Use Tax Worksheet (NC Form D-400)"
    long_description = "Line 18"
    jurisdiction = Jurisdiction.NC

    def __init__(self, **kwargs):
        inputs = [
            BooleanInput('full_records', description="Do you have records of out-of-state (NC) purchases your or your spouse made for tax year 2023?"),
            FloatInput('out_of_state_purchases', description="Enter the total amount of out-of-state purchases, including delivery charges, for 1/1/2023 through 12/31/2023"),
            FloatInput('county_tax_pct', description="Enter 7.5% (.075) in Durham and Orange Counties; 7.25% (.0725) in Mecklenburg and Wake Counties; 7%(.07) in Alexander, Alleghany, Anson, Ashe, Bertie, Buncombe, Cabarrus, Catawba, Chatham, Cherokee, Clay, Cumberland, Davidson, Duplin, Edgecombe, Forsyth, Gaston, Graham, Greene, Halifax, Harnett, Haywood, Hertford, Jackson, Jones, Lee, Lincoln, Madison, Martin, Montgomery, Moore, New Hanover, Onslow, Pasquotank, Pitt, Randolph, Robeson, Rockingham, Rowan, Rutherford, Sampson, Stanly, Surry, Swain, and Wilkes Counties; and 6.75% (.0675) in all other counties"),
            FloatInput('other_state_sales_tax', description="Enter the amount of sales tax legally and properly paid to another state or North Carolina on your out-of-state purchases."),
        ]

        def estimate(self, i, v):
            use_tax_table = [
                (2200, 1),
                (3700, 2),
                (5200, 3),
                (6700, 4),
                (8100, 5),
                (9600, 6),
                (11100, 7),
                (12600, 8),
                (14100, 9),
                (15600, 10),
                (17000, 11),
                (18500, 12),
                (20000, 13),
                (21500, 14),
                (23000, 15),
                (24400, 16),
                (25900, 17),
                (27400, 18),
                (28900, 19),
                (30400, 20),
                (31900, 21),
                (33300, 22),
                (34800, 23),
                (36300, 24),
                (37800, 25),
                (39300, 26),
                (40700, 27),
                (42200, 28),
                (43700, 29),
                (45200, 30),
            ]
            for max_taxable_income, use_tax in use_tax_table:
                if v['nc_d-400.14'] < max_taxable_income:
                    return float(use_tax)
            assert v['nc_d-400.14'] >= 45200
            return v['nc_d-400.14'] * 0.000675

        optional_fields = [
            FloatField('estimate', estimate, places=0),
            FloatField('1', lambda s, i, v: i['out_of_state_purchases'], places=0),
            FloatField('2', lambda s, i, v: i['county_tax_pct'] * v['1'], places=0),
            FloatField('3', lambda s, i, v: min(i['other_state_sales_tax'], v['2']), places=0),
            FloatField('4', lambda s, i, v: round(v['2'] - v['3'], 0), places=0),
            FloatField('consumer_use_tax', lambda s, i, v: v['4'] if i['full_records'] else v['estimate'], places=0),
        ]

        required_fields = [
        ]

        super().__init__(__class__, inputs, required_fields, optional_fields,
                         **kwargs)

    def needs_filing(self, values):
        return False
