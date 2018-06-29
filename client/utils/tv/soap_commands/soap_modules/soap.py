import re
import xml.dom.minidom as dom
from xml.parsers.expat import ExpatError
import http.client, urllib.parse

HTTP_TIMEOUT = 10

class SoapRequest(object):
    """ Base class for SOAP requests. """

    SOAPENV_SCHEMA = "http://schemas.xmlsoap.org/soap/envelope/"

    def __init__(self, urn):
        """ Create a SOAP request with envelope, header and body. """
        self.__doc = dom.Document()
        # Save urn for later use
        self._urn = urn
        # Envelope
        tag_envelope = self.__doc.createElement("soapenv:Envelope")
        tag_envelope.setAttribute("xmlns:soapenv", self.SOAPENV_SCHEMA)
        tag_envelope.setAttribute("xmlns:urn", urn)
        self.__doc.appendChild(tag_envelope)
        # Header
        tag_header = self.__doc.createElement("soapenv:Header")
        tag_envelope.appendChild(tag_header)
        # Body
        self.__tag_body = self.__doc.createElement("soapenv:Body")
        tag_envelope.appendChild(self.__tag_body)
        # Fill body
        self.__tag_body.appendChild(self._fillSoapBody(self.__doc))

    @property
    def xml(self):
        """ Return xml of soap request. """
        return self.__doc.toprettyxml()

    def _fillSoapBody(self, doc):
        """ This needs to be overridden in derived class to provide
            meaningful soap body. """
        tag = doc.createElement("urn:gnampf")
        return tag

    def getResponse(self):
        """ The public entry point to get soap response. """
        raise NotImplementedError("Please implement in derived class.")

    def __repr__(self):
        """ Return string representation of SoapRequest object. """
        return self.xml

class HttpSoapRequest(SoapRequest):
    """ SOAP request that uses HTTP protocol. """

    def __init__(self, host, port, url, urn):
        """ Create a soap request via HTTP. """
        super(HttpSoapRequest, self).__init__(urn)
        self.__host = host
        self.__port = port
        self.__url = url

    def _getAction(self):
        """ Return the soap action as string. """
        raise NotImplementedError(
            "Please provide soap action in derived class.")

    def _parseResponse(self, data):
        """ Parse the xml data returned by request. """
        raise NotImplementedError("Please provide parsing in derived class.")

    def getResponse(self):
        """ Get soap response via HTTP. """
        # HTTP headers
        headers = { "Content-type": "text/xml; charset=utf-8",
                    "SOAPAction": "\"" + self._urn + "#" + self._getAction()
                    + "\""}
        conn = http.client.HTTPConnection(self.__host, self.__port,
                                          timeout=HTTP_TIMEOUT)
        conn.request("POST", self.__url, self.xml, headers)
        response = conn.getresponse()
        data = response.read()

        conn.close()
        # Parse response
        d = ""
        try:
            d = self._parseResponse(data)
        except ExpatError:
            raise
        return d

    def __repr__(self):
        return self.__host + ':' + str(self.__port) + \
            self.__url + "\n" + self.xml
