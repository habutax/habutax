from collections.abc import MutableMapping

import configparser
from enum import Enum

class ConfigInput(object):
    def __init__(self, name, description=None):
        assert("." not in name)
        self._name = name
        self._description = description if description is not None else name

    def __form_init__(self, form):
        """Called when this ConfigInput is associated with a form instance"""
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

    def provided(self, config):
        return config.has_option(self.section(), self.base_name())

    def value(self, config):
        raise NotImplementedError()

    def valid(self, config):
        try:
            self.value(config)
        except (ValueError, configparser.NoOptionError):
            return False
        return True

class StringInput(ConfigInput):
    def value(self, config):
        return config.get(self.section(), self.base_name())

class BooleanInput(ConfigInput):
    def value(self, config):
        return config.getboolean(self.section(), self.base_name())

class IntegerInput(ConfigInput):
    def value(self, config):
        string = config.get(self.section(), self.base_name())
        if len(string) == 0:
            return 0
        return config.getint(self.section(), self.base_name())

class FloatInput(ConfigInput):
    def value(self, config):
        string = config.get(self.section(), self.base_name())
        if len(string) == 0:
            return 0.0
        return config.getfloat(self.section(), self.base_name())

class EnumInput(StringInput):
    def __init__(self, name, options, description=""):
        """
        Create an instance to read/validate an input that can be one of a
        limited number of choices. The `options` parameter can be a list of
        the available choices or a dictionary mapping the choice names to brief
        descriptions of what they mean.
        """
        description = "" if (len(description) == 0 or description == None) else (description + '\n\n')
        description += "Valid values:\n"
        if isinstance(options, dict):
            for k, v in options:
                description += f'    {k}: {v}\n'
        else:
            for opt in options:
                description += f'    {opt}\n'
        description = description.strip()

        super().__init__(name, description=description)
        self.options = options

    def __form_init__(self, form):
        super().__form_init__(form)
        self.enum = Enum(self.name(), self.options)

    def __getattr__(self, attribute):
        return self.enum[attribute]

    def valid(self, config):
        try:
            string = super().value(config)
        except (ValueError, configparser.NoOptionError):
            return False

        try:
            self.enum[string]
        except KeyError as ke:
            return False
        return True

    def value(self, config):
        string = super().value(config)
        return self.enum[string]

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

    def __getitem__(self, key):
        if key not in self.input_specs:
            raise MissingInputSpecification(key)

        i = self.input_specs[key]
        if not i.provided(self.config):
            raise MissingInput(key)
        elif not i.valid(self.config):
            raise InvalidInput(key, self.config.get(i.section(), i.base_name()))
        return i.value(self.config)

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
        del self.config[key]

    def __iter__(self):
        return iter(self.config)

    def __len__(self):
        return len(self.config)
