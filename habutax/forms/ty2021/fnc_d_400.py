import os

import habutax.enum as enum
from habutax.form import Form, Jurisdiction
from habutax.inputs import *
from habutax.fields import *
from habutax.pdf_fields import *

class FormNCD400(Form):
    form_name = "nc_d-400"
    tax_year = 2021
    description = "D-400"
    long_description = "N.C. 2021 Individual Income Tax Return"
    jurisdiction = Jurisdiction.NC
    sequence_no = 0

    def __init__(self, **kwargs):
        inputs = [
            StringInput('county', description="Enter the North Carolina county in which you resided on the last day of 2021. Your county of residence may be different than the county of your mailing address."),
            BooleanInput('out_of_country', description="Were you or, if married filing jointly, your spouse were out of the country on the statutory due date of the return?"),
            BooleanInput('nc_residents', description="Were you, and your spouse if filing jointly, residents of N.C. for the entire year of 2021?"),
            BooleanInput('veteran', description="Are you a veteran?"),
            BooleanInput('spouse_veteran', description="Is your spouse a veteran?"),
            BooleanInput('federal_extension', description="Were you granted an automatic extension to file your 2021 federal income tax return, e.g., Form 1040?"),
            IntegerInput('year_spouse_died', description="Which year did your spouse die?"),
            BooleanInput('additions_to_agi', description="Do you have any additions you are required to add to your federal adjusted gross income for your North Carolina return? If unsure, answer \"yes\" and you will be prompted for them individually."),
            BooleanInput('deductions_from_agi', description="Do you have any deductions you are allowed to make from your federal adjusted gross income for your North Carolina return? If unsure, answer \"yes\" and you will be prompted for them individually."),
            BooleanInput('try_itemizing', description="Would you you like to see if itemizing on your NC State tax return saves you money? Even if you answer \"yes\" here, we will only itemize if it helps you."),
            BooleanInput('partial_year_or_nonresident', description="Were you (or your spouse if filing jointly) a part-year resident or a nonresident of NC? You are a “part-year resident” if you moved to N.C. and became a resident during the tax year, or you moved out of N.C. and became a resident of another state during the tax year. You are a “nonresident” if you were not a resident of N.C. at any time during the tax year."),
            BooleanInput('nc_tax_credits', description="Do you want to claim any NC tax credits? These include credits for income tax paid to another state or country, rehabilitating historic structures, business incentive and energy tax credits, or credits carried over from previous years."),
            BooleanInput('no_consumer_use_tax', description="Do you certify that no Consumer Use Tax is due to North Carolina?"),
            BooleanInput('amended_return', description="Is this an amended NC state return? (HabuTax does not support this)"),
            FloatInput('estimated_tax', description="Enter any estimated North Carolina income tax payments for tax year 2021 (including any portion of your 2020 refund that was applied to your 2021 estimated income tax)."),
            FloatInput('paid_with_extension', description="If you previously applied for a N.C. extension (Form D-410), enter the amount of North Carolina income tax paid with the extension."),
            FloatInput('partnership_payments', description="If you are a nonresident partner in a partnership doing business in North Carolina, enter your share of the income tax paid to North Carolina by the manager of the partnership on your distributive share of the partnership income. Include with your return a copy of Form NC K-1 for Form D-403 provided by the partnership to verify the amount claimed (you must do this outside of HabuTax)"),
            FloatInput('s_corp_payments', description="If you are a nonresident shareholder of an S Corporation doing business in North Carolina, enter your share of the income tax paid to North Carolina by the S Corporation on your distributive share of the S Corporation income. Include with your return a copy of Form NC K-1 for Form CD-401S provided by the S Corporation to verify the amount claimed.(you must do this outside of HabuTax)"),
            BooleanInput('late', description="Are you filing this return after the original due date?"),
            FloatInput('interest_on_underpayment', description="It is possible you owe interest because you have underpaid your NC income tax. Please complete NC Form D-422 to determine the amount, if any, of interest you owe and enter that amount here."),
            FloatInput('2022_estimated_income_tax', description="Enter the amount, if any, of your NC state refund you want applied to 2022 estimated tax"), 
            FloatInput('nc_nongame_endangered_wildlife', description="Enter the amount, if any, of your NC state refund you want to contribute to the NC Nongame and Endangered Wildlife Fund"), 
            FloatInput('nc_education_endowment', description="Enter the amount, if any, of your NC state refund you want to contribute to the N.C Education Endowment Fund"), 
            FloatInput('nc_breast_cervical_cancer', description="Enter the amount, if any, of your NC state refund you want to contribute to the N.C Breast and Cervical Cander Control Program"), 
        ]

        def tax_withheld(self, i, v, belongs_to):
            nc_withholding = 0.0
            for n in range(i['1040.number_w-2']):
                if v[f'w-2:{n}.belongs_to'] not in belongs_to:
                    continue
                if v[f'w-2:{n}.box_15'] == enum.us_states.NC:
                    nc_withholding += v[f'w-2:{n}.box_17']
            for n in range(i['1040.number_1099-g']):
                if v[f'1099-g:{n}.belongs_to'] not in belongs_to:
                    continue
                if v[f'1099-g:{n}.box_10a_1'] == enum.us_states.NC:
                    nc_withholding += v[f'1099-g:{n}.box_11_1']
                if v[f'1099-g:{n}.box_10a_2'] == enum.us_states.NC:
                    nc_withholding += v[f'1099-g:{n}.box_11_2']
            for n in range(i['1040.number_1099-int']):
                if v[f'1099-int:{n}.belongs_to'] not in belongs_to:
                    continue
                if v[f'1099-int:{n}.box_15_1'] == enum.us_states.NC:
                    nc_withholding += v[f'1099-int:{n}.box_17_1']
                if v[f'1099-int:{n}.box_15_2'] == enum.us_states.NC:
                    nc_withholding += v[f'1099-int:{n}.box_17_2']
            for n in range(i['1040.number_1099-div']):
                if v[f'1099-div:{n}.belongs_to'] not in belongs_to:
                    continue
                if v[f'1099-div:{n}.box_14_1'] == enum.us_states.NC:
                    nc_withholding += v[f'1099-div:{n}.box_16_1']
                if v[f'1099-div:{n}.box_14_2'] == enum.us_states.NC:
                    nc_withholding += v[f'1099-div:{n}.box_16_2']
            for n in range(i['1040.number_1099-r']):
                if v[f'1099-r:{n}.belongs_to'] not in belongs_to:
                    continue
                if v[f'1099-r:{n}.box_14_1_state'] == enum.us_states.NC:
                    nc_withholding += v[f'1099-r:{n}.box_14_1']
                if v[f'1099-r:{n}.box_14_2_state'] == enum.us_states.NC:
                    nc_withholding += v[f'1099-r:{n}.box_14_2']
            return nc_withholding

        def your_tax_withheld(self, i, v):
            return tax_withheld(self, i, v, [enum.taxpayer_or_spouse.taxpayer, enum.taxpayer_spouse_or_both.taxpayer, enum.taxpayer_spouse_or_both.both])

        def spouses_tax_withheld(self, i, v):
            return tax_withheld(self, i, v, [enum.taxpayer_or_spouse.spouse, enum.taxpayer_spouse_or_both.spouse])

        required_fields = [
            StringField('you_ssn', lambda s, i, v: i['1040.you_ssn'][:3] + "-" + i['1040.you_ssn'][3:5] + "-" + i['1040.you_ssn'][5:]),
            StringField('spouse_ssn', lambda s, i, v: i['1040.spouse_ssn'][:3] + "-" + i['1040.spouse_ssn'][3:5] + "-" + i['1040.spouse_ssn'][5:] if i['1040.filing_status'] == s.form('1040').FILING_STATUS.MarriedFilingJointly else None),
            StringField('your_first_name', lambda s, i, v: i['1040.first_name'].upper()),
            StringField('your_middle_initial', lambda s, i, v: i['1040.middle_initial'].upper()),
            StringField('your_last_name', lambda s, i, v: i['1040.last_name'].upper()),
            StringField('spouse_first_name', lambda s, i, v: i['1040.spouse_first_name'].upper() if i['1040.filing_status'] == s.form('1040').FILING_STATUS.MarriedFilingJointly else None),
            StringField('spouse_middle_initial', lambda s, i, v: i['1040.spouse_middle_initial'].upper() if i['1040.filing_status'] == s.form('1040').FILING_STATUS.MarriedFilingJointly else None),
            StringField('spouse_last_name', lambda s, i, v: i['1040.spouse_last_name'].upper() if i['1040.filing_status'] == s.form('1040').FILING_STATUS.MarriedFilingJointly else None),
            StringField('mailing_address', lambda s, i, v: i['1040.home_address'].upper()),
            StringField('apartment_no', lambda s, i, v: i['1040.apartment_no'].upper()),
            StringField('city', lambda s, i, v: i['1040.city'].upper()),
            StringField('state', lambda s, i, v: str(i['1040.state'])),
            StringField('zip', lambda s, i, v: i['1040.zip'].upper()),
            StringField('country', lambda s, i, v: i['1040.foreign_country'].upper()),
            StringField('county', lambda s, i, v: i['county'].upper()[:5]),
            StringField('phone_number', lambda s, i, v: i['1040.phone_number']),
            BooleanField('out_of_country', lambda s, i, v: i['out_of_country']),
            BooleanField('nc_residents', lambda s, i, v: i['nc_residents']),
            BooleanField('veteran', lambda s, i, v: i['veteran']),
            BooleanField('spouse_veteran', lambda s, i, v: i['spouse_veteran'] if i['1040.filing_status'] == s.form('1040').FILING_STATUS.MarriedFilingJointly else None),
            BooleanField('federal_extension', lambda s, i, v: i['federal_extension']),
            BooleanField('1', lambda s, i, v: i['1040.filing_status'] == s.form('1040').FILING_STATUS.Single),
            BooleanField('2', lambda s, i, v: i['1040.filing_status'] == s.form('1040').FILING_STATUS.MarriedFilingJointly),
            BooleanField('3', lambda s, i, v: i['1040.filing_status'] == s.form('1040').FILING_STATUS.MarriedFilingSeparately),
            BooleanField('4', lambda s, i, v: i['1040.filing_status'] == s.form('1040').FILING_STATUS.HeadOfHousehold),
            BooleanField('5', lambda s, i, v: i['1040.filing_status'] == s.form('1040').FILING_STATUS.QualifyingWidowWidower),
            StringField('separate_spouse_name', lambda s, i, v: f'i["1040.first_name"] i["1040.middle_initial"] i["1040.last_name"]'.upper() if v['3'] else None),
            StringField('separate_spouse_ssn', lambda s, i, v: i['1040.spouse_ssn'][:3] + "-" + i['1040.spouse_ssn'][3:5] + "-" + i['1040.spouse_ssn'][5:] if v['3'] else None),
            StringField('year_spouse_died', lambda s, i, v: i['year_spouse_died'] if v['5'] else None),
            FloatField('6', lambda s, i, v: v['1040.11'], places=0),
            FloatField('7', lambda s, i, v: v['nc_d-400_ss.15'] if i['additions_to_agi'] else None, places=0),
            FloatField('8', lambda s, i, v: v['6'] + v['7'], places=0),
            FloatField('9', lambda s, i, v: v['nc_d-400_ss.38'] if i['deductions_from_agi'] else None, places=0),
            IntegerField('10a', lambda s, i, v: v['nc_d-400_child_deduction_wkst.3']),
            FloatField('10b', lambda s, i, v: v['nc_d-400_child_deduction_wkst.5'] if v['10a'] > 0 else None, places=0),
            BooleanField('11_itemizing', lambda s, i, v: i['try_itemizing'] and v['nc_d-400_sa.deduction'] > v['nc_d-400_sa.nc_standard_deduction']),
            FloatField('11', lambda s, i, v: v['nc_d-400_sa.deduction'] if v['11_itemizing'] else v['nc_d-400_sa.nc_standard_deduction'], places=0),
            FloatField('12a', lambda s, i, v: v['9'] + v['10b'] + v['11'], places=0),
            FloatField('12b', lambda s, i, v: v['8'] - v['12a'], places=0),
            FloatField('13', lambda s, i, v: s.not_implemented() if i['partial_year_or_nonresident'] else None, places=0),
            FloatField('14', lambda s, i, v: s.not_implemented() if i['partial_year_or_nonresident'] else v['12b'], places=0),
            FloatField('15', lambda s, i, v: v['14'] * 0.0525, places=0), # NC Income Tax
            FloatField('16', lambda s, i, v: s.not_implemented() if i['nc_tax_credits'] else None, places=0),
            FloatField('17', lambda s, i, v: v['15'] - v['16'], places=0),
            BooleanField('no_consumer_use_tax', lambda s, i, v: i['no_consumer_use_tax']),
            FloatField('18', lambda s, i, v: None if v['no_consumer_use_tax'] else v['nc_d-400_consumer_use_tax_wkst.consumer_use_tax'], places=0),
            FloatField('19', lambda s, i, v: v['17'] + v['18'], places=0),
            FloatField('20a', your_tax_withheld, places=0),
            FloatField('20b', spouses_tax_withheld, places=0),
            FloatField('21a', lambda s, i, v: i['estimated_tax'], places=0),
            FloatField('21b', lambda s, i, v: i['paid_with_extension'], places=0),
            FloatField('21c', lambda s, i, v: i['partnership_payments'], places=0),
            FloatField('21d', lambda s, i, v: i['s_corp_payments'], places=0),
            FloatField('22', lambda s, i, v: s.not_implemented() if i['amended_return'] else None, places=0),
            FloatField('23', lambda s, i, v: v['20a'] + v['20b'] + v['21a'] + v['21b'] + v['21c'] + v['21d'] + v['22'], places=0),
            FloatField('24', lambda s, i, v: s.not_implemented() if i['amended_return'] else None, places=0),
            FloatField('25', lambda s, i, v: v['23'] - v['24'], places=0),
            FloatField('refund', lambda s, i, v: v['34'] if v['19'] <= v['25'] else -v['27'], places=0), # Fake "field" to ensure only correct portion is filled
        ]

        optional_fields = [
            # Tax due
            FloatField('26a', lambda s, i, v: v['19'] - v['25'] if v['19'] > v['25'] else s.not_implemented(), places=0),
            FloatField('26b', lambda s, i, v: s.not_implemented() if i['late'] else None, places=0),
            FloatField('26c', lambda s, i, v: s.not_implemented() if i['late'] else None, places=0),
            FloatField('26d', lambda s, i, v: v['26b'] + v['26c'], places=0),
            FloatField('26e', lambda s, i, v: i['interest_on_underpayment'] if (v['17'] - (v['20a'] + v['20b']) >= 1000) else None, places=0),
            FloatField('27', lambda s, i, v: v['26a'] + v['26d'] + v['26e'], places=0),

            # Overpayment
            FloatField('28', lambda s, i, v: v['25'] - v['19'] if v['19'] <= v['25'] else s.not_implemented(), places=0),
            FloatField('29', lambda s, i, v: i['2022_estimated_income_tax'], places=0),
            FloatField('30', lambda s, i, v: i['nc_nongame_endangered_wildlife'], places=0),
            FloatField('31', lambda s, i, v: i['nc_education_endowment'], places=0),
            FloatField('32', lambda s, i, v: i['nc_breast_cervical_cancer'], places=0),
            FloatField('33', lambda s, i, v: v['29'] + v['30'] + v['31'] + v['32'], places=0),
            FloatField('34', lambda s, i, v: v['28'] - v['33'] if v['28'] >= v['33'] else s.not_implemented(), places=0),
        ]

        pdf_fields = [
#            TextPDFField('PRINT', 'OTHER THAN YOUR SIGNATURE, DO NOT HANDWRITE ON THIS FORM'),
            #OptionlessButtonPDFField('z_d400wf_clear', 'unknown'),
            #OptionlessButtonPDFField('z_d400wf_print', 'unknown'),
#            TextPDFField('y_d400wf_datebeg', 'fiscal_year_beginning'),
#            ButtonPDFField('y_d400wf_amendedreturn', 'unknown', 'Yes'),
#            TextPDFField('y_d400wf_dateend', 'fiscal_year_ending'),
            TextPDFField('y_d400wf_ssn1', 'you_ssn'),
            TextPDFField('y_d400wf_ssn2', 'spouse_ssn'),
            TextPDFField('y_d400wf_fname1', 'your_first_name', max_length=25),
            TextPDFField('y_d400wf_mi1', 'your_middle_initial', max_length=1),
            TextPDFField('y_d400wf_lname1', 'your_last_name', max_length=25),
            TextPDFField('y_d400wf_fname2', 'spouse_first_name', max_length=25),
            TextPDFField('y_d400wf_mi2', 'spouse_middle_initial', max_length=1),
            TextPDFField('y_d400wf_lname2', 'spouse_last_name', max_length=25),
            TextPDFField('y_d400wf_add', 'mailing_address', max_length=50),
            TextPDFField('y_d400wf_apartment number', 'apartment_no', max_length=5),
            TextPDFField('y_d400wf_city', 'city', max_length=27),
            ChoicePDFField('y_d400wf_state', 'state', [' ', 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']),
            TextPDFField('y_d400wf_zip', 'zip', max_length=10),
            TextPDFField('y_d400wf_country', 'country', max_length=9),
            TextPDFField('y_d400wf_county', 'county', max_length=5),
#            TextPDFField('y_d400wf_NCEDU_good', 'nc_education_endowment_fund', max_length=9),
            ButtonPDFField('y_d400wf_Out of Country', 'out_of_country', 'Yes'),
#            ButtonPDFField('y_d400wf_Signed by Executor or Administrator', 'unknown', 'Yes'),
#            TextPDFField('y_d400wf_dead1', 'unknown'),
#            TextPDFField('y_d400wf_dead2', 'unknown'),
            ButtonPDFField('y_d400wf_rs1yes', 'nc_residents', 'Yes'),
            ButtonPDFField('y_d400wf_rs1no', 'nc_residents', 'Yes', lambda s, v, f: not v),
            ButtonPDFField('y_d400wf_rs2yes', 'nc_residents', 'Yes'),
            ButtonPDFField('y_d400wf_rs2no', 'nc_residents', 'Yes', lambda s, v, f: not v),
            ButtonPDFField('y_d400wf_v1yes', 'veteran', 'Yes'),
            ButtonPDFField('y_d400wf_v2no', 'veteran', 'Yes', lambda s, v, f: not v),
            ButtonPDFField('y_d400wf_sv1yes', 'spouse_veteran', 'Yes'),
            ButtonPDFField('y_d400wf_sv1no', 'spouse_veteran', 'Yes', lambda s, v, f: not v),
            ButtonPDFField('y_d400wf_fedex1yes', 'federal_extension', 'Yes'),
            ButtonPDFField('y_d400wf_fedex1no', 'federal_extension', 'Yes', lambda s, v, f: not v),
            ButtonPDFField('y_d400wf_fstat1', '1', 'Yes'),
            ButtonPDFField('y_d400wf_fstat2', '2', 'Yes'),
            ButtonPDFField('y_d400wf_fstat3', '3', 'Yes'),
            ButtonPDFField('y_d400wf_fstat4', '4', 'Yes'),
            ButtonPDFField('y_d400wf_fstat5', '5', 'Yes'),
            TextPDFField('y_d400wf_sname2', 'separate_spouse_name', max_length=36),
            TextPDFField('y_d400wf_sssn2', 'separate_spouse_name'),
#            ChoicePDFField('y_d400wf_dead3', 'year_spouse_died', [' ', '2019', '2020']),
            TextPDFField('y_d400wf_li6_good', '6', max_length=9),
            TextPDFField('y_d400wf_li7_good', '7', max_length=8),
            TextPDFField('y_d400wf_li8_good', '8', max_length=9),
            TextPDFField('y_d400wf_li9_good', '9', max_length=8),
            TextPDFField('y_d400wf_li10a_good', '10a', max_length=2),
            TextPDFField('y_d400wf_li10b_good', '10b', max_length=5),
            ButtonPDFField('y_d400wf_ncstandarddeduction', '11_itemizing', 'Yes', lambda s, v, f: not v),
            ButtonPDFField('y_d400wf_ncitemizeddeduction', '11_itemizing', 'Yes'),
            TextPDFField('y_d400wf_li11_page1_good', '11', max_length=8),
            TextPDFField('y_d400wf_li12a_pg1_good', '12a', max_length=9),
            TextPDFField('y_d400wf_li12b_pg1_good', '12b', max_length=9),
            TextPDFField('y_d400wf_li13_page1_good', '13', max_length=6),
            TextPDFField('y_d400wf_li14_pg1_good', '14', max_length=9),
            TextPDFField('y_d400wf_li15_pg1_good', '15', max_length=8),
            TextPDFField('y_d400wf_lname2_PG2', 'your_last_name', max_length=10),
            TextPDFField('y_d400wf_li16_pg2_good', '16', max_length=8),
            TextPDFField('y_d400wf_li17_pg2_good', '17', max_length=8),
            ButtonPDFField('y_d400wf_Consumer Use Tax', 'no_consumer_use_tax', 'Yes'),
            TextPDFField('y_d400wf_li18_pg2_good', '18', max_length=8),
            TextPDFField('y_d400wf_li19_pg2_good', '19', max_length=8),
            TextPDFField('y_d400wf_li20a_pg2_good', '20a', max_length=8),
            TextPDFField('y_d400wf_li20b_pg2_good', '20b', max_length=8),
            TextPDFField('y_d400wf_li21a_pg2_good', '21a', max_length=8),
            TextPDFField('y_d400wf_li21b_pg2_good', '21b', max_length=8),
            TextPDFField('y_d400wf_li21c_pg2_good', '21c', max_length=8),
            TextPDFField('y_d400wf_li21d_pg2_good', '21d', max_length=8),
            TextPDFField('y_d400wf_li22_pg2_good', '22', max_length=8),
            TextPDFField('y_d400wf_li23_pg2_good', '23', max_length=8),
            TextPDFField('y_d400wf_li24_pg2_good', '24', max_length=8),
            TextPDFField('y_d400wf_li25_pg2_good', '25', max_length=9),
            TextPDFField('y_d400wf_li26a_pg2_good', '26a', max_length=8),
            TextPDFField('y_d400wf_li26b_pg2_good', '26b', max_length=6),
            TextPDFField('y_d400wf_li26c_pg2_good', '26c', max_length=6),
            TextPDFField('y_d400wf_li26d_pg2_good', '26d', max_length=8),
            TextPDFField('y_d400wf_li26e_pg2_good', '26e', max_length=8),
            TextPDFField('y_d400wf_li27_pg2_good', '27', max_length=8),
#            ChoicePDFField('y_d400wf_Ex_good', 'unknown', [' ', 'A', 'F']),
            TextPDFField('y_d400wf_li28_pg2_good', '28', max_length=8),
            TextPDFField('y_d400wf_li29_pg2_good', '29', max_length=8),
            TextPDFField('y_d400wf_li30_pg2_good', '30', max_length=8),
            TextPDFField('y_d400wf_li31_pg2_good', '31', max_length=8),
            TextPDFField('y_d400wf_li32_pg2_good', '32', max_length=8),
            TextPDFField('y_d400wf_li33_pg2_good', '33', max_length=8),
            TextPDFField('y_d400wf_li34_pg2_good', '34', max_length=8),
#            TextPDFField('y_d400wf_sigdate', 'unknown'),
#            TextPDFField('y_d400wf_sigdate2', 'unknown'),
            TextPDFField('y_d400wf_dayphone', 'phone_number'),
#            ButtonPDFField('y_d400wf_check', 'unknown', 'Yes'),
#            TextPDFField('y_d400wf_ppsigdate', 'unknown'),
#            TextPDFField('y_d400wf_ppssn', 'unknown', max_length=9),
#            TextPDFField('y_d400wf_ppphoneno', 'unknown'),
    ]
        pdf_file = os.path.join(os.path.dirname(__file__), 'fnc_d-400.pdf')

        super().__init__(__class__, inputs, required_fields, optional_fields, pdf_fields=pdf_fields, pdf_file=pdf_file, **kwargs)

    def needs_filing(self, values):
        return True
