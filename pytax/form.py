from collections.abc import Mapping

class Form(object):
    def __init__(self,
                 child_cls,
                 inputs,
                 required_fields,
                 optional_fields,
                 instance=None):

        self._name = child_cls.form_name
        assert("." not in self._name)
        self._tax_year = child_cls.tax_year
        self._inputs = inputs
        self._required_fields = required_fields
        self._optional_fields = optional_fields
        self._instance = instance

        for i in self._inputs:
            i.__form_init__(self)
        for f in self._required_fields + self._optional_fields:
            f.__form_init__(self)

    def name(self):
        return self._name

    def inputs(self):
        return self._inputs

    def required_fields(self):
        return self._required_fields

    def fields(self):
        return self.required_fields() + self._optional_fields

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
