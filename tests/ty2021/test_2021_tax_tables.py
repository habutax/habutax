import unittest

from habutax.forms.ty2021.f1040_figure_tax import figure_tax
from habutax import enum


class FigureTaxTestCase(unittest.TestCase):
    def test_figure_2021_1040_tax(self):
        scenarios = (
            (75047.08, enum.filing_status_2021.Single, 12254),
            (98325.84, enum.filing_status_2021.MarriedFilingJointly, 13129),
            (99999.99, enum.filing_status_2021.HeadOfHousehold, 16563.00),
            (100000.00, enum.filing_status_2021.HeadOfHousehold, 16569.00),
            (588939, enum.filing_status_2021.QualifyingWidowWidower, 155217.15),
            (588939, enum.filing_status_2021.MarriedFilingJointly, 155217.15),
            (1482.40, enum.filing_status_2021.MarriedFilingSeparately, 149),
            (8182983.94, enum.filing_status_2021.MarriedFilingSeparately, 2995965.31),
        )
        for taxable, status, expected_tax in scenarios:
            tax = figure_tax(taxable, status)
            self.assertAlmostEqual(expected_tax, tax, places=2)
