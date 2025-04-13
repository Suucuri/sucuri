#!/usr/bin/env python
# noinspection GrazieInspection
"""Dynamic Web Document Builder.

Classes neste módulo:
    - :py:class:`Body` build document body.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    25.03
   |br| Initial server implementation (07).
   |br| Improve bet chips (23).
   |br| Refactor ops into Foto, Sentir & Ficha (28).

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <https://is.gd/3Udt>`_.
|   `Labase <https://labase.github.io/>`_ - `NCE <https://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.
"""
from collections import namedtuple
from random import choice, randint
from browser import document, html
from typing import override
CI, FX, FY, AFETO = 10101, 12, 8, "url(_media/afetou.jpg)"
Z = namedtuple("Z", "d s f b i p e h r g t")(
    html.DIV, html.SECTION, html.FIGURE, html.BUTTON, html.IMG, html.SPAN, html.I,
    html.HEADER, html.FOOTER, html.P, html.H1)
COMP = namedtuple("Comp", ["build", "comps"])


def no_op(*_args):
    pass


class Parte:
    def __init__(self):
        self._nome = self._actor = self._action = self._text = self._tag = self._last = None

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text += f", {text}"
        if self._tag is not None:
            self._tag.innerHTML = self._text

    def update_view(self, *args):
        self._handle_part()

    def _handle_part(self):
        self.activate_any()
        self._current_element = self
        # self._current_part.activate_all()
        # print("handle foto", foto, self._current_element, self._componentes[self.part.foto].build)
        # self._handle_foto(foto, el, self._current_element)

    def activate_any(self):
        pass


