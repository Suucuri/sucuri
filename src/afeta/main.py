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
from random import sample, choice, shuffle
# FX, FY, AFETO = 12, 8, "url(../_media/afetou.jpg)"
CI, FX, FY, AFETO = 10101, 12, 8, "url(_media/afetou.jpg)"


class Body:
    """Dynamic Web Document Builder for Body"""
    def __init__(self):
        self.body = document.body
        self.emo, self.chosen, self.st, self.bet = [[]]*4
        self.setup()
        self.render()
        # self.build()

    def setup(self):
        def bet(a, b):
            """Create bet chip with loosing and gaining points"""
            dd = f'<span class="has-text-info-light is-size-4">{chr(CI+a)}</span>'
            uu = f'<span class="has-text-warning-light is-size-4">{chr(CI+b)}</span>'
            return f'{dd}&nbsp;‖&nbsp;{uu}'
        self.emo, self.chosen = list(range(48*2)), []
        shuffle(self.emo)
        self.st = "Amor Raiva Tristeza Alegria Surpresa Medo".split()
        self.bet = [bet(a, b) for a in range(1, 7) for b in range(1, 5) if a >= b]
        emo = sample(self.st, 4)
        self.chosen = [(0, choice(EMO[cs])) if cs in emo else (1, cs) for cs in self.st]

    def sprite(self):
        """Near layer should be more spaced"""
        def calc(x, y):
            item = self.emo.pop()  # randint(0, 48)
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
        st = self.st
        CL = {s: "section", f: "figure", b: "button is-primary is-larger is-fullwidth", "col": "column is-3",
              "cls": "columns is-multiline is-variable is-2 mb-8", "cnt": "container", "box": "box",
              "bxc": "box has-text-centered", "clv": "columns is-variable is-2", "cmn": "column",
              e: "fas fa-recycle fa-2x", "tag": "tag is-warning is-medium", "btt": "button",
              "bin": "button is-danger is-large is-fullwidth mb-3", "bad": "buttons has-addons is-centered mb-3",
              "bts": "button is-small is-fullwidth", "cl1": "columns", "cl2": "columns is-2",
              "cmm": "columns is-multiline is-mobile", "st": "fas fa-star fa-2x", "cn2": "column is-2",
              "cmc": "columns is-multiline is-centered has-text-centered", "crd": "card",
              "bbt": "buttons has-addons is-centered mx-3 px-3", "par": "title is-5 mt-2",
              "go": "fas fa-circle fa-2x", "gat": "tag is-info is-medium", "not": "tag is-dark is-medium",
              "d": "button is-danger is-larger is-fullwidth"}

        def c(elt, cnt, clazz):
            img = i(src="https://picsum.photos/seed/picsum/600/400?random=1", alt="pic0")
            return img if elt == i else elt(cnt, Class=CL[clazz])

        def button():
            return [c(d, c(b, _e, b if n else "d"), "cmn") for n, _e in self.chosen]

        def cols():
            return [c(d, c(d, [c(f, self.sprite(), f), c(html.P, n, "par")], "bxc"), "col")
                    for n in range(8)]

        def panel():
            pre = c(d, c(p, "♻", "not"), "cmn")
            pos = c(d, c(e, "⭐", "not"), "cmn")
            track = [pre] + [c(d, c(p, abs(h), "tag" if h > 0 else "gat"), "cmn") for h in range(-5, 6)] + [pos]
            track[6] = c(d, c(e, "🮕", "not"), "cmn")
            return track

        def aposta():
            def clue_bet():
                clue = c(d, [c(b, nm, "btt") for nm in range(6)], "bad")
                chips = [c(d, c(d, c(b, bt, "btt"), "crd"), "cn2") for bt in self.bet]
                bet = c(d, c(d, chips, "bbt"), "box")
                return [clue, bet]

            return [c(d, [c(b, f"foto de {h}", "bin"), *clue_bet()], "cmn")
                    for h in st[:2]]

        gallery = c(d, c(d, cols(), "cls"), "box")
        buttons = c(d, c(d, button(), "clv"), "box")
        panels = c(d, c(d, panel(), "clv"), "box")
        aposta = c(d, c(d, aposta(), "cl1"), "box")
        bd = c(s, c(d, [gallery, buttons, panels, aposta], "cnt"), s)
        _ = self.body <= bd


EMO = {'Raiva': ['Fúria', 'Ódio', 'Ressentimento', 'Indignação', 'Hostilidade'],
       'Amor': ['Afeição', 'Adoração', 'Paixão', 'Devoção', 'Compaixão'],
       'Alegria': ['Felicidade', 'Euforia', 'Deleite', 'Entusiasmo', 'Contentamento'],
       'Tristeza': ['Luto', 'Mágoa', 'Melancolia', 'Desespero', 'Solidão'],
       'Medo': ['Ansiedade', 'Terror', 'Pânico', 'Pavor', 'Horror'],
       'Surpresa': ['Espanto', 'Choque', 'Assombro', 'Descrença', 'Admiração']}
Body()
