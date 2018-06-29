import re
import time
import xml.dom.minidom as dom
from .soap import HttpSoapRequest

class FactoryInterfaceRequest(HttpSoapRequest):
    """ Base class for factory interface requests. """

    def __init__(self, host, clientId):
        """ Create a factory interface request with defined settings. """
        self._clientId = clientId
        super(FactoryInterfaceRequest, self).__init__(
            host,
            1025,
            "/ResMonTV",
            "urn:loewe.de:ResMonTV")

    def _addCallerIds(self, doc, parent_tag):
        """ Helper method to add caller ids to certain soap tag. """
        fcid_tag = doc.createElement("urn:fcid")
        parent_tag.appendChild(fcid_tag)

        id_tag = doc.createElement("urn:ClientId")
        id_txt = doc.createTextNode(self._clientId)
        id_tag.appendChild(id_txt)
        parent_tag.appendChild(id_tag)

        return parent_tag

    def _addQueryParameters(self, doc, parent_tag, startIndex=1, maxItems=300):
        """ Helper method to add query parameters to a request. """
        qp_tag = doc.createElement('urn:QueryParameters')

        range_tag = doc.createElement('urn:Range')
        range_tag.setAttribute('startIndex', str(startIndex))
        range_tag.setAttribute('maxItems', str(maxItems))
        qp_tag.appendChild(range_tag)

        parent_tag.appendChild(qp_tag)
        return parent_tag

    def _addTagWithText(self, doc, tagName, text):
        """ Helper method to create tag with text node. """
        tag = doc.createElement(tagName)
        txt = doc.createTextNode(text)
        tag.appendChild(txt)
        return tag

    def _parseAndReturnResult(self, data):
        """ Helper method to parse for and return content of result tag. """
        doc = dom.parseString(data)
        es = doc.getElementsByTagName("m:result")
        txt = es[0].firstChild.nodeValue
        return txt

class RequestAccess(FactoryInterfaceRequest):
    """ Request to get access to tv-set via factory interface. """

    def __init__(self, host):
        """ Overridden from base since no clientId is needed. """
        super(RequestAccess, self).__init__(
            host,
            "?")

    def _getAction(self):
        """ This action is used to request access to tv-set. """
        return "RequestAccess"

    def _fillSoapBody(self, doc):
        """ Fill body for RequestAccess soap action. """
        req_tag = self._addCallerIds(doc,
                                     doc.createElement("urn:RequestAccess"))

        type_tag = doc.createElement("urn:DeviceType")
        type_txt = doc.createTextNode(__file__)
        type_tag.appendChild(type_txt)
        req_tag.appendChild(type_tag)

        return req_tag

    def _parseResponse(self, data):
        """ Return clientId or 'Pending'. """
        doc = dom.parseString(data)
        states = doc.getElementsByTagName("m:AccessStatus")
        state = states[0].firstChild.nodeValue
        if state == "Pending":
            return state
        else:
            clientIds = doc.getElementsByTagName("m:ClientId")
            return clientIds[0].firstChild.nodeValue

class GetSystemInfo(FactoryInterfaceRequest):
    """ Request to get system info from tv-set via Factory interface. """

    def _getAction(self):
        """ This action is used to get system info from tv-set. """
        return "GetSystemInfo"

    def _fillSoapBody(self, doc):
        """ Fill xml body for GetSystemInfo soap action. """
        gsi_tag = self._addCallerIds(doc,
                                     doc.createElement("urn:GetSystemInfo"))
        return gsi_tag

    def _parseResponse(self, data):
        """ Return dictionary in the form {'info_name':'info_value',...}. """
        info_dict = {}
        doc = dom.parseString(data)
        tags = doc.getElementsByTagName("m:GetSystemInfoResponse")[0]\
                  .childNodes
        for tag in tags:
            if tag.nodeType == tag.ELEMENT_NODE:
                if tag.tagName == "m:fcid":
                    continue
                elif tag.tagName == "m:ClientId":
                    continue
                elif tag.tagName == "m:Software":
                    subsystem = tag.getElementsByTagName("m:Subsystem")[0]\
                                   .firstChild.nodeValue
                    version = tag.getElementsByTagName("m:Version")[0]\
                                 .firstChild.nodeValue
                    info_dict[subsystem] = version
                else:
                    if tag.firstChild != None:
                        key_name = tag.tagName.split(':')[1]
                        info_dict[key_name] = tag.firstChild.nodeValue
        return info_dict

