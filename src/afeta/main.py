#!/usr/bin/env python
# noinspection GrazieInspection
"""Dynamic Web Document Builder.

Classes neste módulo:
    - :py:class:`Hub` communication hub.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    25.03
   |br| Initial server implementation (30).

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <https://is.gd/3Udt>`_.
|   `Labase <https://labase.github.io/>`_ - `NCE <https://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.
"""
from collections import namedtuple

from browser import timer, worker, window, websocket
from browser.widgets.dialog import InfoDialog

HOST = window.location.host
print(str(HOST))


class Combo:
    COMBO = namedtuple("Combo", ["hub", "view", "control", "work", "db"])

    def __init__(self, proxy=None):
        self.proxy = proxy
        self._publisher = {}
        self._subscriber = {}
        self._combo = self.COMBO

    def execute(self, method_name, *args, **kwargs):
        resolve = self.__publisher(method_name, *args)
        # print("execute resolve", resolve)
        return resolve if resolve else None

    def publish(self, component_name, method_name, method):
        self._publisher[component_name] = (method_name, method)

    def subscribe(self, component_name, method_name, method):
        sb, comp_met = self._subscriber, (component_name, method)
        sb.update({method_name: [comp_met] if method_name not in sb else sb[method_name] + [comp_met]})
        # self._subscriber.setdefault(method_name, [component_name, method])

    def __publisher(self, method_name, *arguments):
        if method_name in self._subscriber:
            x = [method(*arguments) for component_name, method in self._subscriber[method_name]]
            print("__publisher", x, self._subscriber[method_name])
            return x[0] if x or x[0] else None
        else:
            print("__publisher fail", method_name, self._subscriber)
            return None

    def application_builder(self):
        from vista import Body
        from controle import Control

        class View(Combo):
            pass

        class Controller(Combo):
            pass

        class Work(Combo):
            pass

        class Db(Combo):
            pass

        self._combo(self, View(Body(self, self)), Controller(Control(self)), Work(), Db())


class Hub(Combo):
    """General hub for communication exchange."""

    def __init__(self):
        super().__init__()
        self._hub = None
        self._handler = {}
        self._ws = None
        self.worker_builder()
        self._open(0)
        self.application_builder()
        self.execute("inicio")

    def worker_builder(self):
        def on_message(evt):
            data = evt.data
            print("npc", data)
            self._handler["update_foto"](0, data) if "update_foto" in self._handler else None
            # self._componentes[self.part.foto].build[0].text = data

        def on_ready(npc):
            print("npc on_ready", npc)

            def go_npc():
                npc.send(0)

            # timer.set_interval(go_npc, 8000)

        worker.create_worker("player", on_ready, on_message)

    def register(self, part):
        self._handler.update(part)

    def on_open(self, evt):
        InfoDialog("websocket", f"Connection open")

    def on_message(self, evt):
        # message received from server
        InfoDialog("websocket", f"Message received : {evt.data}")

    def on_close(self, evt):
        # websocket is closed
        InfoDialog("websocket", "Connection is closed")

    def _open(self, ev):
        if not websocket.supported:
            InfoDialog("websocket", "WebSocket is not supported by your browser")
            return
        # open a web socket
        self._ws = websocket.WebSocket(f"http://{HOST}/ws")
        # self._ws = websocket.WebSocket("http://localhost:8585/ws")
        # bind functions to web socket events
        self._ws.bind('open', self.on_open)
        self._ws.bind('message', self.on_message)
        self._ws.bind('close', self.on_close)

    def send(self, data):
        if data:
            self._ws.send(data)

    def close_connection(self, ev):
        self._ws.close()


# Body(Control, Hub())
Hub()
