from .f1040 import Form1040
from .f1040_qualdiv_capgain_tax_wkst import Form1040QualDivCapGainTaxWkst
from .f1040_recovery_rebate_credit_wkst import Form1040RecoveryRebateCreditWkst
from .f1040_s2_need6251 import Form1040S2Need6251
from .f1040_s1 import Form1040S1
from .f1040_s3 import Form1040S3
from .f1040_sa import Form1040SA
from .f1040_sb import Form1040SB
from .f1040_s8812 import Form1040S8812
from .f1098 import Form1098
from .f1099_div import Form1099DIV
from .f1099_g import Form1099G
from .f1099_int import Form1099INT
from .f1099_r import Form1099R
from .f8606 import Form8606
from .f8959 import Form8959
from .f8995 import Form8995
from .fw_2 import FormW2
from .f8889 import Form8889
from .fnc_d_400 import FormNCD400
from .fnc_d_400_child_deduction_wkst import FormNCD400ChildDeductionWkst
from .fnc_d_400_consumer_use_tax_wkst import FormNCD400ConsumerUseTaxWkst
from .fnc_d_400_ss import FormNCD400SS
from .fnc_d_400_sa import FormNCD400SA

available_forms = [
	Form1040,
	Form1040QualDivCapGainTaxWkst,
	Form1040RecoveryRebateCreditWkst,
	Form1040S1,
	Form1040S2Need6251,
	Form1040S3,
	Form1040SA,
	Form1040SB,
	Form1040S8812,
	Form1098,
	Form1099DIV,
	Form1099G,
	Form1099INT,
	Form1099R,
	Form8606,
	Form8959,
	Form8995,
	FormW2,
	Form8889,
	FormNCD400,
	FormNCD400ChildDeductionWkst,
	FormNCD400ConsumerUseTaxWkst,
	FormNCD400SS,
	FormNCD400SA,
]
