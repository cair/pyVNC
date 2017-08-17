import pygame
from twisted.internet import reactor
from pyVNC.RFBToGUI import RFBToGUIeightbits, RFBToGUI
from pyVNC.rfb import *


class VNCFactory(RFBFactory):
    """A factory for remote frame buffer connections."""

    def __init__(self, buffer, depth, fast, *args, **kwargs):
        RFBFactory.__init__(self, *args, **kwargs)
        self.buffer = buffer
        if depth == 32:
            self.protocol = RFBToGUI
        elif depth == 8:
            self.protocol = RFBToGUIeightbits
        else:
            raise ValueError("color depth not supported")

        if fast:
            self.encodings = [
                COPY_RECTANGLE_ENCODING,
                RAW_ENCODING,
            ]
        else:
            self.encodings = [
                COPY_RECTANGLE_ENCODING,
                HEXTILE_ENCODING,
                CORRE_ENCODING,
                RRE_ENCODING,
                RAW_ENCODING,
            ]

    def buildProtocol(self, addr):
        display = addr.port - 5900
        pygame.display.set_caption('pyVNC on %s:%s' % (addr.host, display))

        return RFBFactory.buildProtocol(self, addr)

    def clientConnectionLost(self, connector, reason):
        log.msg("connection lost: %r" % reason.getErrorMessage())
        #reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        log.msg("cannot connect to server: %r\n" % reason.getErrorMessage())
        reactor.stop()