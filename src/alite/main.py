#!/usr/bin/env python
# noinspection GrazieInspection
"""Main Page Builder.

Classes neste módulo:
    - :py:funct: message NPC Player.
    - :py:class:`PageBuilder` handle page creation.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>
.. tip:: *Milestone* ⛲ 🛠️ ⭐Golden Penta (08/17)
.. code-block:: python

Changelog
---------
.. versionadded::    25.08
   |br| Initial builder implementation (17).

|   **Open Source Notification:** This file is part of open source program **Alite**
|   **Copyright © 2025  Carlo Oliveira** <carlo@nce.ufrj.br>,
"""
from collections import namedtuple
from tomlib import loads
from browser import document as doc, html as ht

CF = "https://cdnjs.cloudflare.com/ajax/libs/"
lb = "bulma/1.0.4/css/bulma.min.css font-awesome/7.0.0/css/all.min.css".split()
TOML = '''
title = "Alite"
menu = "#sobre Sobre|#participantes Equipe|#projetos Projetos|#publica Publicações|#contato Contato"
prefix = "https://cdnjs.cloudflare.com/ajax/libs/"
libs = "bulma/1.0.4/css/bulma.min.css font-awesome/7.0.0/css/all.min.css"
[builder.nav]
ha0 = {aria_expanded="false", aria_label="menu", Class="navbar-burger", data_target="navbarBasicExample", role="button"}
lc0 = {__0={__ha0="label", Class="navbar-item", href="ref"}, _b="label ref", _c="menu"}
hh0 = {__ha0={__0="title", Class="navbar-item", style="color: var(--coral);"}, Class="title is-4"}
hd0 = {__0=["hh0", "ha0"], Class="navbar-brand"}
hd1 = {__hd0={__0="ha0", Class="navbar-end"}, Class="navbar-menu", id="navbarBasicExample"}
#cont = t.d([brand, menu], Class="container")
hd2 = {__0=["hd0", "menu"], Class="container"}
#return t.n(cont, Class="navbar is-fixed-top", role="navigation", aria_label="main navigation")
hn0__ = {__0="hd2", Class="navbar is-fixed-top", role="navigation", aria_label="main navigation"}

[sobre.card__0]
title = "Formação"
caption = """
Capacitação de alunos em diferentes níveis acadêmicos, desde a extensão até a pós-graduação,
preparando-os para os desafios do mercado de tecnologia educacional."""
icon = "fa-solid fa-person-chalkboard"
[sobre.card__1]
title = "Games Educativos"
caption = """
Desenvolvimento de jogos inovadores que transformam o aprendizado em uma experiência envolvente e eficaz,
utilizando técnicas de gamificação e design instrucional."""
icon = "fa-solid fa-gamepad"
[sobre.card__2]
title = "Neuropedagogia"
caption = """
Análise de dados cognitivos para entender e otimizar o processo de aprendizagem,
criando soluções adaptativas que se ajustam ao ritmo de cada estudante."""
icon = "fa-solid fa-brain"
'''


