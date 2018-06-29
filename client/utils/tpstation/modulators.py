import os
import time
import glob

from pathlib import Path

DTU_SOCKS = Path("/sys/bus/usb/drivers/Dtu/")
DTA_SOCKS = Path("/sys/bus/pci/drivers/Dta/")
DTA_DEV = Path("/sys/bus/pci/devices/")
DTA_RESCAN = Path("/sys/bus/pci/rescan")
BIND = Path("/sys/bus/usb/drivers/usb/bind")
UNBIND = Path("/sys/bus/usb/drivers/usb/unbind")


def __unbind_usb_device(socket):
    with UNBIND.open('w') as file_:
        file_.write(socket)


def __bind_usb_device(socket):
    with BIND.open('w') as file_:
        file_.write(socket)


def __reset_pci_device(socket):
    dta_dev = Path(DTA_DEV, socket, "reset")
    with dta_dev.open('w') as file_:
        file_.write("1")


def __remove_pci_device(socket):
    dta_dev = Path(DTA_DEV, socket, "remove")
    with dta_dev.open('w') as file_:
        file_.write("1")


def __rescan_pci_device():
    with DTA_RESCAN.open('w') as file_:
        file_.write("1")


def get_list_of_dektec_devices():
    dta_devices_names = map(lambda x: x.name , Path(DTA_SOCKS).glob('*[0-9]'))
    dtu_devices_names = map(lambda x: x.name , Path(DTU_SOCKS).glob('*[0-9]'))

    dta_devices = list(dta_devices_names)
    # Remove all chars after ":" in "1-2:1.0", return string like 1-2
    dtu_devices = [x.split(':')[0] for x in dtu_devices_names]
    return dtu_devices, dta_devices


def reconnect_mods(logfile):
    dtu_dev, dta_dev = get_list_of_dektec_devices()
    for socket in dtu_dev:
        __unbind_usb_device(socket)
        logfile.write("#INFO: USB modulator {} unbinded!\n".format(socket))
        time.sleep(3)
        __bind_usb_device(socket)
        logfile.write("#INFO: USB modulator {} binded again!\n".format(socket))
    for socket in dta_dev:
        __reset_pci_device(socket)
        __remove_pci_device(socket)
        __rescan_pci_device()
        logfile.write("#INFO: PCI modulator {} reinitialized!\n".format(socket))
        time.sleep(3)