class GetTunerInfo(FactoryInterfaceRequest):
    """ Request to get system info from tv-set via Factory interface. """

    def __init__(self, host, clientId, tuner=0):
        """ Overridden from base since we need exception uuid parameter. """
        self._tuner = tuner
        super(GetTunerInfo, self).__init__(host, clientId)

    def _getAction(self):
        """ This action is used to get tuner info from tv-set. """
        return "GetTunerInfo"

    def _fillSoapBody(self, doc):
        """ Fill xml body for GetSystemInfo soap action. """
        gti_tag = self._addCallerIds(doc,
                                     doc.createElement("urn:GetTunerInfo"))
        tuner_tag = doc.createElement("urn:tuner")
        txt = doc.createTextNode(str(self._tuner))
        tuner_tag.appendChild(txt)
        gti_tag.appendChild(tuner_tag)
        return gti_tag

    def _parseResponse(self, data):
        """ Return dictionary in the form {'info_name':'info_value',...}. """
        info_dict = {}
        doc = dom.parseString(data)
        tags = doc.getElementsByTagName("m:GetTunerInfoResponse")[0].childNodes
        for tag in tags:
            if tag.nodeType == tag.ELEMENT_NODE:
                if tag.tagName == "m:fcid":
                    continue
                elif tag.tagName == "m:ClientId":
                    continue
                else:
                    if tag.firstChild != None:
                        key_name = tag.tagName.split(':')[1]
                        info_dict[key_name] = tag.firstChild.nodeValue
        return info_dict

class SetMainVolume(FactoryInterfaceRequest):
    """ set sound volume on tv-set via Factory interface. """

    def __init__(self, host, clientId, volume=0):
        """ Overridden from base since we need exception uuid parameter. """
        self._volume = volume
        super(SetMainVolume, self).__init__(host, clientId)

    def _getAction(self):
        """ This action is used to set main volume from tv-set. """
        return "ControlSound"

    def _fillSoapBody(self, doc):
        """ Fill xml body for Con trolSound soap action. """
        gti_tag = self._addCallerIds(doc,
                                     doc.createElement("urn:ControlSound"))
        command_tag = doc.createElement("urn:Command")
        txt = doc.createTextNode('setVolume MAIN ' + str(self._volume))
        command_tag.appendChild(txt)
        gti_tag.appendChild(command_tag)
        return gti_tag

    def _parseResponse(self, data):
        """ Return dictionary in the form {'info_name':'info_value',...}. """
        info_dict = {}
        doc = dom.parseString(data)
        tags = doc.getElementsByTagName("m:ControlSoundResponse")[0].childNodes
        for tag in tags:
            if tag.nodeType == tag.ELEMENT_NODE:
                if tag.tagName == "m:fcid":
                    continue
                elif tag.tagName == "m:ClientId":
                    continue
                else:
                    if tag.firstChild != None:
                        key_name = tag.tagName.split(':')[1]
                        info_dict[key_name] = tag.firstChild.nodeValue
        return info_dict

