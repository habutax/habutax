class Field(object):
    def __init__(self, name):
        self.name = name

    def value(self, inputs, values):
        raise NotImplementedError()

class SimpleField(Field):
    def __init__(self, name, value_lambda):
        self.value = value_lambda
        super().__init__(name)
