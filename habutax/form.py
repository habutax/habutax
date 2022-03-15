from collections.abc import Mapping
from enum import IntEnum, auto, unique

from habutax.inputs import StringInput, BooleanInput, IntegerInput, FloatInput, EnumInput, SSNInput
from habutax.fields import StringField, BooleanField, IntegerField, FloatField, EnumField

class AutoNumber(IntEnum):
    def _generate_next_value_(name, start, count, last_values):
        return 0 if len(last_values) == 0 else max(last_values) + 1

@unique
class Jurisdiction(AutoNumber):
    # US Federal
    US = auto()
    # US state
    AK = auto()
    AL = auto()
    AR = auto()
    AZ = auto()
    CA = auto()
    CO = auto()
    CT = auto()
    DC = auto()
    DE = auto()
    FL = auto()
    GA = auto()
    HI = auto()
    IA = auto()
    ID = auto()
    IL = auto()
    IN = auto()
    KS = auto()
    KY = auto()
    LA = auto()
    MA = auto()
    MD = auto()
    ME = auto()
    MI = auto()
    MN = auto()
    MO = auto()
    MS = auto()
    MT = auto()
    NC = auto()
    ND = auto()
    NE = auto()
    NH = auto()
    NJ = auto()
    NM = auto()
    NV = auto()
    NY = auto()
    OH = auto()
    OK = auto()
    OR = auto()
    PA = auto()
    PR = auto()
    RI = auto()
    SC = auto()
    SD = auto()
    TN = auto()
    TX = auto()
    UT = auto()
    VA = auto()
    VT = auto()
    WA = auto()
    WI = auto()
    WV = auto()
    WY = auto()

class Form(object):
    def __init__(self,
                 child_cls,
                 inputs,
                 required_fields,
                 optional_fields,
                 pdf_fields=[],
                 pdf_file=None,
                 instance=None,
                 solver=None):

        self._name = child_cls.form_name
        assert("." not in self._name)
        self._tax_year = child_cls.tax_year
        self._inputs = inputs
        self._required_fields = required_fields
        self._optional_fields = optional_fields
        self._pdf_fields = pdf_fields
        self._pdf_file = pdf_file
        self._instance = instance
        self._solver = solver

        for i in self._inputs:
            i.__form_init__(self)
        for f in self._required_fields + self._optional_fields:
            f.__form_init__(self)

    def name(self):
        if self._instance is None:
            return self._name
        else:
            return f'{self._name}:{self._instance}'

    def full_description(self):
        return f'{self.__class__.description}: {self.__class__.long_description}'

    def instance(self):
        return self._instance

    def solver(self):
        assert(self._solver)
        return self._solver

    def inputs(self):
        return self._inputs

    def required_fields(self):
        return self._required_fields

    def fields(self):
        return self.required_fields() + self._optional_fields

    def pdf_fields(self):
        return self._pdf_fields

    def pdf_file(self):
        return self._pdf_file

    def needs_filing(self, values):
        raise NotImplementedError()

class InputForm(Form):
    """Convenience class to create a form which creates fields for each
    input"""
    def __init__(self,
                 child_cls,
                 inputs,
                 **kwargs):

        fields = []
        for i in inputs:
            base_name = i.base_name()
            fn = lambda s, i, v, base_name=base_name: i[base_name]

            if type(i) in [StringInput, SSNInput]:
                fields.append(StringField(base_name, fn))
            elif type(i) is BooleanInput:
                fields.append(BooleanField(base_name, fn))
            elif type(i) is IntegerInput:
                fields.append(IntegerField(base_name, fn))
            elif type(i) is FloatInput:
                fields.append(FloatField(base_name, fn))
            elif type(i) is EnumInput:
                fields.append(EnumField(base_name, i.enum, fn))
            else:
                raise TypeError(f'Unexpected input type in InputForm: {type(i)}')

        super().__init__(child_cls, inputs, fields, [], **kwargs)

    def needs_filing(self, values):
        # For typical input-only forms like W-2, 1099, 1098, habutax does not
        # need to present them to be filed because the user already has copies
        # of them
        return False

class FormAccessor(Mapping):
    def __init__(self, mapping, form):
        self.form = form
        self.mapping = mapping

    def __getitem__(self, key):
        if "." not in key:
            key = f'{self.form.name()}.{key}'
        return self.mapping[key]

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)

def name_and_instance(full_form_name):
    split_form_name = full_form_name.split(':')
    form_instance = None
    if len(split_form_name) == 2:
        form_instance = split_form_name[1]
    elif len(split_form_name) != 1:
        raise RuntimeError(f'Unexpected form name: {full_form_name} (expected 0 or 1 colons)')
    return split_form_name[0], form_instance