class Body:
    """Dynamic Web Document Builder for Body"""
    CLS = {'a': 'modal is-active', 'b': 'modal-background', 'c': 'modal-card-body',
           'd': 'box has-text-centered vintage-box', 'e': 'vintage-frame', 'f': 'old-photo',
           'g': 'title is-3 has-text-white waiting-title', 'h': 'subtitle is-5 has-text-light',
           'i': 'loading-container', 'j': 'loading-spinner', 'k': 'has-text-white', 'l': 'modal-card',
           'm': 'modal-card-head', 'n': 'modal-card-title', 'o': 'modal-card-foot', 'p': 'modal-close', 'q': 'delete',
           'r': 'Aguarde os outros Jogadores', 's': 'Analisando fotos',
           't': 'Revivendo memórias', 'u': 'Analisando emoções nas fotos...', 'v': 'Aguarde a sua vez'
           }
    FT = None

    def __init__(self, hub, *_args, **_kwargs):
        self.hub = hub
        self._current_element = self._tips = self._current_part = None
        self._hub = hub
        self._sentires, self.fotos, self._fichas = [list()] * 3
        hub.subscribe(self.__class__.__name__, "inicio", self.inicio)
        self.body = document.body
        self._handle_emotions = self._handle_foto = no_op
        self._handle_emotions = self.do_handle
        self.emo, self.chosen, self.bet, self._fotos, self.but = [list()] * 5
        self._build_parts()
        # hub.register(dict(update_foto=self._update_foto))
        hub.subscribe(self.__class__.__name__, "new_player", self.part.aguarda.new_player)
        hub.subscribe(self.__class__.__name__, "proceed_game", self.part.aguarda.restore)
        hub.subscribe(self.__class__.__name__, "view_update", self._view_update)

        # self.go()
    def _build_parts(self):
        y = self

        class Sentir(Parte):
            def _act(self, _, _e, _handler, go=False):
                self._action = Activate(_handler, _e, target=self, go=go)
                return self._action

            def _handler(self, evt):
                y._current_handler(evt, self.__class__.__name__, self._text)

            def _builder(self, n, _e):
                def handle_event(data, el):
                    self._text, self._last = _e, y._current_element
                    y._current_element = self
                    y._current_handler(data, self.__class__.__name__, n)  # self._text)

                c, b, d, self._text = y.c, Z.b, Z.d, _e
                self._text = _e
                # self._actor = c(b, _e, b if n else "dk", handle=self._act(n, _e, y.emotion_handler))
                self._actor = c(b, _e, b if n else "dk", handle=self._act(n, _e, handle_event))
                node = c(d, self._actor, "cmn")
                return node

            @override
            def _handle_part(self) -> None:
                # print("handle emotion", self._text, y._current_element, self._nome, self._actor)
                y.part.foto.restore_all()
                y.part.sentir.restore_all()
                self._last.text = self._text
                # y._handle_emotions(self._text, self, y._current_element)
                # y._current_element = self

            def activate(self):
                if "is-danger" in self._actor.classList:
                    self._actor.classList.remove("is-dark")
                    self._action.go()

            def restore(self):
                self._actor.classList.add("is-dark") if "is-danger" in self._actor.classList else None
                self._action.stop()

            @classmethod
            def _build(cls, n, _e):
                _cls = cls()
                y._componentes[cls].build.append(_cls)
                return _cls._builder(n, _e)

            @classmethod
            def restore_all(cls):
                [comp.restore() for comp in y._componentes[cls].build]

            @classmethod
            def activate_all(cls):
                [comp.activate() for comp in y._componentes[cls].build]

            @classmethod
            def build(cls):
                return [cls._build(n, _e) for n, _e in y.chosen]

        class Aguardar(Sentir):
            def __init__(self):
                super().__init__()
                self._builder(0, 0)

            @override
            def _builder(self, n, _e):
                c, b, d, h, r, s, p, t, z, self._nome = y.c, Z.b, Z.d, Z.h, Z.r, Z.s, Z.g, Z.t, Body.CLS, _e
                button = html.BUTTON(Class="delete", **{"aria-label": "close"})
                head = c(h, [c(p, z["r"], "n"), button], "m")
                im = y.sprite(randint(0, 90))
                im.width, im.height, im.style.filter = 470, 400, "blur(8px)"
                sp = [[c(t, z["u"], "h"), c(d, [c(d, "", "j")], "i")], ]
                section = [c(d, [c(d, im, "e"), sp], "d")]
                self._tag = html.PROGRESS(0, Class="progress is-large is-info", value=20, max=100)
                foot = [c(r, self._tag, "o")]
                content = [c(d, "", "b"), c(d, [head, section, foot], "l")]
                self._actor = node = c(d, content, "a")
                return node

            @property
            def actor(self):
                return self._actor

            @property
            def text(self):
                return self._text

            @text.setter
            def text(self, text):
                self._text = text
                # print("Aguarda new_player", text, self.text, self._tag)
                if self._tag is not None:
                    self._tag.value = int(self._text)

            def new_player(self, players=1):
                self.text = int(players) * 25

            @override
            def activate(self):
                self._actor.classList.add("is-active")
                self._action.go()

            @override
            def restore(self):
                self._actor.classList.remove("is-active") if self._actor else None
                # print("Aguarda restore", self._actor, self.text, self._tag)
                # self._action.stop()

            @classmethod
            def _build(cls, n, _e):
                _cls = cls()
                # y._componentes[cls].build.append(_cls)
                return _cls._builder(n, _e)

            @classmethod
            def restore_all(cls):
                [comp.restore() for comp in y._componentes[cls].build]

            @classmethod
            def activate_all(cls):
                [comp.activate() for comp in y._componentes[cls].build]

            @classmethod
            def build(cls):
                return cls._build(0, 0)

        class Foto(Sentir):

            @override
            def _builder(self, n, foto):
                def handle_event(data, el):
                    y._current_element = self
                    y._current_handler(data, self.__class__.__name__, self._text)
                    # self._handle_part()
                    # y.foto_handler(data, el)
                c, b, d, f, self._sentiu = y.c, Z.b, Z.d, Z.f, foto
                self._text = str(n)
                self._tag = c(html.P, n, "par")
                self._actor = c(d, [c(f, y.sprite(foto), f), self._tag],
                                "bmp", handle=self._act(n, foto, handle_event, True))
                # "bmp", handle=self._act(n, foto, y.foto_handler, True))
                node = c(d, self._actor, "cmn")
                self.restore()
                return node

            @override
            def _handle_part(self) -> None:
                self.restore_all()
                self.activate()
                y._current_part.activate_all()
                print("handle foto part", self._text, )

            @override
            def activate(self):
                # print(self._sentiu, self._action)
                self._actor.classList.add("has-background-grey")
                self._action.stop()

            @override
            def restore(self):
                # print(self._sentiu, self._action)
                self._actor.classList.remove("has-background-grey")
                self._action.go()

            @classmethod
            def build(cls):
                c, b, d, f = y.c, Z.b, Z.d, Z.f
                b_fotos = [cls._build(n, foto) for n, foto in enumerate(y._fotos)]
                return [c(d, foto, "col") for n, foto in enumerate(b_fotos)]

        class Ficha(Sentir):

            @override
            def _builder(self, n, _e):
                def make_bet(bk, fd):
                    """Create bet chip with loosing and gaining points"""
                    dd = f'<span class="has-text-info-light is-size-4">{chr(CI + bk)}</span>'
                    uu = f'<span class="has-text-warning-light is-size-4">{chr(CI + fd)}</span>'
                    return f'{dd}&nbsp;‖&nbsp;{uu}'

                self._text = str(n)
                c, b, d, self._nome, self._tag = y.c, Z.b, Z.d, _e, n
                self._actor = c(b, make_bet(*_e), "btt", handle=self._act(n, _e, y.betting_handler))  # .act(
                node = c(d, self._actor, "crd")
                return node

            @classmethod
            def build(cls):
                c, b, d = y.c, Z.b, Z.d
                tag = c(b, "Nada ainda", b)
                chips = [c(d, cls._build(tag, bt), "cn2") for bt in y.bet]
                bet = c(d, [c(d, tag, "cmn")] + chips, "bbt")
                return bet

        class Activate:
            """Activate"""

            def __init__(self, handler, element, target, go=True):
                def event_handler(*_args, **_kwargs):
                    return handler(element, target)

                self.handler = event_handler
                self.handle = self.handler if go else no_op

            def go(self):
                self.handle = self.handler

            def stop(self):
                self.handle = no_op

            def __call__(self, arg):
                # print("Activate", self.handle, arg)
                self.handle(arg)
        self.part = namedtuple("Part", "foto, sentir, ficha, aguarda")(Foto, Sentir, Ficha, Aguardar())
        self._current_part = self.part.sentir
        self._tips = []
        self._componentes = {k: COMP(list(), list()) for k in [Sentir, Foto, Ficha, Aguardar]}

    def inicio(self):
        self.setup()
        self.render()

    # def _update_foto(self, idc, data):
    #     self._componentes[self.part.foto].build[idc].text = data

    def do_handle(self, texto, tip, origin: Parte):
        self._tips.append(texto)
        assert isinstance(origin, Parte), type(origin)
        tips = self._componentes[self.part.ficha].build[0]
        print("do_handle", origin, tip, texto, tips, tips.text)
        origin.text = texto
        if len(self._tips) >= 2:
            if self._current_part == self.part.ficha:
                self.part.sentir.restore_all()
                self.part.ficha.restore_all()
                self.part.foto.activate_all()
                return
            sen = f"Sentimento: {choice(self._tips)}"
            self._tips = []
            self._componentes[self.part.ficha].build[0].text = sen
            # self._handle_foto = self.do_foto
            self.part.sentir.restore_all()
            self.part.foto.restore_all()
            self._current_part = self.part.ficha

    def betting_handler(self, chip, foto):
        print("handle bet chips", chip, foto)
        self.part.foto.restore_all()
        self.part.ficha.restore_all()
        self._handle_emotions(chip, foto, self._current_element)
        self._current_element = foto

    def emotion_handler(self, emotion, sentir):
        print("handle emotion", emotion, self._current_element)
        self.part.foto.restore_all()
        self.part.sentir.restore_all()
        self._handle_emotions(emotion, sentir, self._current_element)
        self._current_element = sentir

    def setup(self):
        self.emo, abet, self._fotos, self.chosen = self._hub.execute("play")
        print("setup", abet, self._fotos, self.chosen)
        self.bet = [(a, b) for a, b in abet]

    def sprite(self, foto=None):
        """Near layer should be more spaced"""

        def calc(x, y):
            item = foto or self.emo.pop()  # randint(0, 48)
            item = int(item)
            conta_, lado_ = x - 1 if x > 1 else 1, y - 1 if y > 1 else 1
            return (100 / conta_) * (item % x), (100 / lado_) * (item // x)

        dw, dh, = calc(FX, FY)
        bp = f"{dw:.2f}% {dh:.2f}%"
        e = html.DIV(style=dict(width="270px", height="200px", backgroundImage=AFETO, overflow="hidden"))
        e.style.backgroundSize = f"{FX * 100}% {FY * 100}%"
        e.style.backgroundPosition = bp
        return e

    def c(self, elt, cnt, clazz, handle=None):
        _ = self
        d, s, f, b, i, p, e = Z.d, Z.s, Z.f, Z.b, Z.i, Z.p, Z.e
        CL = {s: "section", f: "figure", b: "button is-primary is-larger is-fullwidth is-dark", "col": "column is-3",
              "cls": "columns is-multiline is-variable is-2 mb-8", "cnt": "container", "box": "box",
              "bxc": "box has-text-centered", "clv": "columns is-variable is-2", "cmn": "column",
              e: "fas fa-recycle fa-2x", "tag": "tag is-warning is-medium", "btt": "button is-danger is-dark",
              "bin": "button is-danger is-large is-fullwidth mb-3", "bad": "buttons has-addons is-centered mb-3",
              "bts": "button is-small is-fullwidth", "cl1": "columns", "cl2": "columns is-2",
              "cmm": "columns is-multiline is-mobile", "st": "fas fa-star fa-2x", "cn2": "column is-1",
              "cmc": "columns is-multiline is-centered has-text-centered", "crd": "card",
              "bbt": "buttons has-addons is-centered mx-3 px-3", "par": "title is-5 mt-2",
              "go": "fas fa-circle fa-2x", "gat": "tag is-info is-medium", "not": "tag is-dark is-medium",
              "dk": "button is-danger is-larger is-fullwidth is-dark",
              "cvs": "current_version is-size-7 has-text-grey-dark",
              "bom": "notification", "bmp": "box has-text-centered"}
        CL.update(Body.CLS)
        _elt = elt(cnt, Class=CL[clazz])
        _elt.bind("click", lambda *_, _e=_elt: handle(_e)) if handle is not None else None
        return _elt

    def render(self):
        c = self.c
        d, s, f, b, i, p, e = Z.d, Z.s, Z.f, Z.b, Z.i, Z.p, Z.e

        def pgr(val, mx, pct):
            return html.PROGRESS(pct, Class="progress is-large is-info", value=val, max=mx)

        def button():
            return self.part.sentir.build()

        def cols():
            return self.part.foto.build()

        def panel():
            pre = c(d, c(p, "♻", "not"), "cmn")
            pos = c(d, c(e, "⭐", "not"), "cmn")
            track = [pre] + [c(d, c(p, abs(h), "tag" if h > 0 else "gat"), "cmn") for h in range(-5, 6)] + [pos]
            track[6] = c(d, c(e, "🮕", "not"), "cmn")
            return track

        def aguarda():
            a = self.part.aguarda
            # print("aguarda", a.actor)
            return a.actor

        def aposta():
            return self.part.ficha.build()

        deco = "꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫꧁ AGUARDE ꧂▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂"
        br = html.BR
        note_t, note_b = [html.P(deco + deco, Class="tag is-primary") for _ in "ab"]
        note_text = html.P("Aguarde até que os jogadores confirmem suas participações")
        note = c(d, [c(d, [note_t, br(), note_text, html.IMG(src="_media/loading.gif"), br(), note_b], "par"),
                     pgr(30, 100, 30)], "bom")
        note.style.position = "absolute"
        gallery = c(d, c(d, cols(), "cls"), "box")
        buttons = c(d, c(d, button(), "clv"), "box")
        panels = c(d, c(d, panel(), "clv"), "box")
        aposta = c(d, c(d, aposta(), "cl1"), "box")
        version = c(p, "Version - ", "cvs")
        bd = [c(s, c(d, [gallery, buttons, panels, aposta, version], "cnt"), s), aguarda()]  # .build()]
        _ = self.body <= bd

    # def npc(self, *_):
    #     print("npc")
        # self._componentes[self.part.foto].build[0].text = "|"
    def _current_handler(self, *args):
        from controle import DATA
        self.hub.execute("handle_event", DATA(*args))

    def _view_update(self, *args):
        print("DID >>> _view_update", self._current_element, self._current_element.update_view)
        self._current_element.update_view(*args)
