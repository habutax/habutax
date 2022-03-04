# Adding and Modifying Tax Forms

This page aims to explain how to add or modify tax forms in HabuTax. It assumes
that you [have a basic understanding of how the solver works](solver.md).

# Creating a New Form

Each form (i.e. Form 1040 for tax year 2021) is represented by its own class,
which descends from the Form class (defined in [form.py](../habutax/form.py)).

Here is a simple form with a three inputs and two fields defined:

example code: f0000.py
```python
from habutax.form import Form
from habutax.inputs import *
from habutax.fields import *

class Form0000(Form):
    # A string containing the name of the form. This is the name other
    # forms/fields will use to reference inputs or fields from this form
    form_name = "0000"

    # The tax year the form is applicable for (should match the directory it is
    # placed in
    tax_year = 2021

    def __init__(self, **kwargs):
        # Build a list of the possible inputs needed by fields defined below.
        # The types of inputs
        inputs = [
            FloatInput('base_tax', description="How many taxes are due for everyone?"),
            BooleanInput('nice', description="Have you been nice this year?"),
            FloatInput('naughty_tax', description="How many taxes should you pay for being naughty?"),
        ]

        required_fields = []

        def line_2(self, inputs, field_values):
            if inputs['nice']:
                return field_values['1']
            else:
                return field_values['1'] + inputs['naughty_tax']

        optional_fields = [
            FloatField('1', lambda s, i, v: i['base_tax']),
            FloatField('2', line_2),
        ]

        # Call the constructor of our parent class (Form). We always pass
        # `kwargs`  through here to allow for the generic instantiation of Form
        # subclasses  by the solver framework.
        super().__init__(__class__, inputs, required_fields, optional_fields, **kwargs)
```

Notice: If adding a new form to HabuTax, you'll need to also ensure the form is
added to the `available_forms` list in `__init__.py` in that tax year's form
directory. For 2021, this would be found at `habutax/forms/ty2021/__init__.py`
relative to the root of the source directory.

# Field Logic

Nearly all of the brains/logic of a form is contained within the definitions of
its field `value()` functions. In the f0000.py example above, these functions
are the lambda or function passed as the second argument in the creation of a
field (the first is its name).

Note that specifying them as a lambda inside the definition of the field itself
works the same as specifying them as functions and passing them in. For example,
the field for line 2 in the f0000.py example could also have been written as:
```python
    FloatField('2', lambda s, i, v: v['1'] if i['nice'] else v['1'] + v['naughty_tax']),
```

## Field value lambda or function

As we previously said, most of interesting logic of a form is performed inside
its fields' value functions, so lets explore how they work. 

To start, there are three parameters passed in to field value functions:

