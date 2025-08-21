#!/usr/bin/env python
# noinspection GrazieInspection
"""Html Page Builder.

Reads a Template builder an fill in content data.

Classes neste módulo:
    - :py:class:`Template` Html calls and template code builder.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>
.. tip:: *Milestone* 🚧 ⛲ 🛠️ Golden Penta ⭐ 25.08 (21)

Changelog
---------
.. versionadded::    25.08
   |br| Initial builder implementation (21).
   |br| code from toml (18).

|   **Open Source Notification:** This file is part of open source program **Alite**
|   **Copyright © 2025  Carlo Oliveira** <carlo@nce.ufrj.br>,
"""
from collections import namedtuple
# from tomlib import loads
from browser import document as doc, html as ht
NO_DICT = {}

HTML = namedtuple('HTML', "n d h a z s p x r u l y i k m")

_ = dict(
    n=ht.NAV, d=ht.DIV, h=ht.H1, a=ht.A, z=ht.SECTION, s=ht.SPAN, p=ht.P, x=ht.H2, r=ht.HR, u=ht.UL,
    l=ht.LI, y=ht.H4, i=ht.IMG, k=ht.LINK, m=ht.META, )


class TemplateBuilder(HTML):
    def __new__(cls):
        self = super(TemplateBuilder, cls).__new__(cls,
            n=ht.NAV, d=ht.DIV, h=ht.H1, a=ht.A, z=ht.SECTION, s=ht.SPAN, p=ht.P, x=ht.H2, r=ht.HR, u=ht.UL, # noqa
            l=ht.LI, y=ht.H4, i=ht.IMG, k=ht.LINK, m=ht.META, ) # noqa
        return self

    def __init__(self):
        super().__init__() # noqa
        self.content = None
        self.names = {}

    def parse_template(self, data):
        tags = self._asdict()
        code = [tags[tag[1]](**kw) for tag, kw in data.items()]
        return code

    def get_names(self, td):
        return td if td not in self.names else self.names.get(td, [])

    def list_comprehension(self, td):
        return [td.xp(self.get_names(data)) for data in td.col]

    def build(self, data: dict=None):
        h = self
        data = self.parse_template(data or {})

        # prefix = "https://cdnjs.cloudflare.com/ajax/libs/"
        # libs = "bulma/1.0.4/css/bulma.min.css font-awesome/7.0.0/css/all.min.css".split()
        # tgs = [h.k(rel="stylesheet", href=prefix + tg) for tg in libs]
        tgs = [h.k(rel="stylesheet", href="/css/labase.css")]
        tgs += [h.k(rel="shortcut icon", href="/_media/suucurijuba.png", type="image/x-icon")]+data
        # tgs += [h.m(charset="utf-8"), ht.META(name="viewport", content="width=device-width, initial-scale=1")]
        _ = [doc.head <= tg for tg in tgs]
        doc.title = "LABASE"
        return tgs


def main():
    TemplateBuilder().build()
