import configparser
from collections.abc import MutableMapping

class UnmetDependency(Exception):
    def __init__(self, dependency_name, message_fmt="Unmet dependency: {dependency}"):
        self.dependency = dependency_name
        self.message = message_fmt.format(dependency=dependency_name)
        super().__init__(self.message)

class ValueStore(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.values = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        try:
            return self.values[key]
        except KeyError as ke:
            raise UnmetDependency(key) from ke

    def __setitem__(self, key, value):
        self.values[key] = value

    def __delitem__(self, key):
        del self.values[key]

    def __iter__(self):
        return iter(self.values)

    def __len__(self):
        return len(self.values)

    def to_config(self, field_map):
        config = configparser.ConfigParser()
        for key, value in self.values.items():
            field = field_map[key]
            form_name, field_name = key.split('.')
            if form_name not in config:
                config[form_name] = {}
            config[form_name][field_name] = field.to_string(value)
        return config