class GetExceptionList(FactoryInterfaceRequest):
    """ Request to get exception list from tv-set via Factory interface. """

    def _getAction(self):
        """ This action is used to retrieve exception list from tv-set. """
        return "GetExceptionList"

    def _fillSoapBody(self, doc):
        """ Fill xml body for GetExceptionList soap action. """
        gel_tag = self._addCallerIds(doc,
                                     doc.createElement("urn:GetExceptionList"))
        # Exeption list view
        xlv_tag = doc.createElement("urn:ExceptionListView")
        def_tag = doc.createTextNode("default")
        xlv_tag.appendChild(def_tag)
        gel_tag.appendChild(xlv_tag)
        # Query parameters: document, parent_tag, startIndex=1, maxItems=300
        self._addQueryParameters(doc, gel_tag)
        return gel_tag

    def _parseResponse(self, data):
        """ Return list of exception uuids. """
        exc_list = []
        doc = dom.parseString(data)
        exc_tags = doc.getElementsByTagName("m:ExceptionItemReference")
        for exc_tag in exc_tags:
            uuid = exc_tag.getAttributeNode("ExceptionItemUuid").nodeValue
            exc_list.append(uuid)
        return exc_list

class GetExceptionItem(FactoryInterfaceRequest):
    """ Request to get certain exception item from tv-set. """

    def __init__(self, host, clientId, itemReference):
        """ Overridden from base since we need exception uuid parameter. """
        self._excUuid = itemReference
        super(GetExceptionItem, self).__init__(host, clientId)

    def _getAction(self):
        """ This action is used to retrieve exception item from tv-set. """
        return "GetExceptionItem"

    def _fillSoapBody(self, doc):
        """ Fill xml body for GetExceptionItem soap action. """
        gei_tag = self._addCallerIds(doc,
                                     doc.createElement("urn:GetExceptionItem"))
        # ExceptionItemReference
        xir_tag = doc.createElement("urn:ExceptionItemReference")
        xir_tag.setAttribute('ExceptionItemUuid', self._excUuid)
        gei_tag.appendChild(xir_tag)
        return gei_tag

    def _parseResponse(self, data):
        """ Return exception string. """
        doc = dom.parseString(data)
        exc = doc.getElementsByTagName("m:ExceptionInfo")
        return exc[0].firstChild.nodeValue

class DeleteExceptionItems(FactoryInterfaceRequest):
    """ Request to delete exceptions on tv-set. """

    def _getAction(self):
        """ This action is used to delete exceptions on tv-set. """
        return "DeleteExceptionItems"

    def _fillSoapBody(self, doc):
        """ Fill xml body for DeleteExceptionItems soap action. """
        dei_tag = self._addCallerIds(doc,
                                     doc.createElement(
                                         "urn:DeleteExceptionItems"))
        # Query parameters: document, parent_tag, startIndex=1, maxItems=300
        self._addQueryParameters(doc, dei_tag)
        return dei_tag

    def _parseResponse(self, data):
        """ Return error code as string. """
        doc = dom.parseString(data)
        ec = doc.getElementsByTagName("m:ErrorCode")
        return ec[0].firstChild.nodeValue

class FactoryInterfaceCommandRequest(FactoryInterfaceRequest):
    """ Base class for requests that need a command
    as param and parse result tag.
    """

    def __init__(self, host, clientId, command):
        """ Overridden from base since we need command parameter. """
        self._cmd = command
        super(FactoryInterfaceCommandRequest, self).__init__(host, clientId)

    def _addCommand(self, doc, parent_tag, cmd):
        """ Helper method to add a Command tag to a request. """
        cmd_tag = doc.createElement("urn:Command")
        cmd_txt = doc.createTextNode(cmd)
        cmd_tag.appendChild(cmd_txt)
        parent_tag.appendChild(cmd_tag)
        return parent_tag

    def _parseResponse(self, data):
        """ Return result message. """
        doc = dom.parseString(data)
        result_tags = doc.getElementsByTagName("m:result")
        return result_tags[0].firstChild.nodeValue

class ControlDebug(FactoryInterfaceCommandRequest):
    """ Request to change debug level of certain module on tv-set. """

    def _getAction(self):
        """ This action is used to control debug level on tv-set. """
        return "ControlDebug"

    def _fillSoapBody(self, doc):
        """ Fill xml body for ControlDebug soap action. """
        cd_tag = self._addCallerIds(doc, doc.createElement("urn:ControlDebug"))
        final_tag = self._addCommand(doc, cd_tag, self._cmd)
        return final_tag

