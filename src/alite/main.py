#!/usr/bin/env python
# noinspection GrazieInspection
"""Main Page Builder.

Classes neste módulo:
    - :py:class:`Template` Html calls and template code builder.
    - :py:class:`PageBuilder` builds a page from TOML description.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>
.. tip:: *Milestone* 🚧 ⛲ 🛠️ Golden Penta ⭐ 25.08 (17)

Changelog
---------
.. versionadded::    25.08
   |br| Initial builder implementation (17).
   |br| code from toml (18).
   |br| import from html_build (23).

|   **Open Source Notification:** This file is part of open source program **Alite**
|   **Copyright © 2025  Carlo Oliveira** <carlo@nce.ufrj.br>,
"""
from collections import namedtuple
from tomlib import loads
from browser import document as doc, html as ht


class Template:
    """Html calls and template code builder.

    """
    def __init__(self):
        self.names, self.macros = {}, {}
        self.tags = g = "n d h a z s p x r u l y i"
        self.template = namedtuple("template", g)(
            n=ht.NAV, d=ht.DIV, h=ht.H1, a=ht.A, z=ht.SECTION, s=ht.SPAN, p=ht.P, x=ht.H2, r=ht.HR, u=ht.UL,
            l=ht.LI, y=ht.H4, i=ht.IMG)

    def exec(self, macro):
        tags = self.template._asdict()
        # tags_ = {k: no_tag(k) for k in self.tags}
        args = [f"__h{tg}{ix}" for tg in tags for ix in "0123456789"]
        def list_comprehension(dicionario):
            """l_0 = {__0={__ha0="label", Class="navbar-item", href="ref"}, _b="label ref", _c="menu"}
            """
            stat = dicionario.get("__0", {})


        def get_name(nome):
            if nome in self.names:
                return self.names[nome]
            else:
                return nome

        def make_code(nome, dicionario):
            nome = nome[2:] if nome.startswith("__") else nome
            if not isinstance(dicionario, dict):
                print("not isinstance(dicionario, dict)", dicionario)
                return dicionario  # self.template.d()
            _tags = [make_code(tg[2:4], arg) for tg, arg in dicionario.items() if tg[0:4] in args]
            _args = dicionario.pop("__0", None) or _tags
            _tag = nome[6]
            _ = [dicionario.pop(tg, None) for tg in args if "__" in tg]
            if _tag not in tags:
                print("code_tag_tags_tag not in tags", _tag, _args)
                return self.template.d()
            if _args:
                _args = [get_name(ar) for ar in _args] if isinstance(_args, list) else get_name(_args)
                print("code_make_code_tags", nome, "_args", _args, "dict", dicionario, "macro", macro)
                _code = tags[_tag](_args, **dicionario)
            else:
                _code = tags[_tag](**dicionario)
            self.names[f"{nome}"] = _code
            return _code

        code = {name: make_code(name, _macro) for name, _macro in self.names.items()}  # if name[-1] != "_"}
        # for name, macro in self.names.items():
        #     code[name] = (name, macro)
        main = [name for name in code.keys() if name.endswith("__")][0]
        [print("code", n, code) for n, code in code.items()]
        print("main", main, code[main])
        return code[main]

    def load(self, raiz, esquema):
        def register_names(fix, dicionario):
            for k, v in dicionario.items():
                if isinstance(v, str):
                    pass
                    # self.names[k] = v
                elif isinstance(v, dict):
                    if k[0] == "h" and k[-1] in "0123456789_":
                        self.names[f"{fix}_{k}"] = v
                    register_names(f"{fix}_{k}", v)

        code = esquema[raiz]
        [self.macros.update({key: {}}) for key in code.keys()]
        register_names("", code)
        print("macro", self.macros, "name", self.names)

    def nav(self, title, menus):
        t = self.template
        # h = t.h(t.a(title, Class="navbar-item", style="color: var(--coral);"), Class="title is-4")
        a = t.a(aria_expanded="false", aria_label="menu", Class="navbar-burger",
                data_target="navbarBasicExample", role="button")
        m = [t.a(label, Class="navbar-item", href=ref) for ref, label in menus]
        lg = t.a(t.i(src="/_media/suucurijuba.png",alt="LABASE", width="26", height="28"), Class="navbar-item", href="/")
        start = t.d(t.a("LABASE", Class="navbar-item", style="color: var(--coral);", href="/"), Class="navbar-start")
        brand = t.d([lg, start, a], Class="navbar-brand")
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
        self.template = Template()
        self.body = doc.body
        self.doc = doc
        doc.title = cf["title"]
        self.title = cf["title"]
        menu = cf["menu"]
        self.menus = [tp.split() for tp in menu.split("|")]

    def build(self, page=None):
        page = page or self
        t = self.template
        t.load("builder", self.config)
        t.names["menu"] = [t.template.a(label, Class="navbar-item", href=ref) for ref, label in self.menus]

        print('t.exec("nav")', t.exec("nav"))
        _ = self.body <= t.exec("nav")
        # _ = self.body <= t.nav(page.title, page.menus)
        _ = self.body <= t.hero(page.title, page.menus)
        _ = self.body <= t.sobre(self.config["sobre"])
        print("macro", t.macros, "name", t.names)

        return self


if __name__ == "__main__":
    import html_build as htb
    htb.main()

    # builder = PageBuilder().build()
    # builder = htb.TemplateBuilder()
    # builder.build()

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
