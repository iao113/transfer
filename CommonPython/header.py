from collections import namedtuple
from enum import Enum, unique

HeadTerm = namedtuple('HeadTerm', ['index', 'value'])

@unique
class Header(Enum):
    FILE_NAME = HeadTerm(index=0, value=0x80)
    FILE_SIZE = HeadTerm(index=0, value=0x40)
    FILE_CONTEXT = HeadTerm(index=0, value=0x20)

HEAD_SIZE = 8
