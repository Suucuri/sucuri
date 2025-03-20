#!/usr/bin/env python
# noinspection GrazieInspection
""" Web server runner.

Classes neste módulo:
    - :py:class:`Body` build document body.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    25.03
   |br| Initial server implementation (07).

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <https://is.gd/3Udt>`_.
|   `Labase <https://labase.github.io/>`_ - `NCE <https://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.
"""
from browser import document, html


class Body:
    def __init__(self):
        self.body = document.body
        self.render()
        # self.build()

    def build(self):
        def cols():
            return [html.DIV(  # column
                            html.DIV(  # column
                                html.H1("oi"),
                                Class="box has-text-centered"),
                            Class="column is-3") for _ in range(3)]
        _ = self.body <= html.SECTION(  # section
            html.DIV(  # container
                html.DIV(  # box
                    html.DIV(  # columns
                        cols(),
                        Class="columns is-multiline is-variable is-2 mb-8"),
                    Class="box"),
                Class="container"),
            Class="section")

    def render(self):
        d, s, f, b, i, p, e = html.DIV, html.SECTION, html.FIGURE, html.BUTTON, html.IMG, html.SPAN, html.I
        st = "amor raiva Tristeza Alegria Surpresa Medo".split()
        CL = {s:"section", f:"figure", b:"button is-primary is-larger is-fullwidth", "col": "column is-3",
              "cls": "columns is-multiline is-variable is-2 mb-8", "cnt": "container", "box": "box",
              "bxc": "box has-text-centered", "clv": "columns is-variable is-2 mb-6", "cmn": "column",
              e: "fas fa-recycle fa-2x", "tag": "tag is-warning is-medium", "btt": "button",
              "bin": "button is-info is-large is-fullwidth mb-3", "bad": "buttons has-addons is-centered mb-3",
              "bts": "button is-small is-fullwidth", "cl1": "columns", "cl2": "columns is-2",
              "cmm": "columns is-multiline is-mobile"}
        def c(elt, cnt, clazz):
            img = i(src="https://picsum.photos/seed/picsum/600/400?random=1", alt="pic0")
            return img if elt==i else elt(cnt, Class=CL[clazz])
        def button():
            return [c(d, c(b, n, b), "cmn") for n in st]
        def cols():
            return [c(d, c(d,c(f, c(i,"", i), f),"bxc"), "col") for _ in range(3)]
        def panel():
            pre = c(d, c(e,"", e), "cmn")
            pos = c(d, c(e,"", e), "cmn")
            return [pre]+[c(d,c(p, abs(h), "tag"), "cmn") for h in range(-5,6)]+[pos]
        def aposta():
            def clue_bet():
                clue = c(d, [c(b,nm, "btt") for nm in range(6)], "bad")
                bet = c(d, [c(d, c(b, bt, "bts"), "cl2") for bt in range(2)], "cmm")
                return [clue, bet]
            tip = c(b, "foto", "bin")
            return [c(d, [c(b, f"foto de {h}", "bin"), *clue_bet()], "cmn")
                    for h in st[:2]]
        gallery = c(d, c(d, cols(), "cls"), "box")
        buttons = c(d, c(d, button(), "clv"), "box")
        panels = c(d, c(d, panel(), "clv"), "box")
        aposta = c(d, c(d, aposta(), "cl1"), "box")
        bd = c(s, c(d, [gallery, buttons, panels, aposta], "cnt"), s)
        _ = self.body <= bd
Body()
