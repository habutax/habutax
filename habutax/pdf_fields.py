from types import MethodType

class PDFValueTooLong(Exception):
    def __init__(self, pdf_field_name, field_name, max_length):
        self.message = f'Value from internal field {field_name} exceeded the max length of PDF field {pdf_field_name} (which is {max_length}) and could not be written'
        self.pdf_field_name = pdf_field_name
        self.field_name = field_name
        self.max_length = max_length
        super().__init__(self.message)

class PDFInvalidChoiceValue(Exception):
    def __init__(self, pdf_field_name, field_name, choice):
        self.message = f'Value from internal field {field_name} does not map to the valid PDF field {pdf_field_name} choices (choice was {choice}) and could not be written'
        self.pdf_field_name = pdf_field_name
        self.field_name = field_name
        self.choice = choice
        super().__init__(self.message)

class PDFField(object):
    def __init__(self, pdf_field_name, field_name, value_fn=None):
        self.pdf_field_name = pdf_field_name
        self.field_name = field_name
        if value_fn is not None:
            self._value_fn = MethodType(value_fn, self)
        else:
            self._value_fn = None

    def value(self, value, field_obj):
        if self._value_fn is not None:
            return self._value_fn(value, field_obj)
        else:
            return field_obj.to_string(value)

class TextPDFField(PDFField):
    def __init__(self, name, value, max_length=None, value_fn=None):
        self.max_length = None
        super().__init__(name, value, value_fn=value_fn)

    def value(self, value, field_obj):
        value = super().value(value, field_obj)
        if self.max_length is not None and len(value) > self.max_length:
            raise PDFValueTooLong(self.pdf_field_name, self.field_name, self.max_length)
        return value

class ButtonPDFField(PDFField):
    def __init__(self, name, value, true_value, value_fn=None):
        self._true_value = true_value # The value to return when this is true
        super().__init__(name, value, value_fn=value_fn)

    def value(self, value, field_obj):
        if self._value_fn is not None:
            value = self._value_fn(value, field_obj)
        if value:
            return self._true_value
        else:
            return 'Off'

class OptionlessButtonPDFField(PDFField):
    def __init__(self, name, value, value_fn=None):
        super().__init__(name, value, value_fn=value_fn)

    def value(self, value, field_obj):
        """Should never be called - so far these are not fields which have needed output"""
        raise NotImplementedError()

class ChoicePDFField(PDFField):
    def __init__(self, name, value, choices, value_fn=None):
        self._choices = choices
        super().__init__(name, value, value_fn=value_fn)

    def value(self, value, field_obj):
        value = super().value(value, field_obj)
        if value not in self._choices:
            raise PDFInvalidChoiceValue(self.pdf_field_name, self.field_name, value)
        return value