class Template:
    def __init__(self, ):
        self.names = {}
        self.template = namedtuple("template", "n d h a z s p x r u l y")(
            n=ht.NAV, d=ht.DIV, h=ht.H1, a=ht.A, z=ht.SECTION, s=ht.SPAN, p=ht.P, x=ht.H2, r=ht.HR, u=ht.UL,
            l=ht.LI, y=ht.H4)

    def load(self, raiz, esquema):
        def register_names(dicionario):
            for k, v in dicionario.items():
                if isinstance(v, str):
                    pass
                    # self.names[k] = v
                elif isinstance(v, dict):
                    if k[0] == "h" and k[-1] in "0123456789_":
                        self.names[k] = v
                    register_names(v)
        code = esquema[raiz]
        [self.names.update({key: {}}) for key in code.keys()]
        register_names(code)
        print("name", self.names)

    def nav(self, title, menus):
        t = self.template
        a = t.a(aria_expanded="false", aria_label="menu", Class="navbar-burger",
                data_target="navbarBasicExample", role="button")
        m = [t.a(label, Class="navbar-item", href=ref) for ref, label in menus]
        h = t.h(t.a(title, Class="navbar-item", style="color: var(--coral);"), Class="title is-4")
        brand = t.d([h, a], Class="navbar-brand")
        # brand = t.d(t.d([h, a], Class="navbar-brand"))
        menu = t.d(t.d(m, Class="navbar-end"), Class="navbar-menu", id="navbarBasicExample")
        cont = t.d([brand, menu], Class="container")
        return t.n(cont, Class="navbar is-fixed-top", role="navigation", aria_label="main navigation")

    def hero(self, title, menus):
        title = "LABASE"
        name = "Laboratório de Automação de Sistemas Educacionais"
        motto = ('Criando ferramentas computacionais para uma educação mais eficiente, '
                 '<span class="highlight">humanizada</span> e <span class="highlight">adaptativa</span>')
        bota = "#projetos&&Nossos Projetos|#contato& btn-outline&Entre em Contato".split("|")
        bota = [bb.split("&") for bb in bota]
        t = self.template
        st = "background: rgba(178, 34, 34, 0.2); color: var(--coral); border: 1px solid var(--firebrick);"
        s = t.s("Inovação em Educação Tecnológica", Class="tag is-medium", style=st)
        dv = t.d(s, Class="mb-5")
        h1 = t.h(title, Class="title is-1 mb-4 glow-text", style="color: var(--coral);")
        h2 = t.x(name, Class="subtitle is-4 mb-5", style="color: var(--goldenrod);")
        p = t.p(motto, Class="is-size-5 mb-6", style="max-width: 800px; margin: 0 auto;")
        d2 = t.d([t.a(ll, href=hf, Class="btn" + cl) for hf, cl, ll in bota], Class="buttons is-centered mt-5")

        return t.z(t.d([dv, h1, h2, p, d2], Class="container has-text-centered"), Class="hero")

    def par(self, tx):
        return [self.template.p(txt) for txt in tx]

    def col(self, w=4, cl="has-text-centered", title="", caption="", icon=""):
        t = self.template
        ic = t.d("&nbsp;", Class=f"feature-icon {icon}")
        st = t.y(title, Class="title is-4 mb-3", style="color: var(--coral)")
        return t.d(t.d([ic, st, t.p(caption)], Class=cl), Class=f"column is-{w}")

    def sobre(self, itens: dict = None):
        t = self.template
        x = t.x("Sobre o LABASE", Class="title is-2 section-title has-text-centered")
        c2 = t.d([], Class="columns is-vcentered")
        c3 = t.d([self.col(**col) for col in itens.values()], Class="columns is-multiline mt-6")
        # c3 = t.d([self.col(title=tt, sub=sb) for tt, sb in itens], Class="columns is-multiline mt-6")
        return t.z(t.d([x, c2, t.r(Class="divider"), c3], Class="container"), Class=f"section", id="sobre")


class PageBuilder:
    """Page Builder."""

    def __init__(self):
        """Constructor."""
        with open("alite/labase.toml", "rb") as f:
            self.config = cf = loads(f.read().decode("utf-8"))
        prefix = cf["prefix"]
        libs = cf["libs"].split()
        tgs = [ht.LINK(rel="stylesheet", href=prefix + tg) for tg in libs]
        tgs += [ht.LINK(rel="stylesheet", href="/css/labase.css")]
        tgs += [ht.LINK(rel="shortcut icon", href="/_media/suucurijuba.png", type="image/x-icon")]
        tgs += [ht.META(charset="utf-8"), ht.META(name="viewport", content="width=device-width, initial-scale=1")]
        _ = [doc.head <= tg for tg in tgs]
        self.body = doc.body
        self.doc = doc
        doc.title = cf["title"]
        self.title = cf["title"]
        menu = cf["menu"]
        self.menus = [tp.split() for tp in menu.split("|")]

    def build(self, page=None):
        page = page or self
        t = Template()
        t.load("builder", self.config)
        _ = self.body <= t.nav(page.title, page.menus)
        _ = self.body <= t.hero(page.title, page.menus)
        _ = self.body <= t.sobre(self.config["sobre"])
        return self


if __name__ == "__main__":
    builder = PageBuilder().build()

