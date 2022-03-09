from types import MethodType

class FieldNotImplemented(Exception):
    def __init__(self, field_name, message_fmt="Encountered unimplemented tax scenario when processing {field_name}", detailed=None):
        self.field_name = field_name
        self.message = message_fmt.format(field_name=field_name)
        if detailed is not None:
            self.message += f': {detailed}'
        super().__init__(self.message)

class Field(object):
    def __init__(self, name):
        assert("." not in name)
        self._name = name

    def __form_init__(self, form):
        """Called when this ConfigInput is associated with a form instance.
        This must be called before any other methods are called on the
        Field."""
        self._form = form

    def form(self, form_name=None):
        if form_name is None:
            return self._form
        else:
            return self._form.solver().forms[form_name]

    def base_name(self):
        """Return the name relative to the form it is in"""
        return self._name

    def name(self):
        return f'{self._form.name()}.{self._name}'

    def not_implemented(self, detailed=None):
        """Can be called by a field it encounters a scenario which it does not
        have the logic to return a value for"""
        raise FieldNotImplemented(self.name(), detailed=detailed)

    def value(self, inputs, values):
        raise NotImplementedError()

    def to_string(self, value):
        raise NotImplementedError()

    def from_string(self, string):
        raise NotImplementedError()

class TypedField(Field):
    def __init__(self, name, value_fn, _type):
        self._value = MethodType(value_fn, self)
        self._type = _type
        super().__init__(name)

    def value(self, inputs, values):
        v = self._value(inputs, values)
        if v is None or isinstance(v, str) and v.strip() == "":
            return self._empty_value
        elif type(v) is not self._type:
            raise TypeError(f'Field named {self.name()} expected to produce type {self._type}, but found {type(v)}.')
        return v

class BasicTypedField(TypedField):
    def to_string(self, value):
        return str(value)

    def from_string(self, string):
        return self._type(string)

class StringField(BasicTypedField):
    def __init__(self, name, value_fn):
        self._empty_value = ""
        super().__init__(name, value_fn, str)

class BooleanField(BasicTypedField):
    def __init__(self, name, value_fn):
        self._empty_value = False
        super().__init__(name, value_fn, bool)

    def from_string(self, string):
        return string.strip().lower() == 'true'

class IntegerField(BasicTypedField):
    def __init__(self, name, value_fn):
        self._empty_value = 0
        super().__init__(name, value_fn, int)

class FloatField(BasicTypedField):
    def __init__(self, name, value_fn, places=2):
        self._empty_value = 0.0
        self._places = places
        super().__init__(name, value_fn, float)

    def value(self, inputs, values):
        value = super().value(inputs, values)
        return round(value, self._places)

    def to_string(self, value):
        return f'{value:.{self._places}f}'

    def from_string(self, string):
        return round(float(string), self._places)

class EnumField(TypedField):
    def __init__(self, name, enum, value_fn):
        self._empty_value = None
        super().__init__(name, value_fn, enum)

    def enum(self):
        return self._type

    def to_string(self, value):
        if value is None:
            return ""
        return str(value)

    def from_string(self, string):
        if len(string) == 0:
            return None
        return self.enum()[string]
