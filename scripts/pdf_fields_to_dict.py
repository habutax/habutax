#!/usr/bin/env python

# Note: Some PDFs (i.e. those from North Carolina) are "encrypted". You will
# probably wish to decrypt them using a qpdf command-line like:
# $ qpdf --decrypt input.pdf output.pdf
#
# Additionally, it may be helpful to remove the first page of a PDF containing
# a form if it is a page you do not wish to include in the output. This can be
# accomplished with a pdftk command-line like:
# $ pdftk input.pdf cat 2-end output chopped.pdf

import argparse
from enum import Enum
import subprocess

class PDFFieldType(Enum):
    TEXT = 0
    BUTTON = 1
    CHOICE = 2
    OPTIONLESS_BUTTON = 3

class PDFField(object):
    def __init__(self):
        self.type = None
        self.name = None
        self.max_length = None
        self.value = None
        self.choices = []

        self._finalized = False

    def finalize(self):
        assert self.name is not None
        assert self.type is not None

        if self.type == PDFFieldType.BUTTON:
            if len(self.choices) == 0:
                self.type = PDFFieldType.OPTIONLESS_BUTTON
            else:
                assert len(self.choices) == 2
                assert "Off" in self.choices
                self.choices = [c for c in self.choices if c != "Off"]
                assert len(self.choices) == 1
        elif self.type == PDFFieldType.CHOICE:
            assert len(self.choices) > 0
        elif self.type == PDFFieldType.TEXT:
            assert len(self.choices) == 0
        else:
            assert False

        self._finalized = True

    def get_value(self):
        assert(self._finalized)

        if self.type == PDFFieldType.BUTTON:
            return self.value == self.choices[0]
        elif self.type == PDFFieldType.CHOICE:
            pass
        return self.value

    def __repr__(self):
        assert(self._finalized)

        if self.type == PDFFieldType.TEXT:
            maxlength_str = ""
            if self.max_length:
                maxlength_str = f', max_length={self.max_length}'
            value = self.value
            if value is None:
                value = 'unknown'
            return f'TextPDFField(\'{self.name}\', \'{value}\'{maxlength_str})'
        elif self.type == PDFFieldType.BUTTON:
            return f'ButtonPDFField(\'{self.name}\', \'unknown\', \'{self.choices[0]}\')'
        elif self.type == PDFFieldType.CHOICE:
            return f'ChoicePDFField(\'{self.name}\', \'unknown\', {self.choices})'
        elif self.type == PDFFieldType.OPTIONLESS_BUTTON:
            return f'#OptionlessButtonPDFField(\'{self.name}\', \'unknown\')'
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pdf', type=str, help="The PDF file to print the fields of")
    parser.add_argument('--pdftk', type=str, default='pdftk', help="Path to the pdftk binary (assumed to be available on PATH if not specified)")
    parser.add_argument('--output', type=str, default=None, help="Path at which you want the resulting text file written (defaults to stdout if not specified)")
    args = parser.parse_args()


    # Parse the output of `pdftk whatever.pdf dump_data_fields` into a list of
    # PDFField instances
    res = subprocess.run([args.pdftk, args.pdf, 'dump_data_fields'], capture_output=True, text=True, check=True)

    all_fields = []
    current = None
    for line in res.stdout.splitlines():
        if line.strip() == "---":
            if current is not None:
                current.finalize()
                all_fields.append(current)
            current = PDFField()
            continue
        name, value = line.split(": ")
        if name == "FieldType":
            if value == "Button":
                current.type = PDFFieldType.BUTTON
            elif value == "Text":
                current.type = PDFFieldType.TEXT
            elif value == "Choice":
                current.type = PDFFieldType.CHOICE
            else:
                assert False, f'Unknown `FieldType`: {name}'
        elif name == "FieldMaxLength":
            current.max_length = int(value)
        elif name == "FieldName":
            current.name = value
        elif name == "FieldValue":
            current.value = value
        elif name == "FieldStateOption":
            current.choices.append(value)

    current.finalize()
    all_fields.append(current)

    # Write python representations of the PDF field types out to either stdout
    # or the specified file
    if args.output:
        with open(args.output, 'w') as outfile:
            outfile.write('    pdf_fields = [\n')
            for field in all_fields:
                outfile.write(' '*8 + repr(field) + ',\n')
            outfile.write('    ]\n')
    else:
        print('    pdf_fields = [')
        for field in all_fields:
            print(' '*8 + repr(field) + ',')
        print('    ]')

    if not args.output:
        pass

if __name__ == "__main__":
    main()
