import unittest

from .. import context

from habutax.forms.ty2021.f1040_figure_tax import figure_tax
from habutax import enum

class FigureTaxTestCase(unittest.TestCase):
    def test_figure_2021_1040_tax(self):
        scenarios = (
            (75047.08, enum.filing_status.Single, 12254),
            (98325.84, enum.filing_status.MarriedFilingJointly, 13129),
            (99999.99, enum.filing_status.HeadOfHousehold, 16563.00),
            (100000.00, enum.filing_status.HeadOfHousehold, 16569.00),
            (588939, enum.filing_status.QualifyingWidowWidower, 155217.15),
            (588939, enum.filing_status.MarriedFilingJointly, 155217.15),
            (1482.40, enum.filing_status.MarriedFilingSeparately, 149),
            (8182983.94, enum.filing_status.MarriedFilingSeparately, 2995965.31),
        )
        for taxable, status, expected_tax in scenarios:
            tax = figure_tax(taxable, status)
            self.assertAlmostEqual(expected_tax, tax, places=2)
