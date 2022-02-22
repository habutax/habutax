from enum import Enum

# Mixin which changes the string formatting to only include the name
class StringyEnum(object):
    def __str__(self):
        return self.name

def make(name, options):
    assert(type(options) == dict)
    for k, v in options.items():
        assert(isinstance(k, str)) 
        assert(isinstance(v, str)) 
    return Enum(name, options, type=StringyEnum)
