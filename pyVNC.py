#!/usr/bin/env python
from threading import Thread
from twisted.python import log
from twisted.internet import reactor
import pygame

import constants
import rfb
from GUI import GUI
from RFBToGUI import RFBToGUI, RFBToGUIeightbits
import argparse
import time


class VNCFactory(rfb.RFBFactory):
    """A factory for remote frame buffer connections."""

    def __init__(self, remoteframebuffer, depth, fast, *args, **kwargs):
        rfb.RFBFactory.__init__(self, *args, **kwargs)
        self.remoteframebuffer = remoteframebuffer
        if depth == 32:
            self.protocol = RFBToGUI
        elif depth == 8:
            self.protocol = RFBToGUIeightbits
        else:
            raise ValueError("color depth not supported")

        if fast:
            self.encodings = [
                rfb.COPY_RECTANGLE_ENCODING,
                rfb.RAW_ENCODING,
            ]
        else:
            self.encodings = [
                rfb.COPY_RECTANGLE_ENCODING,
                rfb.HEXTILE_ENCODING,
                rfb.CORRE_ENCODING,
                rfb.RRE_ENCODING,
                rfb.RAW_ENCODING,
            ]

    def buildProtocol(self, addr):
        display = addr.port - 5900
        pygame.display.set_caption('pyVNC on %s:%s' % (addr.host, display))
        return rfb.RFBFactory.buildProtocol(self, addr)

    def clientConnectionLost(self, connector, reason):
        log.msg("connection lost: %r" % reason.getErrorMessage())
        #reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        log.msg("cannot connect to server: %r\n" % reason.getErrorMessage())
        reactor.stop()


class VNCClient(Thread):
    def __init__(self, host="127.0.0.1", password=None, port=5902, depth=32, fast=False, shared=True):
        Thread.__init__(self)
        pygame.init()
        self.screen = GUI()
        self.host = host
        self.password = password
        self.port = port
        self.depth = depth
        self.fast = fast
        self.shared = shared

    def send_key(self, key, duration=0.001):
        if key in constants.MODIFIERS:
            self.screen.protocol.key_event(constants.MODIFIERS[key], down=1)
        elif key in constants.KEYMAPPINGS:
            self.screen.protocol.key_event(constants.KEYMAPPINGS[key], down=1)
        elif type(key) == str:
            print(ord(key))
            self.screen.protocol.key_event(ord(key))

        time.sleep(.001)

        if key in constants.MODIFIERS:
            self.screen.protocol.key_event(constants.MODIFIERS[key], down=0)
        elif key in constants.KEYMAPPINGS:
            self.screen.protocol.key_event(constants.KEYMAPPINGS[key], down=0)

    def send_mouse(self, event="Left", position=(0, 0)):
        # Left 1, Middle 2, Right 3,
        button_id = None
        if event is "Left":
            button_id = 1
        elif event is "Middle":
            button_id = 2
        elif event is "Right":
            button_id = 4

        self.screen.protocol.pointer_event(position[0], position[1], 0)
        self.screen.protocol.pointer_event(position[0], position[1], button_id)

    def run_block(self):
        reactor.connectTCP(
            self.host,  # remote hostname
            self.port,  # TCP port number
            VNCFactory(
                self.screen,  # the application/display
                self.depth,  # color depth
                self.fast,  # if a fast connection is used
                self.password,  # password or none
                int(self.shared),  # shared session flag
            )
        )

        # run the application
        reactor.callLater(0.1, self.screen.loop)
        reactor.run(installSignalHandlers=False)

    def run(self):
        self.run_block()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1", type=str, help="Hostname of the VNC Server")
    parser.add_argument("--port", default="5902", type=int, help="VNC Server Port")
    parser.add_argument("--password", default=None, type=str, help="Password of the VNC Server")
    parser.add_argument("--depth", default=32, type=int, help="Color Depth")
    parser.add_argument("--fast", default=False, type=bool,  help="Fast encoding")
    parser.add_argument("--shared", default=False, type=bool,  help="Shared VNC Instance")
    args = parser.parse_args()

    vnc = VNCClient(host=args.host,
                    port=args.port,
                    password=args.password,
                    depth=args.depth,
                    fast=args.fast,
                    shared=args.shared)
    vnc.run()


