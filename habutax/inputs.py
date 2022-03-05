from collections.abc import MutableMapping
import configparser
import re

from habutax.enum import StringyEnum

class Input(object):
    def __init__(self, name, description=None):
        assert("." not in name)
        self._name = name
        self._description = description if description is not None else name

    def __form_init__(self, form):
        """Called when this Input is associated with a form instance"""
        self._form = form

    def section(self):
        return self._form.name()

    def base_name(self):
        """Return the name relative to the form it is in"""
        return self._name

    def name(self):
        return f'{self.section()}.{self.base_name()}'

    def help(self):
        return self._description + '\n'

    def value(self, string):
        raise NotImplementedError()

    def valid(self, string):
        try:
            self.value(string)
        except ValueError:
            return False
        return True

class StringInput(Input):
    def value(self, string):
        return string.strip()

class BooleanInput(Input):
    def value(self, string):
        string = string.strip().lower()
        if string in ['true', 'yes', 'y', '1']:
            return True
        if string in ['false', 'no', 'n', '0']:
            return False
        raise ValueError(f'Invalid boolean value: {string}')

class IntegerInput(Input):
    def value(self, string):
        string = string.strip()
        if len(string) == 0:
            return 0
        return int(string)

class FloatInput(Input):
    def value(self, string):
        string = string.strip()
        if len(string) == 0:
            return 0.0
        return float(string)

class EnumInput(StringInput):
    def __init__(self, name, enum, description=""):
        """
        Create an instance to read/validate an input that can be one of a
        limited number of choices. The `options` parameter can be a list of
        the available choices or a dictionary mapping the choice names to brief
        descriptions of what they mean.
        """
        description = "" if (len(description) == 0 or description == None) else (description + '\n\n')
        description += "Valid values:\n"
        for k, v in enum.__members__.items():
            description += f'    {k}: {v.value}\n'
        description = description.strip()

        super().__init__(name, description=description)
        self.enum = enum

    def __form_init__(self, form):
        super().__form_init__(form)

    def __getattr__(self, attribute):
        return self.enum[attribute]

    def valid(self, string):
        try:
            string = super().value(string)
        except ValueError:
            return False

        try:
            self.enum[string]
        except KeyError as ke:
            return False
        return True

    def value(self, string):
        string = super().value(string)
        return self.enum[string]

class RegexInput(StringInput):
    def __init__(self, name, regex, description=""):
        self._regex = re.compile(regex)
        super().__init__(name, description=description)

    def valid(self, string):
        try:
            v = self.value(string)
        except ValueError:
            return False

        return bool(self._regex.match(v))

class SSNInput(StringInput):
    def value(self, string):
        v = super().value(string)
        return v.replace("-", "")

    def valid(self, string):
        try:
            ssn = self.value(string)
        except ValueError:
            return False

        if len(ssn) != 9:
            return False
        for n in ssn:
            if n not in "0123456789":
                return False
        return True

class MissingInputSpecification(Exception):
    def __init__(self, input_name, message_fmt="Missing input specification for {input_name}"):
        self.input_name = input_name
        self.message = message_fmt.format(input_name=input_name)
        super().__init__(self.message)

class MissingInput(Exception):
    def __init__(self, input_name, message_fmt="Unsupplied Input: {input_name}"):
        self.input_name = input_name
        self.message = message_fmt.format(input_name=input_name)
        super().__init__(self.message)

class InvalidInput(Exception):
    def __init__(self, input_name, invalid_value, message_fmt="Invalid Input: {input_name} (currently: '{value}')"):
        self.input_name = input_name
        self.value = invalid_value
        self.message = message_fmt.format(input_name=input_name, value=invalid_value)
        super().__init__(self.message)

class InputStore(MutableMapping):
    def __init__(self, filename, input_specs={}):
        self.config = configparser.ConfigParser()
        self.config.read(filename)
        self.input_specs = input_specs

    def write(self, filename):
        with open(filename, 'w') as outfile:
            self.config.write(outfile)

    def update_input_spec(self, input_specs):
        self.input_specs = input_specs

    def provides(self, input_obj):
        return self.config.has_option(input_obj.section(), input_obj.base_name())

    def __getitem__(self, key):
        if key not in self.input_specs:
            raise MissingInputSpecification(key)

        i = self.input_specs[key]
        if not self.provides(i):
            raise MissingInput(key)
        string = self.config.get(i.section(), i.base_name())
        if not i.valid(string):
            raise InvalidInput(key, string)
        return i.value(string)

    def __setitem__(self, key, value):
        if key not in self.input_specs:
            raise MissingInputSpecification(key)
        i = self.input_specs[key]
        if i.section() not in self.config.sections():
            self.config.add_section(i.section())
        self.config.set(i.section(), i.base_name(), value)

    def __delitem__(self, key):
        raise NotImplementedError()
        if key not in self.input_specs:
            raise MissingInputSpecification(key)
        i = self.input_specs[key]
        self.config.remove_option(i.section(), i.base_name())
        if len(self.config[i.section()]) == 0:
            self.config.remove_section(i.section())

    def __iter__(self):
        return iter(self.config)

    def __len__(self):
        return len(self.config)
