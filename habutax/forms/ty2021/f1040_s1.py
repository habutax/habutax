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
            StringInput('alimony_received_date', description="Date of original divorce or separation agreement for alimony received."),
            BooleanInput('business_income', description="Did you (or your spouse if filing a joint return) operate a business or practice your profession as a sole proprietor?"),
            BooleanInput('other_gains_losses', description="Do you have gains or losses from selling or exchanging assets used in a trade or business in 2021?"),
            BooleanInput('real_estate', description="Do you have income to report from rental real estate, royalties, partnerships, S corporations, trusts, etc.?"),
            BooleanInput('farm_income_loss', description="Do you have farm income (or loss) to report for 2021?"),
            FloatInput('unemployment_income', description="Enter the amount of any unemployment income you received in 2021 (likely reported on a 1099-G), reduced by any amount you repaid or contributions made to a governmental unemployment compensation program (see instructions for Schedule 1, line 7)"),
            BooleanInput('uncommon_income', description="Do you have less common income to report for 2021? This might include net operating losses, gambling, cancellation of debt, foreign earned income, taxable HSA distributions, Alaska Permanent Fund dividends, jury duty pay, prizes and awards, activity not engaged in for profit income, stock options, income from the rental of personal property if you engaged in the rental for profit but were not in the business of renting such property, Olympic/Paralympic medals and USOC prize money, section 951(c) inclusion, section 951A(a) inclusion, Section 461(l) excess business loss adjustment, or taxable distributions from an ABLE account? (see instructions for Form 1040 Schedule 1, lines 8a-8p)"),
            BooleanInput('need_other_income', description="Do you have other income to report (not covered by \"less common income\")?"),
            StringInput('other_income_type', description="Description of any other income you need to report"),
            FloatInput('other_income_amount', description="Amount of other income you need to report"),
            FloatInput('educator_expenses', description=f'If you or your spouse were an eligible educator in {Form1040S1.tax_year}, enter up to $250 per educator in qualified educator expenses. Before entering, reduce this amount if you had any excludable US series EE and I savings bond intereset, nontaxable qualified tuition program earnings/distributions, nontaxable distribution of Coverdel education savings account earnings, or were reimbursed for these expenses in a way not reported on box 1 of your Form W-2.'),
            BooleanInput('certain_business_expenses', description='Did you incurr any of the following expenses in 2021: Certain business expenses of National Guard and reserve members who traveled more than 100 miles from home to perform services as a National Guard or reserve member; Performing-arts-related expenses as a qualified performing artist; Business expenses of fee-basis state or local government officials. For more details, see Form 2106.'),
            BooleanInput('moving_expenses', description='Did you have any moving expenses as a member of the Armed Forces on active duty and due to a military order you move because of a permanent change of station in 2021? See form 3903 and Tax Topic 455.'),
            BooleanInput('deductible_self_employment_tax', description='Were you self-employed and did you self-employment tax in 2021? See Form 1040, Schedule SE.'),
            BooleanInput('sep_simple_qualified', description="Were you self-employed and eligible to deduct any contributions to SEP, SIMPLE, or Qualified Plans in 2021?"),
            BooleanInput('self_employed_health_insurance', description="Are you self-employed and able to deduct the amount you paid for health insurance? (See Form 1040, Schedule 1, line 17 instructions."),
            FloatInput('alimony_paid', description="Enter amounts paid as alimony or separate maintenance pursuant to a divorce or separation agreement entered into on or before December 31, 2018, unless that agreement was changed after December 31, 2018, to expressly provide that alimony paid isn't included in your former spouse's income"),
            StringInput('alimony_paid_ssn', description="SSN of recipient of alimony paid."),
            StringInput('alimony_paid_date', description="Date of original divorce or separation agreement for alimony paid."),
            BooleanInput('traditional_ira_deduction', description="Are you (or your spouse if filing jointly) eligible to take a deduction for contributions to a traditional IRA made in 2021? See instructions for Form 1040, Schedule 1, line 20 for more details."),
            BooleanInput('student_loan_interest', description="Are you (or your spouse if filing jointly) eligible to take a deduction for student loan interest? See instructions for Form 1040, Schedule 1, line 21 for more details."),
            BooleanInput('archer_msa_deduction', description="Are you (or your spouse if filing jointly) eligible to take a deduction for contributions to an Archer MSA made for 2021? See instructions for Form 1040, Schedule 1, line 23 for more details."),
            BooleanInput('uncommon_decuctions', description="Do you have less common decuctions to report for 2021? This might include jury duty pay, deductible expenses related to income reported from the rental of personal property engaged in for profit, nontaxable amount of the value of Olympic and Paralympic medals and USOC prize money, reforestation amortization and expenses, repayment of supplemental unemployment benefits under the Trade Act of 1974, contributions to section 501(c)(18)(D) pension plan, contributions by certain chaplains to section 403(b) plans, attorney fees and court costs for actions involving certain unlawful discrimination claims, attorney fees and court costs you paid in connection with an award from the IRS for information you provided that helped the IRS detect tax law violations, housing deduction from Form 2555, or excess deductions of section 67(e) expenses from Schedule K-1 (Form 1041). (see instructions for Form 1040 Schedule 1, lines 24a-24k)"),
            BooleanInput('need_other_adjustments', description="Do you have other adjustments to income to report (not covered by \"less common deductions\")?"),
            StringInput('other_adjustments_type', description="Description of any other adjustments to income."),
            FloatInput('other_adjustments_amount', description="Amount of other adjustments to income you need to report"),
        ]

        def line_18(self, i, v):
            penalties = sum([v[f'1099-int:{n}.box_2'] for n in range(i['number_1099-int'])])
            penalties += sum([v[f'1099-oid:{n}.box_3'] for n in range(i['number_1099-oid'])])
            if penalties > 0.01:
                return penalties
            return ""

        optional_fields = [
            SimpleField('1', lambda s, i, v: i['state_local_income_tax']),
            SimpleField('2a', lambda s, i, v: i['alimony_received']),
            SimpleField('2b', lambda s, i, v: i['alimony_received_date'] if v['2a'] > 0.001 else ""),
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
            SimpleField('8z_type', lambda s, i, v: i['other_income_type'] if i['need_other_income'] else ""),
            SimpleField('8z', lambda s, i, v: i['other_income_amount'] if i['need_other_income'] else ""),
            SimpleField('9', lambda s, i, v: sum([v[f'8{l}'] for l in "abcdefghijklmnopz"])),
            SimpleField('10', lambda s, i, v: sum([v[f'{n}'] for n in range(1,8)]) + v['9']),
            SimpleField('11', lambda s, i, v: i['educator_expenses']),
            SimpleField('12', lambda s, i, v: s.not_implemented() if i['certain_business_expenses'] else ""),
            SimpleField('13', lambda s, i, v: s.not_implemented()), # Form 8889
            SimpleField('14', lambda s, i, v: s.not_implemented() if i['moving_expenses'] else ""),
            SimpleField('15', lambda s, i, v: s.not_implemented() if i['deductible_self_employment_tax'] else ""),
            SimpleField('16', lambda s, i, v: s.not_implemented() if i['sep_simple_qualified'] else ""),
            SimpleField('17', lambda s, i, v: s.not_implemented() if i['self_employed_health_insurance'] else ""),
            SimpleField('18', line_18),
            SimpleField('19a', lambda s, i, v: i['alimony_paid']),
            SimpleField('19b', lambda s, i, v: i['alimony_paid_ssn'] if v['2a'] > 0.001 else ""),
            SimpleField('19c', lambda s, i, v: i['alimony_paid_date'] if v['2a'] > 0.001 else ""),
            SimpleField('20', lambda s, i, v: s.not_implemented() if i['traditional_ira_deduction'] else ""),
            SimpleField('21', lambda s, i, v: s.not_implemented() if i['student_loan_interest'] else ""),
            SimpleField('22', lambda s, i, v: ""),
            SimpleField('23', lambda s, i, v: s.not_implemented() if i['archer_msa_deduction'] else ""),
            SimpleField('24a', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else ""),
            SimpleField('24b', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else ""),
            SimpleField('24c', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else ""),
            SimpleField('24d', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else ""),
            SimpleField('24e', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else ""),
            SimpleField('24f', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else ""),
            SimpleField('24g', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else ""),
            SimpleField('24h', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else ""),
            SimpleField('24i', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else ""),
            SimpleField('24j', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else ""),
            SimpleField('24k', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else ""),
            SimpleField('24z_type', lambda s, i, v: i['other_adjustments_type'] if i['need_other_adjustments'] else ""),
            SimpleField('24z', lambda s, i, v: i['other_adjustments_amount'] if i['need_other_adjustments'] else ""),
            SimpleField('25', lambda s, i, v: sum([v[f'24{l}'] for l in "abcdefghijkz"])),
            SimpleField('26', lambda s, i, v: sum([v[f'{n}'] for n in range(11,24)]) + v['25']),
        ]

        super().__init__(__class__, inputs, [], optional_fields, **kwargs)