class Loshell(FactoryInterfaceCommandRequest):
    """ Request to send a Loshell command to tv-set. """

    def _getAction(self):
        """ This action is used to send a Loshell command to tv-set. """
        return "Loshell"

    def _fillSoapBody(self, doc):
        """ Fill xml body for Loshell soap action. """
        ls_tag = self._addCallerIds(doc, doc.createElement("urn:Loshell"))
        final_tag = self._addCommand(doc, ls_tag, self._cmd)
        return final_tag

class FactoryInterfaceNetloggingRequest(FactoryInterfaceCommandRequest):
    """ Base class for factory interface netlogging requests. """

    def _addServerIP(self, doc, parent_tag, serverIP):
        """ Helper method to add ServerIP tag. """
        ip_tag = doc.createElement("urn:ServerIP")
        ip_txt = doc.createTextNode(self._cmd)
        ip_tag.appendChild(ip_txt)
        parent_tag.appendChild(ip_tag)
        return parent_tag

    def _parseResponse(self, data):
        """ Return error code as string. """
        doc = dom.parseString(data)
        ec = doc.getElementsByTagName("m:ErrorCode")
        return ec[0].firstChild.nodeValue

class DisableNetlogging(FactoryInterfaceNetloggingRequest):
    """ Request to disable netlogging, self._cmd is used for IP. """

    def _getAction(self):
        """ This action is used to disable netlogging on tv-set. """
        return "DisableNetlogging"

    def _fillSoapBody(self, doc):
        """ Fill xml body for DisableNetlogging soap action. """
        dn_tag = self._addCallerIds(doc,
                                    doc.createElement("urn:DisableNetlogging"))
        final_tag = self._addServerIP(doc, dn_tag, self._cmd)
        return final_tag

class EnableNetlogging(FactoryInterfaceNetloggingRequest):
    """ Request to enable netlogging, self._cmd is used for IP. """

    def _getAction(self):
        """ This action is used to enable netlogging on tv-set. """
        return "EnableNetlogging"

    def _fillSoapBody(self, doc):
        """ Fill xml body for EnableNetlogging soap action. """
        en_tag = self._addCallerIds(doc,
                                    doc.createElement("urn:EnableNetlogging"))
        final_tag = self._addServerIP(doc, en_tag, self._cmd)
        return final_tag

class GetSyslog(FactoryInterfaceCommandRequest):
    """ Request to obtain syslog via factory interface. """

    def _getAction(self):
        """ This action is used to obtain syslog from tv. """
        return "GetSyslog"

    def _fillSoapBody(self, doc):
        """ Fill xml body for GetSyslog soap action. """
        gs_tag = self._addCallerIds(doc, doc.createElement("urn:GetSyslog"))
        final_tag = self._addCommand(doc, gs_tag, self._cmd)
        return final_tag

    def _parseResponse(self, data):
        """ Overridden from base to check m:data tag. """
        doc = dom.parseString(data)
        data_tags = doc.getElementsByTagName("m:data")
        return data_tags[0].firstChild.nodeValue

class GetEaromSize(FactoryInterfaceRequest):
    """ Request to receive size of EAROM. """

    def _getAction(self):
        """ This action is used to retrieve size of earom. """
        return "GetEaromSize"

    def _fillSoapBody(self, doc):
        """ Fill xml body for GetEaromSize with device tag. """
        ges_tag = self._addCallerIds(doc,
                                     doc.createElement("urn:GetEaromSize"))
        device_tag = doc.createElement("urn:device")
        device_txt = doc.createTextNode("0")
        device_tag.appendChild(device_txt)
        ges_tag.appendChild(device_tag)
        return ges_tag

    def _parseResponse(self, data):
        """ Return earom size as int or string in error case. """
        doc = dom.parseString(data)
        es = doc.getElementsByTagName("m:result")
        txt = es[0].firstChild.nodeValue
        # Parse for hex number and capture it
        match = re.match("ok \(([0-9A-F]+)\)", txt)
        if match:
            return int(match.group(1),base=16)
        else:
            return txt

