from twisted.internet import reactor
from constants import *


class GUI:

    def __init__(self):
        pygame.display.set_caption('pyVNC')
        pygame.mouse.set_cursor(*POINTER)
        pygame.key.set_repeat(500, 30)

        # Variable Definitions
        self.size = (400, 400)
        self.clock = pygame.time.Clock()
        self.alive = 1
        self.loopcounter = 0
        self.buttons = 0
        self.protocol = None
        self.buffer = None

        self.set_rfb_size(*self.size)

    def set_rfb_size(self, width, height, depth=32):
        """change screen size"""
        self.width, self.height = width, height
        self.area = Rect(0, 0, width, height)
        winstyle = 0  # |FULLSCREEN
        if depth == 32:
            self.screen = pygame.display.set_mode(self.area.size, winstyle, 32)
        elif depth == 8:
            self.screen = pygame.display.set_mode(self.area.size, winstyle, 8)
        else:
            raise ValueError("color depth not supported")
        self.background = pygame.Surface((self.width, self.height), depth)
        self.background.fill(0)  # black

    def set_protocol(self, protocol):
        """attach a protocol instance to post the events to"""
        self.protocol = protocol

    def check_events(self):
        """process events from the queue"""
        seen_events = 0
        for e in pygame.event.get():
            seen_events = 1

            if e.type == QUIT:
                self.alive = 0
                reactor.stop()

            if self.protocol is not None:

                if e.type == KEYDOWN:
                    if e.key in MODIFIERS:
                        self.protocol.key_event(MODIFIERS[e.key], down=1)
                    elif e.key in KEYMAPPINGS:
                        self.protocol.key_event(KEYMAPPINGS[e.key], down=1)
                    elif e.unicode:
                        self.protocol.key_event(ord(e.unicode))
                    else:
                        print("warning: unknown key %r" % (e))

                elif e.type == KEYUP:
                    if e.key in MODIFIERS:
                        self.protocol.key_event(MODIFIERS[e.key], down=0)
                    elif e.key in KEYMAPPINGS:
                        self.protocol.key_event(KEYMAPPINGS[e.key], down=0)
                elif e.type == MOUSEMOTION:
                    self.buttons = e.buttons[0] and 1
                    self.buttons |= e.buttons[1] and 2
                    self.buttons |= e.buttons[2] and 4
                    self.protocol.pointer_event(e.pos[0], e.pos[1], self.buttons)
                elif e.type == MOUSEBUTTONUP:
                    if e.button == 1: self.buttons &= ~1
                    if e.button == 2: self.buttons &= ~2
                    if e.button == 3: self.buttons &= ~4
                    if e.button == 4: self.buttons &= ~8
                    if e.button == 5: self.buttons &= ~16
                    self.protocol.pointer_event(e.pos[0], e.pos[1], self.buttons)

                elif e.type == MOUSEBUTTONDOWN:
                    if e.button == 1: self.buttons |= 1
                    if e.button == 2: self.buttons |= 2
                    if e.button == 3: self.buttons |= 4
                    if e.button == 4: self.buttons |= 8
                    if e.button == 5: self.buttons |= 16
                    self.protocol.pointer_event(e.pos[0], e.pos[1], self.buttons)

            return not seen_events
        return not seen_events

    def loop(self, dum=None):
        """gui 'mainloop', it is called repeated by twisteds mainloop
           by using callLater"""
        # ~ self.clock.tick()
        no_work = self.check_events()
        if self.alive:
            self.buffer = pygame.surfarray.array3d(self.screen).swapaxes(0, 1)
            reactor.callLater(no_work and 0.020, self.loop)

