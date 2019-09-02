"""
Helper functions for file manipulation
"""
import os
import subprocess
import tempfile
import uuid
from contextlib import contextmanager


@contextmanager
def temp_open(mode='wb', prefix=''):
    """
    Context manager for creating and opening a file temporarily, and then deleting it afterwards.
    Python does have similar utilities (see tempfile), but sometimes this flexibility is useful.
    """
    identifier = str(uuid.uuid4())
    name = '%s_%s' % (prefix, identifier) if prefix else identifier
    path = os.path.join(tempfile.gettempdir(), name)
    f = open(path, mode)
    try:
        yield f
    finally:
        f.close()
        os.unlink(path)


class PdfTextExtractionException(Exception):
    pass


def pdf_bytestring_to_text(byte_string):
    """
    Extracts text from a PDF byte string by first writing the bytes to a file and then opening a pdfminer subprocess.
    """
    with temp_open(prefix='invoice') as f:
        # Create a PDF, then close it so that pdfminer can use it
        f.write(byte_string)
        f.close()

        # pdf2txt is the command-line utility that comes bundled with pdfminer
        pdf2txt = os.path.join(os.environ['VIRTUAL_ENV'], 'bin', 'pdf2txt.py')

        # It's stored in the Scripts directory in dev environments, and in the bin directory on slaves
        if not os.path.exists(pdf2txt):
            pdf2txt = os.path.join(os.environ['VIRTUAL_ENV'], 'Scripts', 'pdf2txt.py')

        # Issues in Windows mean we can't run py2txt.py as an executable, and must instead open a Python subprocess
        args = ['python', pdf2txt, f.name]
        pipe = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # From textract: "pipe.wait() ends up hanging on large files... pipe.communicate appears to avoid this issue"
        stdout, stderr = pipe.communicate()

        # Subprocess may have failed
        if pipe.returncode != 0:
            raise PdfTextExtractionException(
                ' '.join(args), pipe.returncode, stdout, stderr,
            )

        return stdout
