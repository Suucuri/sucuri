#!/usr/bin/env python
# noinspection GrazieInspection
"""Main Engine for Emotion Game.

Classes neste módulo:
    - :py:class:`Act` Database registry classes.
    - :py:class:`Afeto` Emotion game engine.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    25.03
   |br| Initial game implementation (22).

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <https://is.gd/3Udt>`_.
|   `Labase <https://labase.github.io/>`_ - `NCE <https://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.
"""
# import uuid
from collections import namedtuple

# import vista
# import main
# from vista import Parte
PARTE = namedtuple("Part", "foto, sentir, ficha, aguarda")


class ParteResposta:  # (Parte):
    def __init__(self, proxy=None):
        super().__init__()
        self._proxy = proxy
        self._register_listeners()

    def _handle_part(self):
        pass
        # self._proxy._handle_part()

    def _handle_action(self):
        pass

    def _register_listeners(self):
        pass

    def build(self, arg):
        return self._proxy.build(arg)


class Afeto:
    def __init__(self, hub, body: namedtuple):  # : vista.Body):
        self._registry = {}
        self._body = body
        self._hub = hub
        self._types = self._build(hub)
        partes, nomes = self._types._asdict().items(), self._types._asdict().keys()
        self._parts = PARTE(**{k: v(getattr(body, k)) for k, v in partes})
        self._components: PARTE = PARTE(**{k: [] for k, v in partes})
        self._factory()
        # b.foto()

    def _factory(self):
        def _do_foto(part):
            # print("do_foto", part, self._parts.foto._proxy)
            [self._components.foto.append(self._parts.foto.build(pr)) for pr in part]

        def _do_sentir(part):
            [self._components.sentir.append(self._parts.sentir.build(pr)) for pr in part]

        def _do_ficha(part):
            [self._components.ficha.append(self._parts.ficha.build(pr)) for pr in part]

        def _do_aguarda(part):
            [self._components.aguarda.append(self._parts.aguarda.build(pr)) for pr in part]

        partes, nomes = self._types._asdict().items(), self._types._asdict().keys()
        builders = (_do_foto, _do_sentir, _do_ficha, _do_aguarda)
        [self._hub.subscribe(None, f"build_{nome}", builder) for nome, builder in zip(nomes, builders)]

    def _build(self, hub):
        def _register_listeners():
            print("_register_listeners")
            hub.subscribe(self.__class__.__name__, "show_fotos", _show_fotos)
            hub.subscribe(self.__class__.__name__, "foto_sel", lambda me, *args: me._foto_sel(*args))
            hub.subscribe(self.__class__.__name__, "foto_emo", lambda me, *args: me._foto_emo(*args))
            hub.subscribe(self.__class__.__name__, "sel_done", _show_fotos)
            hub.subscribe(self.__class__.__name__, "emo_all", _emo_all)
            hub.subscribe(self.__class__.__name__, "emo_sel", lambda me, *args: me._emo_sel(*args))

        def _show_fotos(*_):
            [foto.restore() for foto in self._components.foto]

        def _emo_all(*_):
            [emo.activate() for emo in self._components.sentir]

        class Foto(ParteResposta):
            # def __init__(self):
            #     super().__init__()

            def _handle_action(self):
                hub.execute("handle_event", self)

            def _foto_sel(self):
                self._proxy.activate()

            def _foto_emo(self, emo):
                self._proxy.text = emo

            def _sel_done(self):
                self._proxy.restore()

        class Sentir(ParteResposta):

            def _register_listeners(self):
                print("Sentir_register_listeners")
                # hub.subscribe(self.__class__.__name__, "emo_all", self._emo_all)
                # hub.subscribe(self.__class__.__name__, "emo_sel", self._emo_sel)
                # hub.subscribe(self.__class__.__name__, "sel_done", self._sel_done)

            # def _emo_all(self, emos):
            #     # [self._proxy.activate(foto) for foto in emos]
            #     print("emo_all", emos)
            #     [emo.activate() for emo in y._components.sentir]

            def _emo_sel(self):
                self._proxy.restore()
                hub.execute("sel_emo", self._proxy.nome)

            def _sel_done(self):
                self._proxy.restore()

        class Ficha(ParteResposta):
            pass

        class Aguardar(ParteResposta):
            pass

        # y = self
        _register_listeners()
        return PARTE(Foto, Sentir, Ficha, Aguardar)


if __name__ == '__main__':
    pass
