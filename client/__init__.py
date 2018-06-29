import sys

from pathlib import Path

sys.path.append(Path(__file__).parent.as_posix())

from celeryapp import app


__version__ = '9.1'
__authors__ = [
    ('ailin', 'ailin@luxoft.com'),
    ('emetelev', 'emetelev@luxoft.com'),
]
