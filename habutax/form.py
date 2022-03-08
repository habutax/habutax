from collections.abc import Mapping

from habutax.inputs import StringInput, BooleanInput, IntegerInput, FloatInput, EnumInput, SSNInput
from habutax.fields import StringField, BooleanField, IntegerField, FloatField, EnumField

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