class FactoryInterfaceEaromRequest(FactoryInterfaceRequest):
    """ Base class for earom requests with address offset. """

    def __init__(self, host, clientId, offset):
        """ Overridden from base since we need offset hex string parameter. """
        self._offset = offset
        super(FactoryInterfaceEaromRequest, self).__init__(host, clientId)

    def _createEaromBody(self, doc, mainTagName, customTagName, customTxt):
        e_tag = self._addCallerIds(doc, doc.createElement(mainTagName))
        final_tag = self._addOffset(doc, e_tag, self._offset)
        custom_tag = doc.createElement(customTagName)
        custom_txt = doc.createTextNode(customTxt)
        custom_tag.appendChild(custom_txt)
        final_tag.appendChild(custom_tag)
        return final_tag

    def _addOffset(self, doc, parent_tag, off):
        """ Helper method to add a Offset tag to a request. """
        off_tag = doc.createElement("urn:offset")
        off_txt = doc.createTextNode(off)
        off_tag.appendChild(off_txt)
        parent_tag.appendChild(off_tag)
        return parent_tag

class ReadEarom(FactoryInterfaceEaromRequest):
    """ Request to read (parts of) EAROM. """

    def __init__(self, host, clientId, offset="0001", size="0001"):
        """ Overridden from base since we need size parameter.
            If offset and size are omitted: Read default chunk size from start.
        """
        self._size = size
        super(ReadEarom, self).__init__(host, clientId, offset)

    def _getAction(self):
        """ This action is used to read from earom. """
        return "ReadEarom"

    def _fillSoapBody(self, doc):
        """ Fill xml body for ReadEarom soap action with offset and number
            of bytes to read. """
        return self._createEaromBody(doc, "urn:ReadEarom", "urn:size",
                                     self._size)

    def _parseResponse(self, data):
        """ Return earom data base64 encoded or string in error case. """
        doc = dom.parseString(data)
        es = doc.getElementsByTagName("m:result")
        txt = es[0].firstChild.nodeValue
        return txt

class WriteEarom(FactoryInterfaceEaromRequest):
    """ Request to write (parts of) EAROM. """

    def __init__(self, host, clientId, offset="0000", data=""):
        """ Overridden from base, since we need data parameter.
            data: data to be written at offset as base64 encoded string. """
        self._data = data
        super(WriteEarom, self).__init__(host, clientId, offset)

    def _getAction(self):
        """ This action is used to write earom. """
        return "WriteEarom"

    def _fillSoapBody(self, doc):
        """ Fill xml body for WriteEarom with offset and data to be written.
        """
        return self._createEaromBody(doc, "urn:WriteEarom", "urn:data",
                                     self._data)

    def _parseResponse(self, data):
        """ Parse for write result. """
        doc = dom.parseString(data)
        es = doc.getElementsByTagName("m:result")
        txt = es[0].firstChild.nodeValue
        return txt

class ResetFactoryDefaults(FactoryInterfaceRequest):
    """ Request to reset tv-set to factory defaults. """

    def __init__(self, host, clientId, system):
        """ Overridden from base, since we need system parameter.
            system can either be 'varlocal' or 'mntconfig'. """
        self._system = system
        super(ResetFactoryDefaults, self).__init__(host, clientId)

    def _getAction(self):
        """ This action is used to reset to factory defaults. """
        return "ResetFactoryDefaults"

    def _fillSoapBody(self, doc):
        """ Fill xml body for ResetFactoryDefaults with system tag. """
        rfd_tag = self._addCallerIds(doc,
                                     doc.createElement(
                                         "urn:ResetFactoryDefaults"))
        sys_tag = doc.createElement("urn:system")
        sys_txt = doc.createTextNode(self._system)
        sys_tag.appendChild(sys_txt)
        rfd_tag.appendChild(sys_tag)
        return rfd_tag

    def _parseResponse(self, data):
        """ Parse for result of reset operation. """
        doc = dom.parseString(data)
        es = doc.getElementsByTagName("m:result")
        txt = es[0].firstChild.nodeValue
        return txt

