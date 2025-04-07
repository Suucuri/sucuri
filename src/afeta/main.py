#!/usr/bin/env python
# noinspection GrazieInspection
"""Dynamic Web Document Builder.

Classes neste módulo:
    - :py:class:`Hub` communication hub.

.. module:: main
    :synopsis: A messaging hub implementing publisher-subscriber pattern for inter-module communication.

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

from browser import worker, window, websocket
from browser.widgets.dialog import InfoDialog
MA = namedtuple("MA", "m, a")

HOST = window.location.host
print(str(HOST))


class MS:
    # G = {k: MA(lambda *_: None, None) for k in "error proceed_game".split()}
    G = {k: lambda *_: None for k in "error proceed_game".split()}

    @classmethod
    def x(cls, k, *args):
        # return cls.G[k].m(*args)
        return cls.G[k](*args)


class Combo:
    """
    Central messaging hub implementing publisher-subscriber pattern to facilitate communication
    between application components (hub, view, controller, work, db).

    :param proxy: Proxy object for method forwarding (optional)
    :type proxy: object

    .. py:attribute:: COMBO
        :type: namedtuple
        Container for component references with fields: hub, view, control, work, db
    """

    COMBO = namedtuple("Combo", ["hub", "view", "control", "work", "db"])

    def __init__(self, proxy=None):
        """
        Initialize messaging hub with proxy and component registry.
        Creates empty dictionaries for publishers and subscribers.
        """
        self._proxy = proxy
        self._publisher = {}
        self._subscriber = {}
        self._combo = self.COMBO

    def __getattr__(self, name):
        """
        Attribute accessor that forwards unknown attributes/methods to proxy.

        :param name: Attribute/method name being accessed
        :type name: str
        :return: Either local attribute or (proxy, name) tuple
        :rtype: Union[object, tuple]
        """
        condition = name.startswith("_") or name in ("subscribe", "execute")
        return getattr(self, name) if condition else (self._proxy, name)

    def execute(self, method_name, *args, **_):
        """
        Execute a method through the publisher-subscriber system.

        :param method_name: Name of the method to execute
        :type method_name: str
        :param args: Positional arguments for the method
        :return: Result of the first subscriber's execution or None
        :rtype: Optional[Any]
        """
        try:
            resolve = self.__publisher(method_name, *args)
            return resolve if resolve else None
        except Exception as ex:
            print("execute Exception", ex, method_name, *args)
            return None

    def _publish(self, component_name, method_name, method):
        """
        Register a publisher method.

        :param component_name: Name of publishing component
        :type component_name: str
        :param method_name: Published method name
        :type method_name: str
        :param method: Callable method reference
        :type method: Callable
        :meta private:
        """
        self._publisher[component_name] = (method_name, method)

    def subscribe(self, component_name, method_name, method):
        """
        Register a subscriber method for a given method name.

        :param component_name: Name of subscribing component
        :type component_name: str
        :param method_name: Method name to subscribe to
        :type method_name: str
        :param method: Callable method to invoke
        :type method: Callable
        """
        sb, comp_met = self._subscriber, (component_name, method)
        sb.update({method_name: [comp_met] if method_name not in sb else sb[method_name] + [comp_met]})

    def __publisher(self, method_name, *arguments):
        """
        Internal method to invoke subscribed methods.

        :param method_name: Method name to publish
        :type method_name: str
        :param arguments: Arguments to pass to subscribers
        :return: First subscriber's result or None
        :rtype: Optional[Any]
        :meta private:
        """
        if method_name in self._subscriber:
            x = [method(*arguments) for component_name, method in self._subscriber[method_name]]
            return x[0] if x or x[0] else None
        else:
            print("__publisher fail", method_name, self._subscriber)
            return None

    def _application_builder(self):
        """
        Construct application component hierarchy.

        Creates and initializes View, Controller, Work, and Db components,
        wiring them into the COMBO structure.

        :meta private:
        """
        combo = self
        from vista import Body
        from controle import Control

        class View(Combo):
            """Component responsible for UI presentation"""
            pass

        class Controller(Combo):
            """Component handling business logic and workflow"""
            pass

        class Work(Combo):
            """Background work processor"""
            def __init__(self):
                super().__init__()
            pass

        class Db(Combo):
            """Database access component"""
            pass

        self._combo(self, View(Body(self, self)), Controller(Control(self)), Work(), Db())


class Hub(Combo):
    """General hub for communication exchange."""

    def __init__(self):
        super().__init__()
        self._hub = self._worker = None
        self._handler = {}
        self._ws = None
        self.worker_builder()
        # self._open(0)
        self._application_builder()
        # ops = (self.error, self._subscriber["proceed_game"]())
        ops = (self.error, self.proc_game, self.new_player)
        MS.G = {k: op for k, op in zip("error proceed_game new_player".split(), ops)}
        self.execute("inicio")

    def new_player(self, *a):
        self.execute("new_player", *a)

    def proc_game(self, *a):
        self.execute("proceed_game", *a)

    def error(self, msg):
        InfoDialog("Worker Error", f"Error received : {msg}")

    def worker_builder(self):
        def on_message(evt):
            data = evt.data
            print("worker on message", *data)
            MS.x(*data)

        def on_ready(npc):
            print("npc on_ready", npc)
            self._worker = npc
            npc.send(['recruit_players', 4])
            # npc.send(json.dumps(['recruit_players', 4]))
            #
            # def go_npc():
            #     npc.send(0)

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
