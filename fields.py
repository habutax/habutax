from types import MethodType

class Field(object):
    def __init__(self, name):
        assert("." not in name)
        self._name = name

    def __form_init__(self, form):
        """Called when this ConfigInput is associated with a form instance"""
        self.form = form

    def name(self):
        return f'{self.form.name()}.{self._name}'

    def value(self, inputs, values):
        raise NotImplementedError()

class SimpleField(Field):
    def __init__(self, name, value_lambda):
        self.value = MethodType(value_lambda, self)
        super().__init__(name)
