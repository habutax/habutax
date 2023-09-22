import unittest

from .. import context

from habutax.forms.ty2023.f1040_figure_tax import figure_tax
from habutax import enum

class FigureTaxTestCase(unittest.TestCase):
    def test_figure_2023_1040_tax(self):
        scenarios = (
            (75047.08, enum.filing_status.Single, 11813),
            (98325.84, enum.filing_status.MarriedFilingJointly, 12247),
            (99999.99, enum.filing_status.HeadOfHousehold, 15788),
            (100000.00, enum.filing_status.HeadOfHousehold, 15794),
            (588939, enum.filing_status.QualifyingSurvivingSpouse, 149917.65),
            (588939, enum.filing_status.MarriedFilingJointly, 149917.65),
            (1482.40, enum.filing_status.MarriedFilingSeparately, 149),
            (8182983.94, enum.filing_status.MarriedFilingSeparately, 2992661.06),
        )
        for taxable, status, expected_tax in scenarios:
            tax = figure_tax(taxable, status)
            self.assertAlmostEqual(expected_tax, tax, places=2)

    def test_figure_2023_1040_tax_monotonically_increasing(self):
        statuses = [enum.filing_status.Single, enum.filing_status.MarriedFilingSeparately, enum.filing_status.MarriedFilingJointly, enum.filing_status.QualifyingSurvivingSpouse, enum.filing_status.HeadOfHousehold]
        for status in statuses:
            last = 0
            for taxable_income in range(0, 200, 3):
                this = figure_tax(taxable_income, status)
                self.assertGreaterEqual(this, last)
                last = this
            for taxable_income in range(200, 10000, 23):
                this = figure_tax(taxable_income, status)
                self.assertGreaterEqual(this, last)
                last = this
            for taxable_income in range(10000, 199999, 43):
                this = figure_tax(taxable_income, status)
                self.assertGreaterEqual(this, last)
                last = this
            for taxable_income in range(199999, 750000, 1967):
                this = figure_tax(taxable_income, status)
                self.assertGreaterEqual(this, last)
                last = this
