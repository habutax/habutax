import math
from habutax.form import Form

class Form8962(Form):
    """
    HabuTax Module: Form 8962 (Premium Tax Credit)
    Calculates the PTC based on 1040 MAGI and 1095-A Marketplace Data.
    """

    def __init__(self, solver):
        super().__init__(solver)
        self.form_id = "8962"
        self.dependencies = ["1040", "1095A"]

        # FPL Tables 
        self.fpl_tables = {
            2024: {1: 15060, 2: 20440, 3: 25820, 4: 31200, 5: 36580, 6: 41960},
            2025: {1: 15650, 2: 21150, 3: 26650, 4: 32150, 5: 37650, 6: 43150}
        }

    def _get_fpl_threshold(self, tax_year, family_size):
        year_table = self.fpl_tables.get(tax_year, self.fpl_tables[2025])
        size = min(family_size, 6) 
        return year_table.get(size, 15650)

    def line_1(self):
        return self.solver.get_field("1040", "family_size") or 1

    def line_2a(self):
        agi = self.solver.get_field("1040", "line_11") or 0.0
        exempt_int = self.solver.get_field("1040", "line_2a") or 0.0
        return agi + exempt_int

    def line_3(self):
        magi = self.line_2a()
        fpl_threshold = self._get_fpl_threshold(self.solver.tax_year, self.line_1())
        if fpl_threshold == 0: return 0
        return math.floor((magi / fpl_threshold) * 100)

    def line_7(self):
        fpl_pct = self.line_3()
        if fpl_pct <= 150: return 0.0000
        elif fpl_pct >= 400: return 0.0850
        else: return min(0.0850, (fpl_pct - 150) * 0.00034)

    def line_8a(self):
        return round(self.line_2a() * self.line_7())

    def line_11(self):
        annual_premium = self.solver.get_field("1095A", "annual_enrollment_premiums") or 0.0
        annual_slcsp = self.solver.get_field("1095A", "annual_slcsp") or 0.0
        annual_aptc = self.solver.get_field("1095A", "annual_aptc") or 0.0
        
        contribution = self.line_8a()
        max_credit = max(0.0, annual_slcsp - contribution)
        return {
            "e": min(annual_premium, max_credit),
            "f": annual_aptc
        }

    def line_26_and_27(self):
        data = self.line_11()
        net_ptc = data["e"] - data["f"]

        if net_ptc > 0:
            return {"line_26_refundable_ptc": round(net_ptc), "line_27_excess_repayment": 0.0}
        elif net_ptc < 0:
            return {"line_26_refundable_ptc": 0.0, "line_27_excess_repayment": round(abs(net_ptc))}
        return {"line_26_refundable_ptc": 0.0, "line_27_excess_repayment": 0.0}
