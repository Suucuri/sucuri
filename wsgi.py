#!/usr/bin/env python
# noinspection GrazieInspection
""" Web server runner.

Classes neste módulo:
    - :py:class:`DirectoryHandler` handle all routes from web.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>
.. codeauthor:: Craig Campbell <https://craig.is>

Changelog
---------
.. versionchanged::    24.03
   |br| Revert to enable serving index from root (07).

.. versionadded::    24.03
   |br| Initial server implementation (07).

|   **Open Source Notification:** This file is part of open source program **Pynoplia**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   # Copyright (c) 2018, Craig Campbell
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <https://is.gd/3Udt>`_.
|   `Labase <https://labase.github.io/>`_ - `NCE <https://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.
"""

import os
import tornado.web
from tornado import websocket
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.escape import xhtml_escape

# config options
define('port', default=8585, type=int, help='port to run web server on')
define('debug', default=True, help='start app in debug mode')
define('route_to_index', default=True, help='route all requests to index.html')
options.parse_command_line(final=True)

PORT = options.port
DEBUG = options.debug
ROUTE_TO_INDEX = options.route_to_index
PATH = '/'

cl = []


class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def _open(self):
        if self not in cl:
            cl.append(self)

    def _on_close(self):
        if self in cl:
            cl.remove(self)

    def open(self):
        print("WebSocket opened")
        self._open()

    def on_message(self, message):
        print("WebSocket message received", message)
        self.write_all(message)

    def on_close(self):
        print("WebSocket closed")
        self._on_close()

    def write_all(self, msg):
        print("WebSocket write all", cl, msg)
        [receiver.write_message(msg) for receiver in cl if receiver is not self]


class DirectoryHandler(tornado.web.StaticFileHandler):
    def validate_absolute_path(self, root, absolute_path):
        print(absolute_path, self.request.uri, os.path.isdir(absolute_path))
        if ROUTE_TO_INDEX and self.request.uri != '/' and '.' not in self.request.uri:
            uri = self.request.uri
            if self.request.uri.endswith('/'):
                uri = uri[:-1]

            absolute_path = absolute_path.replace(uri, '/index.html')

        if os.path.isdir(absolute_path):
            index = os.path.join(absolute_path, 'index.html')
            print("os.path.isfile(index)", index, absolute_path)
            if os.path.isfile(index):
                print("if os.path.isfile(index)", index, absolute_path)
                return index

            return absolute_path

        return super(DirectoryHandler, self).validate_absolute_path(root, absolute_path)

    def get_content_type(self):
        if self.absolute_path.endswith('.vtt'):
            return 'text/vtt'

        if self.absolute_path.endswith('.m3u8'):
            return 'application/vnd.apple.mpegurl'

        content_type = super(DirectoryHandler, self).get_content_type()

        # default to text/html
        if content_type == 'application/octet-stream':
            return 'text/html'

        return content_type

    @classmethod
    def get_content(cls, abspath, start=None, end=None):
        relative_path = abspath.replace(os.getcwd(), '') + '/'

        if os.path.isdir(abspath):
            html = ('<html><title>Directory listing for %s</title><body><h2>Directory listing for %s</h2><hr><ul>'
                    % (relative_path, relative_path))
            for filename in os.listdir(abspath):
                force_slash = ''
                full_path = filename
                if os.path.isdir(os.path.join(relative_path, filename)[1:]):
                    full_path = os.path.join(relative_path, filename)
                    force_slash = '/'

                html += '<li><a href="%s%s">%s%s</a>' % (
                    xhtml_escape(full_path), force_slash, xhtml_escape(filename), force_slash)

            return html + '</ul><hr>'

        return super(DirectoryHandler, cls).get_content(abspath, start=start, end=end)


settings = {
    'debug': DEBUG,
    'gzip': True,
    'static_handler_class': DirectoryHandler
}

application = tornado.web.Application([
    (r'/ws', SocketHandler),
    # (r'/index', DirectoryHandler, {'path': './'})
    (r'/(.*)', DirectoryHandler, {'path': './'})
], **settings)

if __name__ == "__main__":
    print("Listening on port %d..." % PORT)
    application.listen(PORT)
    IOLoop.instance().start()
