import traceback

import xml.dom.minidom as dom

from utils.tv.soap_commands import HttpSoapRequest


class GuiSoapInterfaceRequest(HttpSoapRequest):
    """ Base class for gui soap interface request. """

    def __init__(self, host):
        """ Create a gui soap interface request with defined settings. """
        super().__init__(host, 47110, "", "urn:GUI2012")

    def _buildQuery(self, doc, parentTag, headTag, bodyTag, tagValue):
        head_tag = doc.createElement(headTag)
        body_tag = doc.createElement(bodyTag)
        tag_value = doc.createTextNode(tagValue)
        body_tag.appendChild(tag_value)
        head_tag.appendChild(body_tag)

        return head_tag


class GetGuiStatus(GuiSoapInterfaceRequest):
    def __init__(self, host):
        super().__init__(host)

    def _getAction(self):
        return "GetStatus"

    def _fillSoapBody(self, doc):
        tag = self._buildQuery(doc, doc.getElementsByTagName("soapenv:Body"), "urn:GetStatus", "urn:aRequest", "GuiStatus")
        return tag

    def _parseResponse(self, data):
        doc = None
        try:
            doc = dom.parseString("".join(map(chr,[x for x in data if x is not 0xad])))
            tag = doc.getElementsByTagName('m:aResult')[0]
            return tag.firstChild.nodeValue
        except:
            traceback.print_exc()
            return "ERROR while parsing response"

class SendKey(GuiSoapInterfaceRequest):
    def __init__(self, host, keycode):
        self.keycode = keycode
        super().__init__(host)

    def _getAction(self):
        return "SendKey"

    def _fillSoapBody(self, doc):
        tag = self._buildQuery(doc, doc.getElementsByTagName("soapenv:Body"), "urn:SendKey", "urn:aKeyCode", self.keycode)
        return tag

    def _parseResponse(self, data):
        return ""