class FactoryInterfaceLoregRequest(FactoryInterfaceRequest):
    """ Base class for loreg requests. """

    def __init__(self, host, clientId, key):
        """ Overridden from base, since we need key param. """
        self._key = key
        super(FactoryInterfaceLoregRequest, self).__init__(host, clientId)

    def _addKey(self, doc, parent_tag, key):
        """ Helper method to add a Offset tag to a request. """
        key_tag = doc.createElement("urn:Key")
        key_txt = doc.createTextNode(key)
        key_tag.appendChild(key_txt)
        parent_tag.appendChild(key_tag)
        return parent_tag

class deleteLoregKey(FactoryInterfaceLoregRequest):
    """ Delete a certain loreg key / value pair. """

    def _getAction(self):
        """ This action is used to delete a certain loreg key / value pair. """
        return "deleteLoregKey"

    def _fillSoapBody(self, doc):
        """ Fill xml body for deleteLoregKey with key tag. """
        dlk_tag = self._addCallerIds(doc,
                                     doc.createElement("urn:deleteLoregKey"))
        final_tag = self._addKey(doc, dlk_tag, self._key)
        return final_tag

    def _parseResponse(self, data):
        """ Parse for result of delete operation. """
        doc = dom.parseString(data)
        es = doc.getElementsByTagName("m:result")
        txt = es[0].firstChild.nodeValue
        return txt

class setLoregKey(FactoryInterfaceLoregRequest):
    """ Set a certain loreg key / value pair. """

    def __init__(self, host, clientId, key, value):
        """ Overridden from base, since we need value param. """
        self._value = value
        super(setLoregKey, self).__init__(host, clientId, key)

    def _getAction(self):
        """ This action is used to set a certain loreg key / value pair. """
        return "setLoregKey"

    def _fillSoapBody(self, doc):
        """ Fill xml body for setLoregKey with key and value tag. """
        dlk_tag = self._addCallerIds(doc, doc.createElement("urn:setLoregKey"))
        final_tag = self._addKey(doc, dlk_tag, self._key)
        value_tag = doc.createElement("urn:Value")
        value_txt = doc.createTextNode(self._value)
        value_tag.appendChild(value_txt)
        final_tag.appendChild(value_tag)
        return final_tag

    def _parseResponse(self, data):
        """ Parse for result of set operation. """
        doc = dom.parseString(data)
        es = doc.getElementsByTagName("m:result")
        txt = es[0].firstChild.nodeValue
        return txt

class getLoregKey(FactoryInterfaceLoregRequest):
    """ Get the value of a certain loreg key. """

    def _getAction(self):
        """ This action is used to get the value of a certain loreg key. """
        return "getLoregKey"

    def _fillSoapBody(self, doc):
        """ Fill xml body for getLoregKey with key tag. """
        dlk_tag = self._addCallerIds(doc, doc.createElement("urn:getLoregKey"))
        final_tag = self._addKey(doc, dlk_tag, self._key)
        return final_tag

    def _parseResponse(self, data):
        """ Parse for result of get operation. """
        doc = dom.parseString(data)
        es = doc.getElementsByTagName("m:result")
        return int(re.search('(\d+)', es[0].firstChild.nodeValue).group(1))

class ControlServicelist(FactoryInterfaceCommandRequest):
    """ Control the servicelist. """

    def _getAction(self):
        """ This action is used to control the servicelist. """
        return "ControlServicelist"

    def _fillSoapBody(self, doc):
        """ Fill xml body for ControlServicelist with cmd tag. """
        cs_tag = self._addCallerIds(doc,
                                    doc.createElement(
                                        "urn:ControlServicelist"))
        final_tag = self._addCommand(doc, cs_tag, self._cmd)
        return final_tag

    def _parseResponse(self, data):
        return self._parseAndReturnResult(data)

