from types import MethodType

class FieldNotImplemented(Exception):
    def __init__(self, field_name, message_fmt="Encountered scenario we do not implement for {field_name}"):
        self.field_name = field_name
        self.message = message_fmt.format(field_name=field_name)
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

    def name(self):
        return f'{self._form.name()}.{self._name}'

    def not_implemented(self):
        """Can be called by a field it encounters a scenario which it does not
        have the logic to return a value for"""
        raise FieldNotImplemented(self.name())

    def value(self, inputs, values):
        raise NotImplementedError()

class SimpleField(Field):
    def __init__(self, name, value_lambda):
        self.value = MethodType(value_lambda, self)
        super().__init__(name)
