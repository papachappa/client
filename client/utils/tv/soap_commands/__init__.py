import sys

from pathlib import Path

from .soap_modules.loshell import loshell
from .soap_modules.ficom import connectFi, FIError
from .soap_modules.interface import (DeleteExceptionItems, DisableNetlogging,
                                     EnableNetlogging, GetSystemInfo,
                                     GetExceptionList, GetExceptionItem,
                                     GetWakeupReasons, ControlDebug, deleteLoregKey)

from .soap_modules.soap import HttpSoapRequest
from .get_chassis import get_chassis_info
from .cam_emulator_connect import cam_emulator_connect

sys.path.append(Path(__file__).parent.as_posix())
