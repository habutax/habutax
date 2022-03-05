import unittest

from .. import context

from habutax.forms.ty2021.f1040_figure_tax import figure_tax
from habutax import enum

class FigureTaxTestCase(unittest.TestCase):
    def setUp(self):
        self.FILING_STATUS = enum.make('1040 Filing Status', {
            'Single': "single, unmarried, or legally separated",
            'MarriedFilingJointly': "married and filing a joint return",
            'MarriedFilingSeparately': "married and file a separate return",
            'HeadOfHousehold': "unmarried and provide a home for certain other person",
            'QualifyingWidowWidower': "generally filed if your spouse died in 2019 or 2020 and you didn't remarry before the end of 2021 and you have a child or stepchild whom you can claim as a dependent (see Form 1040 instructions for more)"})

    def test_figure_2021_1040_tax(self):
        scenarios = (
            (75047.08, self.FILING_STATUS.Single, 12254),
            (98325.84, self.FILING_STATUS.MarriedFilingJointly, 13129),
            (99999.99, self.FILING_STATUS.HeadOfHousehold, 16563.00),
            (100000.00, self.FILING_STATUS.HeadOfHousehold, 16569.00),
            (588939, self.FILING_STATUS.QualifyingWidowWidower, 155217.15),
            (588939, self.FILING_STATUS.MarriedFilingJointly, 155217.15),
            (1482.40, self.FILING_STATUS.MarriedFilingSeparately, 149),
            (8182983.94, self.FILING_STATUS.MarriedFilingSeparately, 2995965.31),
        )
        for taxable, status, expected_tax in scenarios:
            tax = figure_tax(taxable, status, self.FILING_STATUS)
            self.assertAlmostEqual(expected_tax, tax, places=2)