* **self/s**: This is a reference to the Field\* instance to which it belongs.
  In fact, the function you pass in is bound to that instance by the Field\*
  constructor(s) as proper method (in other words, even though the `line2` value
  function is defined within the scope `Form0000.__init__` in our example,
  `self` will refer to the Field\* instance when it is called.
* **inputs/i**: This is a dictionary-like object through which a field can
  access required inputs. In the definition of field "2" above, `i['base_tax']`
  returns the boolean value from the `FloatInput` named "base_tax".
* **field_values/v**: This is a dictionary-like object through which a field can
  access the results produced by other fields' value methods. In the definition
  of field "2" above in `def line_2`, `field_values['1']` returns the value
  produced by the `FloatField` named "1".

Note that it is not necessary to use the same names for these parameters as
shown above. You'll frequently find them shortened to 's', 'i', and 'v' within
the existing forms for convenience.

## Dependencies are implicit, not explicit

You may notice that there are no explicit dependencies specified by fields.
This is because a field's dependencies on inputs and/or other fields are
specified only by referencing them in its value method. This is important to
understand if you are implementing form logic, because it has real implications
for which inputs are required of the user and which fields are calculated and
included in returns.

In particular, if you want a particular input/field to only be required in
certain situations, it should only be referenced once you have checked other
conditions to be sure it is required. If one field's value method
unconditionally references a dependency, that dependency will be unconditionally
required any time that field is.

In the definition of `line_2` in the above example (repeated below), we can see
that the 'naughty_tax' input is only referenced if the boolean 'nice' input is
False:

```python
def line_2(self, inputs, field_values):
    if inputs['nice']:
        return field_values['1']
    else:
        return field_values['1'] + inputs['naughty_tax']
```

As long as the user reports that 'nice' is True, the 'naughty_tax' value is not
required to be provided as input by the user. The same logic applies to
referencing other fields: If a field's value is not referenced by any other
field, it will not be filled out (unless passed in as one of the required fields
in its form's constructor, if another field on that form is referenced).

If you need to require that a field's value be calculated without using the
value within a field, you should reference its value (simply accessing it on the
field_values dictionary-like object passed into the field's value method is
enough).

## Declining to supply field output

In some cases, it may be unnecessary to write a value to a form field (if it is
0, or otherwise found to be unneeded). In these cases, you can return `None`.
Any other fields accessing this field's value will, however, still see that its
value is the empty value (0 for IntegerFields, 0.0 for FloatFields, "" for
String Fields, False for BooleanFields).

The main difference between specifying None vs. 0 (or 0.0, etc.) is that fields
returning values of None will not be included in the output (either to text file
or PDF), while fields returning a legal value will be.

## Referencing fields or inputs from other forms

In the example above, you see that other fields and inputs are referenced by
name within field value methods. However, so far the examples have only used
part of their name. Field and input objects' 'full' names contain a reference to
the field defining them, but we are able to access them without specifying this
full name to make it easier to refer to them by their 'local' names within the
defining form.

For example, because `self.form().name()` returns the name of a field's form, we
could re-write `field_values['1']` as `field_values[f'{self.form().name()}.1']`
inside `def line_2` above. You likely won't ever need to reference the current
form in this way, but this functionality provides the ability to query field
(and even input) values produced by other forms. This is useful, for example,
when Form 1040 needs to include the output of another form in its own
calculations.

In fact, as mentioned above, because dependencies are implicit rather than
explicit, referencing another form in this way causes that form, and the
referenced field in particular, to be included and solved. This is the mechanism
used to require and include forms from other forms in HabuTax.

## Multiple instances of the same form

Sometimes multiple copies of the same form are needed (for instance, when filing
federal taxes married filing jointly, it can be required to have a copy of some
forms for each spouse, or there may be multiple W-2s, 1099s, etc.). To handle
this, HabuTax supports naming 'instances' of forms to differentiate between
copies. By default forms have an empty 'instance name', and are named by the
`form_name` defined on their class ('0000' in the example above). To give a form
an instance name, reference that form's fields using the form's base name plus a
colon followed by a string representing the instance name. For example, if form
'0000' was required to be filled out independently by both the taxpayer and
their spouse, you might reference both fields `0000:taxpayer.2` and
`0000:spouse.2`. This would cause two copies of form '0000' to be created and
independently recursively solved for field '2'.

All forms have their own section in the input files specified by the user. When
no instance name is supplied by the form field(s) requiring another form, that
form is named by its base name in the input. When a field uses an instance name,
the corresponding section in the input file must be named the same way. So, if a
form required field `0000:taxpayer.2` to be filled out, the input might look
like:

```
[0000:taxpayer]
base_tax = 124.87
nice = yes
```

But if `0000.2` was instead referenced by the field with the dependency upon
this form, this would need to appear in the input file as:

```
[0000]
base_tax = 124.87
nice = yes
```

Sometimes it is not possible to know ahead of time exactly how many forms of a
particular type will be required (i.e. W-2s, 1099s). One strategy for tackling
these is to have one input field request the user to enter the number of a
particular type of form they need. For example, you might ask the user how many W-2s they
have to enter via a form input like).

```python
IntegerInput('number_w-2s', description='How many, if any, forms W-2 were you provided with for this tax year?')
```

You could then require `number_w-2s` instances of the form named `w-2`, and
return the total of all their `box_1`s with a field value method like:

```python
def line_1(self, inputs, field_values):
    if inputs['number_w-2s'] > 0:
        return sum([field_values[f'w-2:{n}.box_1'] for n in range(inputs['number_w-2s'])])
    else:
        return None
```

## Actions available through value method's `self`

As previously mentioned, the `self` argument to a field's value method provides
access to all the methods available on that field.

### Not implemented behavior

Because HabuTax seeks to fail loudly when it encounters a situation it does not
know how to handle, it is sometimes necessary for a field to be able to indicate
it has encountered a situation it cannot (or does not) know how to handle. When
a field encounters a situation in its value method, you should call:

```python
self.not_implemented()
```

This notifies the solver that the field has encountered a situation it does not
implement and that the tax form cannot be successfully/correctly solved given
the current inputs and form implementation.

### Accessing form instances

It is sometimes necessary to access things defined on the form itself. For
example, if an enum is defined for a form (perhaps as part of an EnumInput, see
the fsomething.py example below), you may need a reference to the enum in order
to check if the supplied input value matches a particular enum value. Using the
'EYES' enum from the fsomething.py example, we could check if the supplied eye
color was green using a snippet like the following:

```python
if i['eye_color'] == self.form('something').EYES.green:
    # Do a special calculation for green-eyed taxpayers
```

Note that if you want to reference the field's own form, you may omit the form
name argument like: `self.form().EYES.green`.

# Input-only Forms

Some forms are input-only, like forms W-2, 1099-INT. Because such forms do not
need any special field calculations (their values match their inputs), an
InputForm class is defined which will automatically create Field objects to
match all specified Input objects for any form which inherits from it. Below is
a simple example, and you can see [tax year 2021 form
W-2](../habutax/forms/ty2021/fw-2.py) for a more complete example.

example code: fsomething.py
```python
import habutax.enum as enum
from habutax.form import InputForm
from habutax.inputs import *

class FormSomething(InputForm):
    form_name = "something"
    tax_year = 2021

    def __init__(self, **kwargs):
        self.EYES = enum.make("eye color", {
            'blue': 'your eyes are blue',
            'brown': 'your eyes are brown',
            'green': 'your eyes are green',
            'hazel': 'your eyes are hazel',
            'other': 'your eyes are some other color'
        })
        inputs = [
            StringInput('name', description='What is your name?'),
            SSNInput('ssn', description='What is your social security number?'),
            EnumInput('eye_color', self.EYES, description='What color are your eyes?')
        ]

        super().__init__(__class__, inputs, **kwargs)
```

Note that all inputs passed into the InputForm `super()` constructor here become
**required** fields.

# Input Types

The type of a input primarily specifies the types of checks done on its input
(whether provided via a textual input file or HabuTax's interactive prompt). The
types of form inputs are:

* StringInput
* BooleanInput
* IntegerInput
* FloatInput
* EnumInput
* RegexInput (produces strings)
* SSNInput (produces strings)

See [inputs.py](../habutax/inputs.py) in the source for more details.

# Field Types

The type of a field primarily specifies the types of checks done on its output
(whatever is returned from its `value()` method). The types of form fields are:

* StringField
* BooleanField
* IntegerField
* FloatField
* EnumField

See [fields.py](../habutax/fields.py) in the source for more details.
