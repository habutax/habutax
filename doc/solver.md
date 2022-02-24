# How the Solver Works

HabuTax's solver begins by adding all required fields for the form(s) it is
ultimately trying to solve to a list of unsolved fields. Typically this form
would be Form 1040 or a top-level state tax form, and would be specified on the
command-line (it does not need to be a complete list of all forms which may be
required). Once the solver has a list of the fields it must solve, it loops over
all the unsolved fields:

1. Attempting to calculate each field's value (each field supplies its own
   calculation for the `Field.value()` method in
   [fields.py](../habutax/fields.py))
2. If the field's value is not able to be calculated due to missing dependencies
   (it uses un-supplied input or a value from another field whose value is still
   unknown)
   * Those dependencies are identified and the current field is marked as being
     dependent upon them
   * If a dependency exists upon another field which has not been marked as
     needing to be computed, that field is added to the list of unsolved fields.
     If the field dependency is to a field on a form we have not yet seen, that
     form's required fields are also added to the list of unsolved fields (some
     forms require fields to be filled out if the form is used at all, even if
     they are not direct dependencies)
   * If a dependency exists upon another input value, and the user has supplied
     `--prompt` on the command-line, the user is prompted for that input.
3. If the field's value **was** able to be calculated with the currently-known
   inputs and solved field values, its value is calculated and added to the
   collection of solved values. Additionally, any fields marked as dependent
   upon this one are marked as met so that they may be attempted again.
4. Once a field's dependency has been resolved, the solver attempts to calculate
   its value again. It is possible that additional unmet dependencies are
   discovered, and that the dependency-resolution process repeats for this field.
5. The solver continues iterating over all unsolved fields whose known
   dependencies are met, marking any resolved dependencies as met along the way,
   until it either solve all fields, or fails to make forward progress. Failing
   to make forward progress indicates one of
   1. missing input data,
   2. unimplemented form logic (by design), or
   3. an implementation error with the implemented form fields
