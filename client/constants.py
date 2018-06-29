from enum import Enum


CHASSIS_LIST = ('HL1', 'HL2')

class TEST_STATUS(Enum):
    failed = 'FAIL'
    blocked = 'BLOCK'
    passed = 'PASS'
