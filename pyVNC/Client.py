from threading import Thread
from twisted.internet import reactor
import pygame
import time
from pyVNC import constants
from pyVNC.Buffer import DisplayBuffer, ArrayBuffer
from pyVNC.VNCFactory import VNCFactory


class Client(Thread):
    def __init__(self, host="127.0.0.1", password=None, port=5902, depth=32, fast=False, shared=True, gui=False, gui_with_array=False):
        Thread.__init__(self)
        pygame.init()
        self.has_gui = gui
        self.screen = DisplayBuffer(gui_with_array) if gui else ArrayBuffer()
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
