#!/usr/bin/env python
# noinspection GrazieInspection
"""Main Engine for Presentation.

Classes neste módulo:
    - :py:class:`Act` Database registry classes.
    - :py:class:`Afeto` Emotion game engine.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    25.04
   |br| Initial presentation implementation (26).

.. versionadded::    25.04
   |br| New component address registration (19).
   |br| Response Objects (23).

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <https://is.gd/3Udt>`_.
|   `Labase <https://labase.github.io/>`_ - `NCE <https://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.
"""
from vitollino import Cena, STYLE, Elemento
from browser import html, markdown, window
import vitollino
from text import PFD, IMG

vitollino.STYLE = dict(width=4400, height=3200)
IMD = "../_media/talk/{}.jpeg"
PFK = """
&nbsp;&nbsp;&nbsp;&nbsp;<br/>
&nbsp;&nbsp;&nbsp;&nbsp;O massacre dos povos originários.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;As ideias iniciais em [PbWiki]<br/>
&nbsp;&nbsp;&nbsp;&nbsp;O curumim Tchuck e a cunhatã Kiri<br/>
&nbsp;&nbsp;&nbsp;&nbsp;Programando para enfrentar desafios<br/>
&nbsp;&nbsp;&nbsp;&nbsp;Desafios: É pau é pedra. Pisa na fulô<br/>
"""
PFM = """
&nbsp;&nbsp;&nbsp;&nbsp;<br/>
## O massacre dos povos originários.<br/>
- As ideias iniciais em [PbWiki]<br/>
- O curumim *Tchuck* e a cunhatã Kiri<br/>
- Programando para enfrentar desafios<br/>
- Desafios: É pau é pedra. Pisa na fulô<br/>
"""
SHOW = [500, 150, 800, 600, 10]
SW, SH = 800, 600


class Main:
    def __init__(self):
        self.cena = c = Cena("../_media/talk/sbtema.jpg")
        cenas = IMG * 2
        self.slide_spec = zip(cenas, PFD)
        c.elt.style.position = "absolute"
        c.elt.style.transition = "transform 1.5s ease-in-out"
        mainer = self
        W, H = window.innerWidth, window.innerHeight

        class Span:
            def __init__(self, tx, x=500, y=150, w=1200, h=600, color="peru", weight="bold", size="95px", cn=None):
                txm, _ = markdown.mark(tx)
                # bp = html.SPAN(txm, style=dict(color=color, fontSize=size, fontWeight=weight))
                bp = html.SPAN(tx, style=dict(color=color, fontWeight=weight, fontSize=size, position="absolute"))
                e = Elemento("", x=x, y=y, w=w, h=h, cena=cn or c)
                e.elt.bind("click", mainer.vai)
                _ = e.elt <= bp

        c.vai()

        class Slide:
            def __init__(
                    self, img, tx, x=0, y=0, w=SW, h=SH, sc=1.0,
                    color="navajowhite", weight="normal", size="30px", spans=None):
                scn = sc
                # print(x, y, h, H, sc, yn)
                self.init = [x, y, w, h, scn * 1.0]
                txm, _ = markdown.mark(tx)
                e = Elemento(
                    img, x=x, y=y, w=w, h=h, cena=c,
                    style=dict(position="absolute", overflow="hidden", backgroundSize="cover",
                               borderRadius="20px", transform=f"scale({sc}) translate({x}px, {y}px)",
                               transformOrigin="0px 0px", ))
                s = Elemento("", x=50, y=50, w=w - 200, h=h - 100, o=0.5, cena=c,
                             style=dict(borderRadius="40px", backgroundColor=color, paddingLeft="20px"))
                _ = e.elt <= s.elt
                bp = html.SPAN(txm, style=dict(color="black", fontWeight=weight, fontSize=size))
                _ = s.elt <= bp
                e.elt.bind("click", self.vai)
                if spans is not None and len(spans) > 0:
                    [Span(tx, x=x, y=y, color=col, weight=wei, size=siz, cn=e) for tx, x, y, col, wei, siz in spans]

            def vai(self, *_):
                x, y, w, h, scn = self.init
                fsc = (H / h)
                scs = (H - h) / 2
                scr = (1.0 / scn) * fsc
                print("foi", x, y, w, h, scn, 1.0 / 1.0)
                xn = (scs - x) * fsc - x * scr
                yn = -y * fsc - y * scr
                c.elt.style.transformOrigin = "0px 0px"
                c.elt.style.transform = f"translate({xn}px, {yn}px) scale({scr})"

        # self.s1 = s1 = Slide("../_media/talk/caveira.jpeg", PFD[2], sc=0.2, x=1600, y=200)
        ox = 10
        sps = [("Bem Vindo ao LABASE", ox, 150, "saddlebrown", "bold", "68px"),
               ("Laboratório de Automação", ox, 280, "peru", "bold", "60px"),
               ("de Sistemas Educacionais", ox, 390, "peru", "bold", "60px")]
        # s0 = Slide("", "", color="#0080FF80", sc=0.95, x=400, y=200, w=1000, spans=sps)
        s0 = Slide("", "", color="#00000000", sc=1.7, x=600, y=320, w=800, spans=sps)
        self.slides = [s0] + [Slide(IMD.format(im), tx, sc=0.2, x=200+3000*(ix % 2), y=500+100 * (ix // 2))
                              for ix, (im, tx) in enumerate(self.slide_spec)]
        self.current = 0

        c.elt.bind("click", self.vai)
        self.vai()

    def vai(self, *_):
        print("foi", self.current)
        self.slides[self.current].vai()
        self.current = (self.current + 1) if self.current < len(self.slides)-1 else 0
        # self.s1.vai()


if __name__ == '__main__':
    main = Main()
