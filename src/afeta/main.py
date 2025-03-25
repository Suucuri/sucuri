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

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <https://is.gd/3Udt>`_.
|   `Labase <https://labase.github.io/>`_ - `NCE <https://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.
"""
from browser import document, html
from controle import Control

# FX, FY, AFETO = 12, 8, "url(../_media/afetou.jpg)"
CI, FX, FY, AFETO = 10101, 12, 8, "url(_media/afetou.jpg)"


class Body:
    """Dynamic Web Document Builder for Body"""

    def __init__(self):
        self._current_element = None

        def no_op(*_args):
            pass

        class Activate:
            """Activate"""

            def __init__(self, handler, target, go=True):
                target.append(self) if self not in target else None
                self.target = target
                self.handler = handler
                self.handle = handler if go else no_op

            def go(self):
                self.handle = self.handler

            def stop(self):
                self.handle = no_op

            def __call__(self, arg):
                print("Activate", self.target)
                self.handle(arg)
                # [sct.stop() for sct in self.target]

        self.body = document.body
        self.act = Activate
        self._handle_emotions = self._handle_foto = no_op
        self.control = Control(self)
        self.emo, self.chosen, self.st, self.bet, self._fotos, self.but = [list()] * 6
        self.b_fotos, self.b_but = list(), list()
        self.setup()
        self.render()
        # self.build()

    def betting_handler(self, chip):
        print("handle bet chips", chip, self.b_fotos)
        buttons = [button.childNodes[0].classList for button in self.but]
        [button.add("is-dark") for button in buttons]
        [button.go() for button in self.b_fotos]
        self._handle_emotions()
        [sct.stop() for sct in self.b_but]

    def emotion_handler(self, emotion):
        print("handle emotion", emotion, self.b_fotos)
        self._current_element.classList.remove("has-background-grey")
        buttons = [button.childNodes[0].classList for button in self.but]
        [button.add("is-dark") for button in buttons if "is-danger" in button]
        [button.go() for button in self.b_fotos]
        self._handle_emotions()
        [sct.stop() for sct in self.b_but]

    def foto_handler(self, foto, el):
        el.classList.add("has-background-grey")
        self._current_element = el
        buttons = [button.childNodes[0].classList for button in self.but]
        print("handle foto", foto, [cl for cl in buttons[0]])
        [button.remove("is-dark") for button in buttons if "is-danger" in button]
        print(self.b_but)
        [button.go() for button in self.b_but]
        self._handle_foto()
        [sct.stop() for sct in self.b_fotos]

    def setup(self):
        def bet(a, b):
            """Create bet chip with loosing and gaining points"""
            dd = f'<span class="has-text-info-light is-size-4">{chr(CI + a)}</span>'
            uu = f'<span class="has-text-warning-light is-size-4">{chr(CI + b)}</span>'
            return f'{dd}&nbsp;‖&nbsp;{uu}'

        self.emo, abet, self._fotos, self.chosen = self.control.play()
        # self.emo, self.chosen = list(range(48*2)), []
        # shuffle(self.emo)
        # self.st = "Amor Raiva Tristeza Alegria Surpresa Medo".split()
        self.bet = [bet(a, b) for a, b in abet]
        # emo = sample(self.st, 4)
        # self.chosen = [(0, choice(EMO[cs])) if cs in emo else (1, cs) for cs in self.st]

    def sprite(self, foto=None):
        """Near layer should be more spaced"""

        def calc(x, y):
            item = foto or self.emo.pop()  # randint(0, 48)
            conta_, lado_ = x - 1 if x > 1 else 1, y - 1 if y > 1 else 1
            return (100 / conta_) * (item % x), (100 / lado_) * (item // x)

        dw, dh = calc(FX, FY)
        bp = f"{dw:.2f}% {dh:.2f}%"
        e = html.DIV(style=dict(width="270px", height="200px", backgroundImage=AFETO, overflow="hidden"))
        e.style.backgroundSize = f"{FX * 100}% {FY * 100}%"
        e.style.backgroundPosition = bp
        return e

    def render(self):
        d, s, f, b, i, p, e = html.DIV, html.SECTION, html.FIGURE, html.BUTTON, html.IMG, html.SPAN, html.I
        # st = self.st
        CL = {s: "section", f: "figure", b: "button is-primary is-larger is-fullwidth is-dark", "col": "column is-3",
              "cls": "columns is-multiline is-variable is-2 mb-8", "cnt": "container", "box": "box",
              "bxc": "box has-text-centered", "clv": "columns is-variable is-2", "cmn": "column",
              e: "fas fa-recycle fa-2x", "tag": "tag is-warning is-medium", "btt": "button",
              "bin": "button is-danger is-large is-fullwidth mb-3", "bad": "buttons has-addons is-centered mb-3",
              "bts": "button is-small is-fullwidth", "cl1": "columns", "cl2": "columns is-2",
              "cmm": "columns is-multiline is-mobile", "st": "fas fa-star fa-2x", "cn2": "column is-1",
              "cmc": "columns is-multiline is-centered has-text-centered", "crd": "card",
              "bbt": "buttons has-addons is-centered mx-3 px-3", "par": "title is-5 mt-2",
              "go": "fas fa-circle fa-2x", "gat": "tag is-info is-medium", "not": "tag is-dark is-medium",
              "d": "button is-danger is-larger is-fullwidth is-dark", "cvs": "current_version is-size-7 has-text-grey-dark",
              "bom": "notification", "bmp": "box has-text-centered"}

        def pgr(val, mx, pct):
            return html.PROGRESS(pct, Class="progress is-large is-info", value=val, max=mx)

        def c(elt, cnt, clazz, handle=None):
            _elt = elt(cnt, Class=CL[clazz])
            _elt.bind("click", lambda *_, _e=_elt: handle(_e)) if handle is not None else None
            return _elt
            # img = i(src="https://picsum.photos/seed/picsum/600/400?random=1", alt="pic0")
            # return img if elt == i else elt(cnt, Class=CL[clazz])

        def button():
            return [
                c(d, c(
                    b, _e, b if n else "d",
                    handle=self.act(lambda *_, em=_e: self.emotion_handler(em) if not n else None,
                                    self.b_but, False)), "cmn")
                for n, _e in self.chosen]

        def cols():
            b_fotos = [
                c(d, [c(f, self.sprite(foto), f), c(html.P, n, "par")],
                  "bmp", handle=self.act(lambda el, em=foto: self.foto_handler(em, el), self.b_fotos))
                for n, foto in enumerate(self._fotos)]  # for n in range(8)]
            return [c(d, foto, "col") for n, foto in enumerate(b_fotos)]  # for n in range(8)]

        def panel():
            pre = c(d, c(p, "♻", "not"), "cmn")
            pos = c(d, c(e, "⭐", "not"), "cmn")
            track = [pre] + [c(d, c(p, abs(h), "tag" if h > 0 else "gat"), "cmn") for h in range(-5, 6)] + [pos]
            track[6] = c(d, c(e, "🮕", "not"), "cmn")
            return track

        def aposta():
            def clue_bet():
                # clue = c(d, [c(b, nm, "btt") for nm in range(9)], "bad")
                chips = [c(d, c(d, c(b, bt, "btt"), "crd"), "cn2") for bt in self.bet]
                # bet = c(d, c(d, chips, "bbt"), "box")
                bet = c(d, [c(d, c(b, f"Sentimento Escolhido: {self.chosen[2][1]}", b), "cmn")]+chips, "bbt")
                return bet

            return clue_bet()  # c(d, clue_bet(), "cmn")
            #
            # return [c(d, [c(b, f"foto de {h}", "bin"), *clue_bet()], "cmn")
            #         for h in st[:2]]

        deco = "꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫꧁ AGUARDE ꧂▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂"
        br = html.BR
        note_t, note_b = [html.P(deco + deco, Class="tag is-primary") for _ in "ab"]
        note_text = html.P("Aguarde até que os jogadores confirmem suas participações")
        note = c(d, [c(d, [note_t, br(), note_text, html.IMG(src="_media/loading.gif"), br(), note_b], "par"),
                     pgr(30, 100, 30)], "bom")
        note.style.position = "absolute"
        # gallery = c(d, c(d, [note]+cols(), "cls"), "box")
        gallery = c(d, c(d, cols(), "cls"), "box")
        self.but = button()
        buttons = c(d, c(d, self.but, "clv"), "box")
        panels = c(d, c(d, panel(), "clv"), "box")
        aposta = c(d, c(d, aposta(), "cl1"), "box")
        version = c(p,"Version - ", "cvs")
        bd = c(s, c(d, [gallery, buttons, panels, aposta, version], "cnt"), s)
        _ = self.body <= bd


Body()
