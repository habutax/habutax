from habutax.form import Form
from habutax.inputs import *
from habutax.fields import *

class Form1040S1(Form):
    form_name = "1040_s1"
    tax_year = 2021

    def __init__(self, **kwargs):
        inputs = [
            FloatInput('state_local_income_tax', description="Enter the total amount of any refunds, credits, or offsets of state or local income taxes you received in 2021 which you are required to report (see instructions). This typically includes amounts you received on form 1099-G."),
            FloatInput('alimony_received', description="Enter amounts received as alimony or separate maintenance pursuant to a divorce or separation agreement entered into on or before December 31, 2018, unless that agreement was changed after December 31, 2018, to expressly provide that alimony received isn't included in your income"),
            BooleanInput('business_income', description="Did you (or your spouse if filing a joint return) operate a business or practice your profession as a sole proprietor?"),
            BooleanInput('other_gains_losses', description="Do you have gains or losses from selling or exchanging assets used in a trade or business in 2021?"),
            BooleanInput('real_estate', description="Do you have income to report from rental real estate, royalties, partnerships, S corporations, trusts, etc.?"),
            BooleanInput('farm_income_loss', description="Do you have farm income (or loss) to report for 2021?"),
            FloatInput('unemployment_income', description="Enter the amount of any unemployment income you received in 2021 (likely reported on a 1099-G), reduced by any amount you repaid or contributions made to a governmental unemployment compensation program (see instructions for Schedule 1, line 7)"),
            BooleanInput('uncommon_income', description="Do you have less common income to report for 2021? This might include net operating losses, gambling, cancellation of debt, foreign earned income, taxable HSA distributions, Alaska Permanent Fund dividends, jury duty pay, prizes and awards, activity not engaged in for profit income, stock options, income from the rental of personal property if you engaged in the rental for profit but were not in the business of renting such property, Olympic/Paralympic medals and USOC prize money, section 951(c) inclusion, section 951A(a) inclusion, Section 461(l) excess business loss adjustment, or taxable distributions from an ABLE account? (see instructions)"),
            BooleanInput('need_other_income', description="Do you have other income to report (not covered by \"less common income\")?"),
            StringInput('other_income_type', description="Description of any other income you need to report"),
            FloatInput('other_income_amount', description="Amount of other income you need to report"),
        ]

        fields = [
            SimpleField('1', lambda s, i, v: i['state_local_income_tax']),
            SimpleField('2a', lambda s, i, v: i['alimony_received']),
            SimpleField('2b', lambda s, i, v: i['alimony_date'] if v['2a'] > 0.001 else ""),
            SimpleField('3', lambda s, i, v: s.not_implemented() if i['business_income'] else ""), # Schedule C
            SimpleField('4', lambda s, i, v: s.not_implemented() if i['other_gains_losses'] else ""), # Form 4797
            SimpleField('5', lambda s, i, v: s.not_implemented() if i['real_estate'] else ""), # Schedule E
            SimpleField('6', lambda s, i, v: s.not_implemented() if i['farm_income_loss'] else ""), # Schedule F
            SimpleField('7', lambda s, i, v: i['unemployment_income']),
            SimpleField('8a', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8b', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8c', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8d', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8e', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8f', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8g', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8h', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8i', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8j', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8k', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8l', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8m', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8n', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8o', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8p', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else ""),
            SimpleField('8z_type', lambda s, i, v: i['other_income_type'] if i['other_income'] else ""),
            SimpleField('8z', lambda s, i, v: i['other_income_amount'] if i['other_income'] else ""),
            SimpleField('9', lambda s, i, v: sum([v[f'8{l}'] for l in "abcdefghijklmnopz"])),
            SimpleField('10', lambda s, i, v: sum([v[f'{n}'] for n in range(1,8)]) + v['9']),
        ]

        super().__init__(__class__, inputs, fields, [], **kwargs)
