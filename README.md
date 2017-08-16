# pyVNC
pyVNC Client is a client library for interacting programatically (and physically) with a VNC session.
pyVNC Client that is built with
[Twisted-Python](https://twistedmatrix.com/trac/) and
[PyGame](http://www.pygame.org/).

The client supports the following encodings: `Hextile, CoRRE, RRE, RAW, CopyRect`

pyVNC is tested for `Python >= 3.5`

#Usage

## Example 1
```py
 vnc = VNCClient(host="127.0.0.1",
                 password=None, 
                 port=5902,
                 depth=32,
                 fast=False,
                 shared=True) # Default parameters
                 
 vnc.start()    # Starts the vnc client (Threaded)
 
 vnc.send_key("a") # Sends the key "a"
 vnc.send_mouse("Left", (200, 200)) # Left Clicks at x=200, y=200
 vnc.send_mouse("Right", (200, 200)) # Right Clicks at x=200, y=200
 vnc.get_screen() # Get a array representation of the screen shape: (?, ?, 3)
 vnc.join() # Exit
``` 

## Parameters
`pyVNC.py --host=127.0.0.1 --password=None --depth=32 --fast=False, shared=False`

# What is it good for?
pyVNC is excellent for automating tasks inside a VNC session.

# References:
- http://homepage.hispeed.ch/py430/python/
- http://code.google.com/p/vnc2flv/
- http://arkaitzj.wordpress.com/2011/11/12/vnc-in-your-browser-through-websockets-handled-by-gevent/
- http://sibson.github.io/vncdotool/
- http://www.python.org
- http://twistedmatrix.com/
- http://www.pygame.org
- http://www.realvnc.org

## Copyright Notice
Thanks to the original authors for providing an excellent implemenation of the VNC protocol in python.
This project would not have been possible with their work:
- (c) 2003 chris <cliechti@gmx.net>
- (c) 2009 techtonik <techtonik@gmail.com>

And pyVNC author:
- (c) 2017 Per-Arne Andersen <per@sysx.no>

Released under the MIT License.

You're free to use it for commercial and noncommercial
application, modify and redistribute it as long as the
copyright notices are intact. There are no warranties, not
even that it does what it says to do ;-)


## Changes
16.08.17 - Forked and reworked as a client library