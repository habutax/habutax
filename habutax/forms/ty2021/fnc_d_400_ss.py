import os

from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *
from habutax.pdf_fields import *

class FormNCD400SS(Form):
    form_name = "nc_d-400_ss"
    tax_year = 2021
    description = "D-400 Schedule S"
    long_description = "N.C. Adjustments for Individuals"
    jurisdiction = Jurisdiction.NC
    sequence_no = 1

    def __init__(self, **kwargs):
        inputs = [
            FloatInput('interest_income_not_nc', description="Enter the total amount of interest received from notes, bonds, and other obligations of states and political subdivisions other than North Carolina if not included in federal adjusted gross income."),
            FloatInput('deferred_gains_opportunity_fund', description="Enter the amount of gain reinvested into a qualified Opportunity Fund under IRC section 1400Z-2 that was excluded from federal AGI."),
            FloatInput('bonus_depreciation_deducted', description="Enter 85% of the amount of any bonus depreciation deducted on your federal return (this isn't common)."),
            FloatInput('section_179_expense_difference', description="Enter 85% of the difference between the IRC section 179 expense deduction using federal limitations and the deduction using N.C. limitations (this isn't common)."),
            FloatInput('s_corp_builtin_gains', description="Enter the amount by which a shareholder’s share of S Corporation income is reduced under IRC section 1366(f)(2) for the taxable year by the amount of built-in gains tax imposed on the S Corporation under IRC section 1374 (this isn't common, and doesn't apply if you do not hold shares of an S corporation)."),
            FloatInput('federal_basis_exceeds_nc', description="Enter the amount by which your basis of property under federal law exceeds your basis of property for state purposes in the year that you dispose of the property (not common)."),
            FloatInput('net_operating_loss_deduction', description="If you deduct a net operating loss from another year on your 2021 federal return, an addition is required for the amount of net operating loss deducted and not absorbed during tax year 2021 that will be carried forward to subsequent years. Enter any amount here (this isn't common)."),
            FloatInput('tax_deducted_by_s_corp', description="Enter any amount of a shareholder’s, partner’s, or beneficiary’s share of the amount deducted under section 164 of the Code as state, local, or foreign income tax by an S Corporation, Partnership, or Estate & Trust (this is not common)."),
            FloatInput('529_contributions_wrong_purpose', description="If you took a state tax deduction for contributions made to the N.C. 529 Plan while the deduction was in effect (taxable years beginning on or after January 1, 2006 and before January 1, 2014), and in tax year 2021, you withdrew funds from the plan, enter on Line 9 the amount you deducted in prior tax years to the extent the funds withdrawn were not used for a purpose allowed under IRC section 529."),
            FloatInput('cancelled_residence_debt', description="Enter the amount of qualified principal residence debt discharged in 2021 excluded from federal gross income under IRC section 108."),
            FloatInput('employer_education_loan_payments', description="Enter the amount of payments made by your employer for qualified education loans, as defined in IRC section 221(d)(1), excluded from federal gross income under IRC section 127(c)."),
            FloatInput('business_meal_deduction', description="Enter any difference between the business-related expenses for food and beverages provided by a restaurant taken on the federal return and the amount allowed under the provisions of IRC Section 274(n), as enacted as of May 1, 2020"),
            FloatInput('discharged_student_debt', description="Enter the amount of any student loan discharged and not included in gross income under IRC 108(f)(5)"),
            FloatInput('state_local_refund', description="Enter the amount of any state or local income tax refund that is included in federal adjusted gross income."),
            FloatInput('interest_us_obligations', description="Enter the amount of any interest you received from notes, bonds, and other obligations of the United States (such as U.S. savings bonds, treasury notes and bills, etc.) or United States possessions."),
            FloatInput('social_security_rrta', description="Enter any Title 2 social security benefits received under the Social Security Act and any Tier 1 or Tier 2 railroad retirement benefits received under the Railroad Retirement Act that were included in federal adjusted gross income."),
            FloatInput('bailey_settlement', description="Enter any retirement benefits received by vested N.C. state government, N.C. local government, or gederal government retirees (Bailey Settlement) that are not taxable in North Carolina."),
            FloatInput('certain_military_retirement', description="Enter any military retirement payments received by a retired member who served at least 20 years in the military or who was medically retired from the military or payments from the Survivor Benefit Plan to a beneficiary of a retired member who served at least 20 years in the military or who was medically retired from the military which you are not deducting under the Bailey Settlement."),
            FloatInput('bonus_asset_basis', description="In the event of an actual or deemed transfer of an asset occurring on or after January 1, 2013, wherein the tax basis of the asset carries over from the transferor to the transferee for federal income tax purposes, the transferee must add any remaining bonus depreciation deductions allowed to the basis of the transferred asset and depreciate the adjusted basis over any remaining life of the asset. The transferor is not allowed any future bonus depreciation deductions. Enter that amount here. (For more information, see G.S. 105-153.6(e) and (f), as well as the NC Department of Revenue’s website.)"),
            BooleanInput('bonus_depreciation', description="Did you have any bonus depreciation deduction added to the federal adjusted gross income on your 2016, 2017, 2018, 2019, and 2020 state tax returns?"),
            FloatInput('bonus_depreciation_2016', description="You may enter an amount to deduct from your NC taxable income equal to 20% of the bonus depreciation deduction added to federal adjusted gross income on your 2016 state tax returns."),
            FloatInput('bonus_depreciation_2017', description="You may enter an amount to deduct from your NC taxable income equal to 20% of the bonus depreciation deduction added to federal adjusted gross income on your 2017 state tax returns."),
            FloatInput('bonus_depreciation_2018', description="You may enter an amount to deduct from your NC taxable income equal to 20% of the bonus depreciation deduction added to federal adjusted gross income on your 2018 state tax returns."),
            FloatInput('bonus_depreciation_2019', description="You may enter an amount to deduct from your NC taxable income equal to 20% of the bonus depreciation deduction added to federal adjusted gross income on your 2019 state tax returns."),
            FloatInput('bonus_depreciation_2020', description="You may enter an amount to deduct from your NC taxable income equal to 20% of the bonus depreciation deduction added to federal adjusted gross income on your 2020 state tax returns."),
            BooleanInput('section_179_expense', description="Did you have any IRC section 179 expense deductions added to federal adjusted gross income on your 2016, 2017, 2018, 2019, or 2020 state tax returns?"),
            FloatInput('section_179_expense_2016', description="Enter 20% of the IRC section 179 expense deduction added to federal adjusted gross income on your 2016 state tax return, if any."),
            FloatInput('section_179_expense_2017', description="Enter 20% of the IRC section 179 expense deduction added to federal adjusted gross income on your 2017 state tax return, if any."),
            FloatInput('section_179_expense_2018', description="Enter 20% of the IRC section 179 expense deduction added to federal adjusted gross income on your 2018 state tax return, if any."),
            FloatInput('section_179_expense_2019', description="Enter 20% of the IRC section 179 expense deduction added to federal adjusted gross income on your 2019 state tax return, if any."),
            FloatInput('section_179_expense_2020', description="Enter 20% of the IRC section 179 expense deduction added to federal adjusted gross income on your 2020 state tax return, if any."),
            FloatInput('section_1400z-2_gain', description="You may deduct a gain included in federal adjusted gross income under IRC section 1400Z-2 to the extent the same amount was included in the calculation of N.C. taxable income in a prior tax year. Enter any such amount here."),
            FloatInput('nc_obligations_disposition', description="You may deduct the gain from the sale or disposition of North Carolina obligations issued before July 1, 1995, from adjusted gross income if the law under which the obligations were issued specifically exempts the gain. Enter any such amount."),
            FloatInput('indian_tribe_exempt_income', description="Enter any income from 2021 which was earned or received by an enrolled member of any federally recognized Indian tribe and was derived from activities on any federally recognized Indian reservation while the member resides on the reservation. Income from intangibles having a situs on the reservation and retirement income associated with activities on the reservation are considered income derived from activities on the reservation."),
            FloatInput('state_basis_exceeds_federal', description="Enter any amount by which the NC state basis exceeded the federal cost basis for property disposed of in 2021."),
            FloatInput('business_expense_disallowed', description="You may deduct the amount by which the deduction for an ordinary and necessary business expense was required to be reduced or was not allowed under the Code because you claimed a federal tax credit against your federal income tax liability in lieu of a deduction. This deduction is allowed only to the extent North Carolina does not allow a similar credit for the amount. Enter any such amount here."),
            FloatInput('personal_education_savings', description="You may deduct the amount deposited during the taxable year to a personal education savings account (“PESA”) under Article 41 of Chapter 115C of the NC General Statues to the extent the deposit is included in calculating federal adjusted gross income. Enter any such amount here."),
            FloatInput('state_emergency_disaster', description="You may deduct the amount paid from the State Emergency Response and Disaster Relief Reserve Fund for hurricane relief assistance to the extent this amount is included in federal adjusted gross income. Enter any such amount here."),
            FloatInput('certain_economic_incentive', description="You may deduct the amount received as an economic incentive pursuant to G.S. 143B-437.012 or Part 2G or Part 2H of Article 10 of G.S.  143B to the extent this amount is included in federal adjusted gross income. Enter any such amount here."),
            FloatInput('certain_nc_grants', description="You may deduct the amount of the Extra Credit Grant or Business Recovery Grant payment you received in tax year 2021 to the extent the payment is included in calculating federal adjusted gross income. Enter any such amount here."),
            FloatInput('certain_net_operating_loss_carrybacks', description="You may deduct an amount equal to 20% of the Net Operating Loss Carryback added to federal adjusted gross income under G.S. 105-153.5(c2) (8), (9), or (10) on your 2013 through 2019 state tax return. Enter any such amount here."),
            FloatInput('certain_net_operating_loss_carryforward', description="You may deduct an amount equal to 20% of the Excess Net Operating Loss Carryforward Deduction added to federal adjusted gross income on your 2019 and 2020 state tax return. Enter any such amount here."),
            FloatInput('excess_business_loss', description="You may deduct an amount equal to 20% of the Excess Business Loss added to federal adjusted gross income on your 2018, 2019, and 2020 state tax return. Enter any such amount here."),
            FloatInput('business_interest_limitation', description="You may deduct an amount equal to 20% of the Business Interest Limitation added to federal adjusted gross income on your 2019 and 2020 state tax return. Enter any such amount here."),
        ]

        optional_fields = [
            # Part A. Additions to Federal Adjusted Gross Income (If you have
            # items that are not included in federal adjusted gross income but
            # are taxable to North Carolina, complete Lines 1 through 15.)
            FloatField('1', lambda s, i, v: i['interest_income_not_nc'], places=0),
            FloatField('2', lambda s, i, v: i['deferred_gains_opportunity_fund'], places=0),
            FloatField('3', lambda s, i, v: i['bonus_depreciation_deducted'], places=0),
            FloatField('4', lambda s, i, v: i['section_179_expense_difference'], places=0),
            FloatField('5', lambda s, i, v: i['s_corp_builtin_gains'], places=0),
            FloatField('6', lambda s, i, v: i['federal_basis_exceeds_nc'], places=0),
            FloatField('7', lambda s, i, v: i['net_operating_loss_deduction'], places=0),
            FloatField('8', lambda s, i, v: i['tax_deducted_by_s_corp'], places=0),
            FloatField('9', lambda s, i, v: i['529_contributions_wrong_purpose'], places=0),
            FloatField('10', lambda s, i, v: i['cancelled_residence_debt'], places=0),
            FloatField('11', lambda s, i, v: i['employer_education_loan_payments'], places=0),
            FloatField('12', lambda s, i, v: i['business_meal_deduction'], places=0),
            FloatField('13', lambda s, i, v: i['discharged_student_debt'], places=0),
            FloatField('14', lambda s, i, v: 0.0, places=0), # "reserved for future use"
            FloatField('15', lambda s, i, v: sum([v[f'{f}'] for f in range(1, 15)]), places=0), # total additions to federal AGI

            # Part B. Deductions from Federal Adjusted Gross Income (If you
            # have items of income that are included in federal adjusted gross
            # income but are not taxable to North Carolina, complete Lines 16
            # through 38.
            FloatField('16', lambda s, i, v: i['state_local_refund'], places=0),
            FloatField('17', lambda s, i, v: i['interest_us_obligations'], places=0),
            FloatField('18', lambda s, i, v: i['social_security_rrta'], places=0),
            FloatField('19', lambda s, i, v: i['bailey_settlement'], places=0),
            FloatField('20', lambda s, i, v: i['certain_military_retirement'], places=0),
            FloatField('21', lambda s, i, v: i['bonus_asset_basis'], places=0),
            FloatField('22a', lambda s, i, v: i['bonus_depreciation_2016'] if i['bonus_depreciation'] else None, places=0),
            FloatField('22b', lambda s, i, v: i['bonus_depreciation_2017'] if i['bonus_depreciation'] else None, places=0),
            FloatField('22c', lambda s, i, v: i['bonus_depreciation_2018'] if i['bonus_depreciation'] else None, places=0),
            FloatField('22d', lambda s, i, v: i['bonus_depreciation_2019'] if i['bonus_depreciation'] else None, places=0),
            FloatField('22e', lambda s, i, v: i['bonus_depreciation_2020'] if i['bonus_depreciation'] else None, places=0),
            FloatField('22f', lambda s, i, v: v['22a'] + v['22b'] + v['22c'] + v['22d'] + v['22e'], places=0),
            FloatField('23a', lambda s, i, v: i['section_179_expense_2016'] if i['section_179_expense'] else None, places=0),
            FloatField('23b', lambda s, i, v: i['section_179_expense_2017'] if i['section_179_expense'] else None, places=0),
            FloatField('23c', lambda s, i, v: i['section_179_expense_2018'] if i['section_179_expense'] else None, places=0),
            FloatField('23d', lambda s, i, v: i['section_179_expense_2019'] if i['section_179_expense'] else None, places=0),
            FloatField('23e', lambda s, i, v: i['section_179_expense_2020'] if i['section_179_expense'] else None, places=0),
            FloatField('23f', lambda s, i, v: v['23a'] + v['23b'] + v['23c'] + v['23d'] + v['23e'], places=0),
            FloatField('24', lambda s, i, v: i['section_1400z-2_gain'], places=0),
            FloatField('25', lambda s, i, v: i['nc_obligations_disposition'], places=0),
            FloatField('26', lambda s, i, v: i['indian_tribe_exempt_income'], places=0),
            FloatField('27', lambda s, i, v: i['state_basis_exceeds_federal'], places=0),
            FloatField('28', lambda s, i, v: i['business_expense_disallowed'], places=0),
            FloatField('29', lambda s, i, v: i['personal_education_savings'], places=0),
            FloatField('30', lambda s, i, v: i['state_emergency_disaster'], places=0),
            FloatField('31', lambda s, i, v: i['certain_economic_incentive'], places=0),
            FloatField('32', lambda s, i, v: i['certain_nc_grants'], places=0),
            FloatField('33', lambda s, i, v: i['certain_net_operating_loss_carrybacks'], places=0),
            FloatField('34', lambda s, i, v: i['certain_net_operating_loss_carryforward'], places=0),
            FloatField('35', lambda s, i, v: i['excess_business_loss'], places=0),
            FloatField('36', lambda s, i, v: i['business_interest_limitation'], places=0),
            FloatField('37', lambda s, i, v: 0.0, places=0), # "reserved for future use"
            # Add Lines 16 through 21, 22f, 23f, and 24 through 37
            FloatField('38', lambda s, i, v: sum([v[f'{f}'] for f in range(16, 22)]) + v['22f'] + v['23f'] + sum([v[f'{f}'] for f in range(24, 38)]), places=0),
        ]

        required_fields = [
            StringField('last_name', lambda s, i, v: i['1040.last_name'][:10]),
            StringField('ssn', lambda s, i, v: i['1040.you_ssn'][:3] + "-" + i['1040.you_ssn'][3:5] + "-" + i['1040.you_ssn'][5:]),
        ]

        pdf_fields = [
#            TextPDFField('PRINT', 'DO NOT HANDWRITE ON THIS FORM'),
            TextPDFField('y_d400wf_lname2_PG2', 'last_name', max_length=10),
            TextPDFField('y_d400schswf_ssn', 'ssn'),
            TextPDFField('y_d400schswf_li1_good', '1', max_length=8),
            TextPDFField('y_d400schswf_li2_good', '2', max_length=8),
            TextPDFField('y_d400schswf_li3_good', '3', max_length=8),
            TextPDFField('y_d400schswf_li4_good', '4', max_length=8),
            TextPDFField('y_d400schswf_li5_good', '5', max_length=8),
            TextPDFField('y_d400schswf_li6_good', '6', max_length=8),
            TextPDFField('y_d400schswf_li7_good', '7', max_length=8),
            TextPDFField('y_d400schswf_li8_good', '8', max_length=8),
            TextPDFField('y_d400schswf_li9_good', '9', max_length=8),
            TextPDFField('y_d400schswf_li10_good', '10', max_length=8),
            TextPDFField('y_d400schswf_li11_good', '11', max_length=8),
            TextPDFField('y_d400schswf_li12_good', '12', max_length=8),
            TextPDFField('y_d400schswf_li13_good', '13', max_length=8),
#            TextPDFField('y_d400wf_reserved1', '14_reserved_for_future_use', max_length=32),
#            TextPDFField('y_d400schswf_li14_good', '14', max_length=8),
            TextPDFField('y_d400schswf_li15_good', '15', max_length=8),
            #OptionlessButtonPDFField('z_d400swf_print', 'unknown'),
            #OptionlessButtonPDFField('z_d400schswf_clear', 'unknown'),
            TextPDFField('y_d400schswf_li16_good', '16', max_length=8),
            TextPDFField('y_d400schswf_li17_good', '17', max_length=8),
            TextPDFField('y_d400schswf_li18_good', '18', max_length=8),
            TextPDFField('y_d400schswf_li19_good', '19', max_length=8),
            TextPDFField('y_d400schswf_li20_good', '20', max_length=8),
            TextPDFField('y_d400schswf_li21_good', '21', max_length=8),
            TextPDFField('y_d400schswf_li22a_good', '22a', max_length=8),
            TextPDFField('y_d400schswf_li22b_good', '22b', max_length=8),
            TextPDFField('y_d400schswf_li22c_good', '22c', max_length=8),
            TextPDFField('y_d400schswf_li22d_good', '22d', max_length=8),
            TextPDFField('y_d400schswf_li22e_good', '22e', max_length=8),
            TextPDFField('y_d400schswf_li22f_good', '22f', max_length=8),
            TextPDFField('y_d400schswf_li23a_good', '23a', max_length=8),
            TextPDFField('y_d400schswf_li23b_good', '23b', max_length=8),
            TextPDFField('y_d400schswf_li23c_good', '23c', max_length=8),
            TextPDFField('y_d400schswf_li23d_good', '23d', max_length=8),
            TextPDFField('y_d400schswf_li23e_good', '23e', max_length=8),
            TextPDFField('y_d400schswf_li23f_good', '23f', max_length=8),
            TextPDFField('y_d400schswf_li24_good', '24', max_length=8),
            TextPDFField('y_d400schswf_li25_good', '25', max_length=8),
            TextPDFField('y_d400schswf_li26_good', '26', max_length=8),
            TextPDFField('y_d400schswf_li27_good', '27', max_length=8),
            TextPDFField('y_d400schswf_li28_good', '28', max_length=8),
            TextPDFField('y_d400schswf_li29_good', '29', max_length=8),
            TextPDFField('y_d400schswf_li30_good', '30', max_length=8),
            TextPDFField('y_d400schswf_li31_good', '31', max_length=8),
            TextPDFField('y_d400schswf_li32_good', '32', max_length=8),
            TextPDFField('y_d400schswf_li33_good', '33', max_length=8),
            TextPDFField('y_d400schswf_li34_good', '34', max_length=8),
            TextPDFField('y_d400schswf_li35_good', '35', max_length=8),
            TextPDFField('y_d400schswf_li36_good', '36', max_length=8),
#            TextPDFField('y_d400wf_reserved2', '37_reserved_for_future_use', max_length=32),
#            TextPDFField('y_d400schswf_li37_good', '37', max_length=8),
            TextPDFField('y_d400schswf_li38_good', '38', max_length=8),
        ]
        pdf_file = os.path.join(os.path.dirname(__file__), 'fnc_d-400_ss.pdf')

        super().__init__(__class__, inputs, required_fields, optional_fields, pdf_fields=pdf_fields, pdf_file=pdf_file, **kwargs)

    def needs_filing(self, values):
        return True