class EPGRemoveEvents(FactoryInterfaceRequest):
    """ Delete epg events. """

    def _getAction(self):
        """ This action is used to reset EPG database. """
        return "EPGRemoveEvents"

    def _fillSoapBody(self, doc):
        """ Fill xml body for EPGRemoveEvents. """
        ere_tag = self._addCallerIds(doc,
                                     doc.createElement("urn:EPGRemoveEvents"))
        return ere_tag

    def _parseResponse(self, data):
        """ Parse for result of this operation. """
        # Result starts with uppercase R here !!!
        doc = dom.parseString(data)
        es = doc.getElementsByTagName("m:Result")
        txt = es[0].firstChild.nodeValue
        return txt

class GetOperationTime(FactoryInterfaceRequest):
    """ Get operation time. """

    def _getAction(self):
        """ This action is used to retrieve operation time of tv-set. """
        return "GetOperationTime"

    def _fillSoapBody(self, doc):
        """ Fill xml body for GetOperationTime with Counter tag. """
        got_tag = self._addCallerIds(doc,
                                     doc.createElement("urn:GetOperationTime"))
        counter_tag = doc.createElement("urn:Counter")
        counter_txt = doc.createTextNode("ALL")
        counter_tag.appendChild(counter_txt)
        got_tag.appendChild(counter_tag)
        return got_tag

    def _parseResponse(self, data):
        """ Parse for result / data of this operation. """
        doc = dom.parseString(data)
        es = doc.getElementsByTagName("m:data")
        txt = es[0].firstChild.nodeValue
        return txt

class SetMediaPath(FactoryInterfaceRequest):
    """ Set a certain media path / uri via factory interface. """

    def __init__(self, host, clientId, uri, terminal="TERMINAL_ID0",
                 type="TERMINAL_ALL", flags="",
                 vampParams="outputMode=auto_yc_cvbs"):
        """ Overridden from base, since we need params. """
        self._uri = uri
        self._terminal = terminal
        self._type = type
        self._flags = flags
        self._vampParams = vampParams
        super(SetMediaPath, self).__init__(host, clientId)

    def _getAction(self):
        """ This action is used to set uri. """
        return "SetMediaPath"

    def _fillSoapBody(self, doc):
        """ Fill xml body for SetMediaPath tag. """
        smp_tag = self._addCallerIds(doc,
                                     doc.createElement("urn:SetMediaPath"))
        smp_tag.appendChild(self._addTagWithText(doc, "urn:terminal",
                                                 self._terminal))
        smp_tag.appendChild(self._addTagWithText(doc, "urn:type", self._type))
        smp_tag.appendChild(self._addTagWithText(doc, "urn:flags",
                                                 self._flags))
        smp_tag.appendChild(self._addTagWithText(doc, "urn:uri", self._uri))
        smp_tag.appendChild(self._addTagWithText(doc, "urn:vampParams",
                                                 self._vampParams))
        return smp_tag

    def _parseResponse(self, data):
        """ Return result tag of this operation. """
        return self._parseAndReturnResult(data)

class GetFuseInfo(FactoryInterfaceRequest):
    """ Get info about fuses needed for CI+. """

    def _getAction(self):
        """ This action is used to get info about fuses. """
        return "GetFuseInfo"

    def _fillSoapBody(self, doc):
        """ Fill xml body for GetFuseInfo. """
        gfi_tag = self._addCallerIds(doc, doc.createElement("urn:GetFuseInfo"))
        gfi_tag.appendChild(self._addTagWithText(doc, "urn:aux", "5a"))
        return gfi_tag

    def _parseResponse(self, data):
        """ Parse for result of this operation. """
        doc = dom.parseString(data)
        txt = doc.toprettyxml()
        return txt

