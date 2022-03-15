import os
import tempfile
import subprocess

from habutax import fields
from habutax import inputs
from habutax import values

fdf_header = """%FDF-1.2
%,,oe"
1 0 obj
<< /FDF << /Fields ["""

fdf_footer = """
] >> >>
endobj
trailer
<< /Root 1 0 R >>
%%EOF;
"""

class PDFFiller(object):
    def __init__(self, solution, available_forms, outfilename, flatten=True):
        self._solution = solution
        self._form_map = {f.form_name: f for f in available_forms}
        self._output_filename = outfilename
        self._pdftk = 'pdftk'
        self._flatten = flatten

        # Instances of Forms in the solution, and fields belonging to those
        # forms
        self.forms = []
        self._field_map = {}

        # Values read from solution file
        self._values = values.ValueStore()

    def _read_form_fields(self, form_name):
        # Read values in as their types from solution file's string
        # representation
        for field_name in self._solution[form_name]:
            full_name = f'{form_name}.{field_name}'
            string = self._solution[form_name][field_name]
            field = self._field_map[full_name]
            self._values[full_name] = field.from_string(string)

    def _add_form(self, full_form_name):
        split_form_name = full_form_name.split(':')
        form_instance = None
        if len(split_form_name) == 2:
            form_name = split_form_name[0]
            form_instance = split_form_name[1]
        elif len(split_form_name) != 1:
            raise RuntimeError(f'Unexpected form name: {form_name} (expected 0 or 1 colons)')
        form_name = split_form_name[0]

        if form_name not in self._form_map:
            raise NotImplementedError(f'Form {form_name} is not supported.')

        form = self._form_map[form_name](instance=form_instance)
        self.forms.append(form)

        for f in form.fields():
            assert(f not in self._field_map)
            self._field_map[f.name()] = f

        self._read_form_fields(full_form_name)

    def _create_fdf(self, data, filename):
        lines = []
        for k, v in data.items():
            lines.append(f'<< /T ({k}) /V ({v}) >>')
        with open(filename, 'w') as fdf:
            fdf.write(fdf_header)
            fdf.write("\n".join(lines))
            fdf.write(fdf_footer)

    def _fill_form(self, form, pdf_filename):
        assert form.pdf_file()
        assert len(form.pdf_fields()) > 0
        required_fields = {f.name() for f in form.required_fields()}

        fdf_map = {}
        for pdf_field in form.pdf_fields():
            field_name = pdf_field.field_name
            if "." not in field_name:
                field_name = f'{form.name()}.{field_name}'

            if field_name not in self._field_map:
                raise RuntimeError(f'PDF filler found a field absent from the specification of any supplied form: {field_name} in form {form.name()}')
            try:
                value = self._values[field_name]
                field = self._field_map[field_name]
                string_value = pdf_field.value(value, field)
            except values.UnmetDependency:
                assert field_name not in required_fields
                string_value = ""
            fdf_map[pdf_field.pdf_field_name] = string_value

        fdf_filename = f'{pdf_filename}.fdf'
        self._create_fdf(fdf_map, fdf_filename)

        cmd = [self._pdftk, form.pdf_file(), 'fill_form', fdf_filename, 'output', pdf_filename]
        if self._flatten:
            cmd.append('flatten')
        res = subprocess.run(cmd, check=True)

    def fill(self):
        for form_name in self._solution:
            # Ignore this artifact of ConfigParser
            if form_name == 'DEFAULT':
                continue
            self._add_form(form_name)

        # Filter by forms which need to be filed, and sort the remaining forms
        # by jurisdiction and then sequence number so that they are output in
        # the correct order
        filling_forms = [f for f in self.forms if f.needs_filing(self._values)]
        filling_forms.sort(key=lambda f: (f.jurisdiction, f.sequence_no))

        pdfs = []
        with tempfile.TemporaryDirectory() as tmpdirname:
            for form in filling_forms:
                if form.needs_filing(self._values):
                    pdf_filename = os.path.join(tmpdirname, f'{form.name()}.pdf')
                    self._fill_form(form, pdf_filename)
                    pdfs.append(pdf_filename)

            cmd = [self._pdftk]
            cmd.extend(pdfs)
            cmd.extend(['cat', 'output', self._output_filename])
            res = subprocess.run(cmd, check=True)