'''
<section class="section" id="sobre">
    <div class="container">
        <h2 class="title is-2 section-title has-text-centered">Sobre o LABASE</h2>

        <div class="columns is-vcentered">
            <div class="column is-7">
                <div class="content is-medium">
                    <p>O <span class="highlight">LABASE</span> se dedica &agrave; cria&ccedil;&atilde;o de ferramentas
                        computacionais para uma educa&ccedil;&atilde;o mais eficiente, humanizada e adaptativa.</p>

                    <p>Com foco em metodologias &aacute;geis, programa&ccedil;&atilde;o orientada a objetos,
                        neuropedagogia computacional e games inteligentes, o laborat&oacute;rio promove inova&ccedil;&atilde;o
                        did&aacute;tica em ambientes de ensino e pesquisa.</p>

                    <p>Atuamos na forma&ccedil;&atilde;o de alunos da extens&atilde;o, gradua&ccedil;&atilde;o e p&oacute;s-gradua&ccedil;&atilde;o,
                        com projetos que aliam desenvolvimento de jogos educacionais e an&aacute;lise de dados sobre
                        aprendizagem e cogni&ccedil;&atilde;o.</p>
                </div>
            </div>

            <div class="column is-5">
                <div class="box" data-darkreader-inline-border-left-short=""
                     style="border-left: 4px solid var(--coral); --darkreader-inline-border-left-short: 4px solid var(--darkreader-border--coral);">
                    <h3 class="title is-4 mb-4" data-darkreader-inline-color=""
                        style="color: var(--goldenrod); --darkreader-inline-color: var(--darkreader-text--goldenrod, var(--darkreader-text-000000, #e8e6e3));">
                        Nossa Miss&atilde;o</h3>

                    <p class="mb-5">Promover a inova&ccedil;&atilde;o educacional atrav&eacute;s da tecnologia,
                        desenvolvendo solu&ccedil;&otilde;es que tornem o processo de aprendizagem mais eficiente, acess&iacute;vel
                        e adaptado &agrave;s necessidades individuais dos estudantes.</p>

                    <h3 class="title is-4 mb-4" data-darkreader-inline-color=""
                        style="color: var(--goldenrod); --darkreader-inline-color: var(--darkreader-text--goldenrod, var(--darkreader-text-000000, #e8e6e3));">
                        &Aacute;reas de Foco</h3>

                    <ul class="mb-0">
                        <li>Metodologias &Aacute;geis em Educa&ccedil;&atilde;o</li>
                        <li>Programa&ccedil;&atilde;o Orientada a Objetos</li>
                        <li>Neuropedagogia Computacional</li>
                        <li>Desenvolvimento de Games Inteligentes</li>
                        <li>An&aacute;lise de Dados Educacionais</li>
                    </ul>
                </div>
            </div>
        </div>

        <hr class="divider"/>
        <div class="columns is-multiline mt-6">
            <div class="column is-4">
                <div class="has-text-centered">
                    <div class="feature-icon">&nbsp;</div>

                    <h4 class="title is-4 mb-3" data-darkreader-inline-color=""
                        style="color: var(--coral); --darkreader-inline-color: var(--darkreader-text--coral, var(--darkreader-text-000000, #e8e6e3));">
                        Forma&ccedil;&atilde;o</h4>

                    <p>Capacita&ccedil;&atilde;o de alunos em diferentes n&iacute;veis acad&ecirc;micos, desde a extens&atilde;o
                        at&eacute; a p&oacute;s-gradua&ccedil;&atilde;o, preparando-os para os desafios do mercado de
                        tecnologia educacional.</p>
                </div>
            </div>

            <div class="column is-4">
                <div class="has-text-centered">
                    <div class="feature-icon">&nbsp;</div>

                    <h4 class="title is-4 mb-3" data-darkreader-inline-color=""
                        style="color: var(--coral); --darkreader-inline-color: var(--darkreader-text--coral, var(--darkreader-text-000000, #e8e6e3));">
                        Games Educativos</h4>

                    <p>Desenvolvimento de jogos inovadores que transformam o aprendizado em uma experi&ecirc;ncia
                        envolvente e eficaz, utilizando t&eacute;cnicas de gamifica&ccedil;&atilde;o e design
                        instrucional.</p>
                </div>
            </div>

            <div class="column is-4">
                <div class="has-text-centered">
                    <div class="feature-icon">&nbsp;</div>

                    <h4 class="title is-4 mb-3" data-darkreader-inline-color=""
                        style="color: var(--coral); --darkreader-inline-color: var(--darkreader-text--coral, var(--darkreader-text-000000, #e8e6e3));">
                        Neuropedagogia</h4>

                    <p>An&aacute;lise de dados cognitivos para entender e otimizar o processo de aprendizagem, criando
                        solu&ccedil;&otilde;es adaptativas que se ajustam ao ritmo de cada estudante.</p>
                </div>
            </div>
        </div>
    </div>
</section>
'''
