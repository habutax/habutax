import os

from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *
from habutax.pdf_fields import *

class Form1040S1(Form):
    form_name = "1040_s1"
    tax_year = 2021
    description = "Schedule 1 (Form 1040)"
    long_description = "Additional Income and Adjustments to Income"
    jurisdiction = Jurisdiction.US
    sequence_no = 1

    def __init__(self, **kwargs):
        inputs = [
            BooleanInput('state_local_income_tax_adjust', description="Do you have any refunds, credits, or offsets of state or local income taxes you received in 2021 which you are required to report which you have not already reported via entered 1099-G forms, or adjustments to make to the amounts on your entered 1099-Gs?"),
            FloatInput('state_local_income_tax', description="Enter the total amount of any refunds, credits, or offsets of state or local income taxes you received in 2021 which you are required to report (see instructions). This typically includes amounts you received on form 1099-G. Please include the amounts even from Forms 1099-G you have entered into HabuTax separately."),
            FloatInput('alimony_received', description="Enter amounts received as alimony or separate maintenance pursuant to a divorce or separation agreement entered into on or before December 31, 2018, unless that agreement was changed after December 31, 2018, to expressly provide that alimony received isn't included in your income"),
            StringInput('alimony_received_date', description="Date of original divorce or separation agreement for alimony received."),
            BooleanInput('business_income', description="Did you (or your spouse if filing a joint return) operate a business or practice your profession as a sole proprietor?"),
            BooleanInput('other_gains_losses', description="Do you have gains or losses from selling or exchanging assets used in a trade or business in 2021?"),
            BooleanInput('real_estate', description="Do you have income to report from rental real estate, royalties, partnerships, S corporations, trusts, etc.?"),
            BooleanInput('farm_income_loss', description="Do you have farm income (or loss) to report for 2021?"),
            FloatInput('unemployment_income', description="Enter the amount of any unemployment income you received in 2021 (likely reported on a 1099-G), reduced by any amount you repaid or contributions made to a governmental unemployment compensation program (see instructions for Schedule 1, line 7). Note that any unemployment income entered into HabuTax via a 1099-G is not being considered unless you enter it again here."),
            BooleanInput('uncommon_income', description="Do you have less common income to report for 2021? This might include net operating losses, gambling, cancellation of debt, foreign earned income, taxable HSA distributions, Alaska Permanent Fund dividends, jury duty pay, prizes and awards, activity not engaged in for profit income, stock options, income from the rental of personal property if you engaged in the rental for profit but were not in the business of renting such property, Olympic/Paralympic medals and USOC prize money, section 951(c) inclusion, section 951A(a) inclusion, Section 461(l) excess business loss adjustment, or taxable distributions from an ABLE account? (see instructions for Form 1040 Schedule 1, lines 8a-8p)"),
            BooleanInput('need_other_income', description="Do you have other income to report (not covered by \"less common income\")? Do not include refunds of overpaid interest reported on form 1098, box 4 (unless you are not entering that form into HabuTax)"),
            StringInput('other_income_type', description="Description of any other income you need to report"),
            FloatInput('other_income_amount', description="Amount of other income you need to report"),
            FloatInput('educator_expenses', description=f'If you or your spouse were an eligible educator in {Form1040S1.tax_year}, enter up to $250 per educator in qualified educator expenses. Before entering, reduce this amount if you had any excludable US series EE and I savings bond intereset, nontaxable qualified tuition program earnings/distributions, nontaxable distribution of Coverdel education savings account earnings, or were reimbursed for these expenses in a way not reported on box 1 of your Form W-2.'),
            BooleanInput('certain_business_expenses', description='Did you incurr any of the following expenses in 2021: Certain business expenses of National Guard and reserve members who traveled more than 100 miles from home to perform services as a National Guard or reserve member; Performing-arts-related expenses as a qualified performing artist; Business expenses of fee-basis state or local government officials. For more details, see Form 2106.'),
            BooleanInput('moving_expenses', description='Did you have any moving expenses as a member of the Armed Forces on active duty and due to a military order you move because of a permanent change of station in 2021? See form 3903 and Tax Topic 455.'),
            BooleanInput('deductible_self_employment_tax', description='Were you self-employed and did you self-employment tax in 2021? See Form 1040, Schedule SE.'),
            BooleanInput('sep_simple_qualified', description="Were you self-employed and eligible to deduct any contributions to SEP, SIMPLE, or Qualified Plans in 2021?"),
            BooleanInput('self_employed_health_insurance', description="Are you self-employed and able to deduct the amount you paid for health insurance? (See Form 1040, Schedule 1, line 17 instructions."),
            FloatInput('alimony_paid', description="Enter amounts paid as alimony or separate maintenance pursuant to a divorce or separation agreement entered into on or before December 31, 2018, unless that agreement was changed after December 31, 2018, to expressly provide that alimony paid isn't included in your former spouse's income"),
            SSNInput('alimony_paid_ssn', description="SSN of recipient of alimony paid."),
            StringInput('alimony_paid_date', description="Date of original divorce or separation agreement for alimony paid."),
            BooleanInput('traditional_ira_deduction', description="Are you (or your spouse if filing jointly) eligible to take a deduction for contributions to a traditional IRA made in 2021? See instructions for Form 1040, Schedule 1, line 20 for more details."),
            BooleanInput('student_loan_interest', description="Are you (or your spouse if filing jointly) eligible to take a deduction for student loan interest? See instructions for Form 1040, Schedule 1, line 21 for more details."),
            BooleanInput('archer_msa_deduction', description="Are you (or your spouse if filing jointly) eligible to take a deduction for contributions to an Archer MSA made for 2021? See instructions for Form 1040, Schedule 1, line 23 for more details."),
            BooleanInput('uncommon_deductions', description="Do you have less common decuctions to report for 2021? This might include jury duty pay, deductible expenses related to income reported from the rental of personal property engaged in for profit, nontaxable amount of the value of Olympic and Paralympic medals and USOC prize money, reforestation amortization and expenses, repayment of supplemental unemployment benefits under the Trade Act of 1974, contributions to section 501(c)(18)(D) pension plan, contributions by certain chaplains to section 403(b) plans, attorney fees and court costs for actions involving certain unlawful discrimination claims, attorney fees and court costs you paid in connection with an award from the IRS for information you provided that helped the IRS detect tax law violations, housing deduction from Form 2555, or excess deductions of section 67(e) expenses from Schedule K-1 (Form 1041). (see instructions for Form 1040 Schedule 1, lines 24a-24k)"),
            BooleanInput('need_other_adjustments', description="Do you have other adjustments to income to report (not covered by \"less common deductions\")?"),
            StringInput('other_adjustments_type', description="Description of any other adjustments to income."),
            FloatInput('other_adjustments_amount', description="Amount of other adjustments to income you need to report"),
            BooleanInput('hsa_contribution_you', description='Did you make a contribution to an HSA and need to file Form 8889?'),
            BooleanInput('hsa_contribution_spouse', description='Did your spouse make a contribution to an HSA and need to file Form 8889?'),
        ]

        def line_1(self, i, v):
            if i['state_local_income_tax_adjust']:
                return i['state_local_income_tax']
            return float(sum([v[f'1099-g:{n}.box_2'] for n in range(i['1040.number_1099-g'])]))

        def other_income(self, i, v):
            mort_int_refund = sum([v[f'1098:{n}.box_4'] for n in range(i['1040.number_1098'])])
            types = []
            income = []
            if mort_int_refund > 0.001:
                types.append("Refund of overpaid mortgage interest")
                income.append(mort_int_refund)
            if i['need_other_income']:
                types.append(i['other_income_type'])
                income.append(i['other_income_amount'])
            if len(types) > 0:
                return (", ".join(types), sum(income))
            return (None, None)

        def line_18(self, i, v):
            penalties = float(sum([v[f'1099-int:{n}.box_2'] for n in range(i['1040.number_1099-int'])]))
            penalties += float(sum([v[f'1099-oid:{n}.box_3'] for n in range(i['1040.number_1099-oid'])]))
            if penalties > 0.01:
                return penalties
            return ""

        def line_13(self, i, v):
            if not i['hsa_contribution_you'] and not i['hsa_contribution_spouse']:
                return None

            hsa_deduction = v['8889:you.hsa_deduction'] if i['hsa_contribution_you'] else 0.0
            hsa_deduction += v['8889:spouse.hsa_deduction'] if i['hsa_contribution_spouse'] else 0.0
            return hsa_deduction

        optional_fields = [
            FloatField('1', line_1),
            FloatField('2a', lambda s, i, v: i['alimony_received']),
            StringField('2b', lambda s, i, v: i['alimony_received_date'] if v['2a'] > 0.001 else None),
            FloatField('3', lambda s, i, v: s.not_implemented() if i['business_income'] else None), # Schedule C
            FloatField('4', lambda s, i, v: s.not_implemented() if i['other_gains_losses'] else None), # Form 4797
            FloatField('5', lambda s, i, v: s.not_implemented() if i['real_estate'] else None), # Schedule E
            FloatField('6', lambda s, i, v: s.not_implemented() if i['farm_income_loss'] else None), # Schedule F
            FloatField('7', lambda s, i, v: i['unemployment_income']),
            FloatField('8a', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8b', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8c', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8d', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8e', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8f', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8g', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8h', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8i', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8j', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8k', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8l', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8m', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8n', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8o', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8p', lambda s, i, v: s.not_implemented() if i['uncommon_income'] else None),
            FloatField('8z', lambda s, i, v: other_income(s, i, v)[1]),
            FloatField('9', lambda s, i, v: sum([v[f'8{l}'] for l in "abcdefghijklmnopz"])),
            FloatField('10', lambda s, i, v: v['1'] + v['2a'] + sum([v[f'{n}'] for n in range(3,8)]) + v['9']),
            FloatField('11', lambda s, i, v: i['educator_expenses']),
            FloatField('12', lambda s, i, v: s.not_implemented() if i['certain_business_expenses'] else None),
            FloatField('13', line_13), # Form 8889
            FloatField('14', lambda s, i, v: s.not_implemented() if i['moving_expenses'] else None),
            FloatField('15', lambda s, i, v: s.not_implemented() if i['deductible_self_employment_tax'] else None),
            FloatField('16', lambda s, i, v: s.not_implemented() if i['sep_simple_qualified'] else None),
            FloatField('17', lambda s, i, v: s.not_implemented() if i['self_employed_health_insurance'] else None),
            FloatField('18', line_18),
            FloatField('19a', lambda s, i, v: i['alimony_paid']),
            StringField('19b', lambda s, i, v: i['alimony_paid_ssn'] if v['2a'] > 0.001 else None),
            StringField('19c', lambda s, i, v: i['alimony_paid_date'] if v['2a'] > 0.001 else None),
            FloatField('20', lambda s, i, v: s.not_implemented() if i['traditional_ira_deduction'] else None),
            FloatField('21', lambda s, i, v: s.not_implemented() if i['student_loan_interest'] else None),
            FloatField('22', lambda s, i, v: ""),
            FloatField('23', lambda s, i, v: s.not_implemented() if i['archer_msa_deduction'] else None),
            FloatField('24a', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else None),
            FloatField('24b', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else None),
            FloatField('24c', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else None),
            FloatField('24d', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else None),
            FloatField('24e', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else None),
            FloatField('24f', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else None),
            FloatField('24g', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else None),
            FloatField('24h', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else None),
            FloatField('24i', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else None),
            FloatField('24j', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else None),
            FloatField('24k', lambda s, i, v: s.not_implemented() if i['uncommon_deductions'] else None),
            FloatField('24z', lambda s, i, v: i['other_adjustments_amount'] if i['need_other_adjustments'] else None),
            FloatField('25', lambda s, i, v: sum([v[f'24{l}'] for l in "abcdefghijkz"])),
            FloatField('26', lambda s, i, v: sum([v[f'{n}'] for n in list(range(11,19)) + list(range(20,24))]) + v['19a'] + v['25']),
        ]
        required_fields = [
            StringField('8z_type', lambda s, i, v: other_income(s, i, v)[0]),
            StringField('24z_type', lambda s, i, v: i['other_adjustments_type'] if i['need_other_adjustments'] else None),
        ]

        pdf_fields = [
            TextPDFField('form1[0].Page1[0].f1_01[0]', '1040.full_names'),
            TextPDFField('form1[0].Page1[0].f1_02[0]', '1040.you_ssn', max_length=11),
            TextPDFField('form1[0].Page1[0].f1_03[0]', '1'),
            TextPDFField('form1[0].Page1[0].f1_04[0]', '2a'),
            TextPDFField('form1[0].Page1[0].f1_05[0]', '2b'),
            TextPDFField('form1[0].Page1[0].f1_06[0]', '3'),
            TextPDFField('form1[0].Page1[0].f1_07[0]', '4'),
            TextPDFField('form1[0].Page1[0].f1_08[0]', '5'),
            TextPDFField('form1[0].Page1[0].f1_09[0]', '6'),
            TextPDFField('form1[0].Page1[0].f1_10[0]', '7'),
            TextPDFField('form1[0].Page1[0].f1_11[0]', '8a'),
            TextPDFField('form1[0].Page1[0].f1_12[0]', '8b'),
            TextPDFField('form1[0].Page1[0].f1_13[0]', '8c'),
            TextPDFField('form1[0].Page1[0].f1_14[0]', '8d'),
            TextPDFField('form1[0].Page1[0].f1_15[0]', '8e'),
            TextPDFField('form1[0].Page1[0].f1_16[0]', '8f'),
            TextPDFField('form1[0].Page1[0].f1_17[0]', '8g'),
            TextPDFField('form1[0].Page1[0].f1_18[0]', '8h'),
            TextPDFField('form1[0].Page1[0].f1_19[0]', '8i'),
            TextPDFField('form1[0].Page1[0].f1_20[0]', '8j'),
            TextPDFField('form1[0].Page1[0].f1_21[0]', '8k'),
            TextPDFField('form1[0].Page1[0].f1_22[0]', '8l'),
            TextPDFField('form1[0].Page1[0].f1_23[0]', '8m'),
            TextPDFField('form1[0].Page1[0].f1_24[0]', '8n'),
            TextPDFField('form1[0].Page1[0].f1_25[0]', '8o'),
            TextPDFField('form1[0].Page1[0].f1_26[0]', '8p'),
#            TextPDFField('form1[0].Page1[0].Line8z_ReadOrder[0].f1_27[0]', '8z_type'),
            TextPDFField('form1[0].Page1[0].Line8z_ReadOrder[0].f1_28[0]', '8z_type'),
            TextPDFField('form1[0].Page1[0].f1_29[0]', '8z'),
            TextPDFField('form1[0].Page1[0].f1_30[0]', '9'),
            TextPDFField('form1[0].Page1[0].f1_31[0]', '10'),
            TextPDFField('form1[0].Page2[0].f2_01[0]', '11'),
            TextPDFField('form1[0].Page2[0].f2_02[0]', '12'),
            TextPDFField('form1[0].Page2[0].f2_03[0]', '13'),
            TextPDFField('form1[0].Page2[0].f2_04[0]', '14'),
            TextPDFField('form1[0].Page2[0].f2_05[0]', '15'),
            TextPDFField('form1[0].Page2[0].f2_06[0]', '16'),
            TextPDFField('form1[0].Page2[0].f2_07[0]', '17'),
            TextPDFField('form1[0].Page2[0].f2_08[0]', '18'),
            TextPDFField('form1[0].Page2[0].f2_09[0]', '19a'),
            TextPDFField('form1[0].Page2[0].Line19b_CombField[0].f2_10[0]', '19b', max_length=9),
            TextPDFField('form1[0].Page2[0].f2_11[0]', '19c'),
            TextPDFField('form1[0].Page2[0].f2_12[0]', '20'),
            TextPDFField('form1[0].Page2[0].f2_13[0]', '21'),
            TextPDFField('form1[0].Page2[0].f2_14[0]', '22'), #"Reserved for future use"
            TextPDFField('form1[0].Page2[0].f2_15[0]', '23'),
            TextPDFField('form1[0].Page2[0].f2_16[0]', '24a'),
            TextPDFField('form1[0].Page2[0].f2_17[0]', '24b'),
            TextPDFField('form1[0].Page2[0].f2_18[0]', '24c'),
            TextPDFField('form1[0].Page2[0].f2_19[0]', '24d'),
            TextPDFField('form1[0].Page2[0].f2_20[0]', '24e'),
            TextPDFField('form1[0].Page2[0].f2_21[0]', '24f'),
            TextPDFField('form1[0].Page2[0].f2_22[0]', '24g'),
            TextPDFField('form1[0].Page2[0].f2_23[0]', '24h'),
            TextPDFField('form1[0].Page2[0].f2_24[0]', '24i'),
            TextPDFField('form1[0].Page2[0].f2_25[0]', '24j'),
            TextPDFField('form1[0].Page2[0].f2_26[0]', '24k'),
#            TextPDFField('form1[0].Page2[0].Line24z_ReadOrder[0].f2_27[0]', '24z_type'),
            TextPDFField('form1[0].Page2[0].Line24z_ReadOrder[0].f2_28[0]', '24z_type'),
            TextPDFField('form1[0].Page2[0].f2_29[0]', '24z'),
            TextPDFField('form1[0].Page2[0].f2_30[0]', '25'),
            TextPDFField('form1[0].Page2[0].f2_31[0]', '26'),
        ]
        pdf_file = os.path.join(os.path.dirname(__file__), 'f1040s1.pdf')

        super().__init__(__class__, inputs, required_fields, optional_fields, pdf_fields=pdf_fields, pdf_file=pdf_file, **kwargs)

    def needs_filing(self, values):
        return True