class GetWakeupReasons(FactoryInterfaceRequest):
    """ Get wake-up reason. """

    def _getAction(self):
        """ This action is used to retrieve operation time of tv-set. """
        return "ControlPower"

    def _fillSoapBody(self, doc):
        """ Fill xml body for GetOperationTime with Counter tag. """
        got_tag = self._addCallerIds(doc,
                                     doc.createElement("urn:ControlPower"))
        counter_tag = doc.createElement("urn:Command")
        counter_txt = doc.createTextNode("getWakeupReasons")
        counter_tag.appendChild(counter_txt)
        got_tag.appendChild(counter_tag)
        return got_tag

    def _parseResponse(self, data):
        """ Parse for result / data of this operation. """
        doc = dom.parseString(data)
        es = doc.getElementsByTagName("m:result")
        txt = es[0].firstChild.nodeValue
        return txt
        
class DeleteCoredumpItems(FactoryInterfaceRequest):
    """ Request to delete core dumps on tv-set. """

    def _getAction(self):
        """ This action is used to delete exceptions on tv-set. """
        return "DeleteCoredumpItems"

    def _fillSoapBody(self, doc):
        """ Fill xml body for DeleteCoredumpItems soap action. """
        dei_tag = self._addCallerIds(doc,
                                     doc.createElement(
                                         "urn:DeleteCoredumpItems"))
        # Query parameters: document, parent_tag, startIndex=1, maxItems=300
        self._addQueryParameters(doc, dei_tag)
        return dei_tag

    def _parseResponse(self, data):
        """ Return error code as string. """
        doc = dom.parseString(data)
        ec = doc.getElementsByTagName("m:ErrorCode")
        return ec[0].firstChild.nodeValue
        
class GetCoredumpList(FactoryInterfaceRequest):
    """ Request to get core dumps list from tv-set via Factory interface. """

    def _getAction(self):
        """ This action is used to retrieve exception list from tv-set. """
        return "GetCoredumpList"

    def _fillSoapBody(self, doc):
        """ Fill xml body for CoredumpList soap action. """
        gel_tag = self._addCallerIds(doc,
                                     doc.createElement("urn:GetCoredumpList"))
        # Exeption list view
        xlv_tag = doc.createElement("urn:CoredumpListView")
        def_tag = doc.createTextNode("default")
        xlv_tag.appendChild(def_tag)
        gel_tag.appendChild(xlv_tag)
        # Query parameters: document, parent_tag, startIndex=1, maxItems=300
        self._addQueryParameters(doc, gel_tag)
        return gel_tag

    def _parseResponse(self, data):
        """ Return list of exception uuids. """
        exc_list = []
        doc = dom.parseString(data)
        exc_tags = doc.getElementsByTagName("m:CoredumpItemReference")
        for exc_tag in exc_tags:
            uuid = exc_tag.getAttributeNode("CoredumpItemUuid").nodeValue
            exc_list.append(uuid)
        return exc_list

class GetCoredumpItem(FactoryInterfaceRequest):
    """ Request to get certain core dump item from tv-set. """

    def __init__(self, host, clientId, itemReference):
        """ Overridden from base since we need core dump uuid parameter. """
        self._excUuid = "dvbcrash_" + itemReference + ".core"
        super(GetCoredumpItem, self).__init__(host, clientId)

    def _getAction(self):
        """ This action is used to retrieve core item from tv-set. """
        return "GetCoredumpItem"

    def _fillSoapBody(self, doc):
        """ Fill xml body for GetCoredumpItem soap action. """
        gei_tag = self._addCallerIds(doc,
                                     doc.createElement("urn:GetCoredumpItem"))
        # CoredumpItemReference
        xir_tag = doc.createElement("urn:CoredumpItemReference")
        xir_tag.setAttribute('CoredumpItemUuid', self._excUuid)
        gei_tag.appendChild(xir_tag)
        return gei_tag

    def _parseResponse(self, data):
        """ Return exception string. """
        doc = dom.parseString(data)
        # was m:CoredumpInfo
        exc = doc.getElementsByTagName("m:CoredumpItemUUID")
        return exc[0].firstChild.nodeValue
