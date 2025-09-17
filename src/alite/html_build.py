#!/usr/bin/env python
# noinspection GrazieInspection
"""Html Page Builder.

Reads a Template builder an fill in content data.

Classes neste módulo:
    - :py:class:`TemplateBuilder` Html calls and template code builder.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>
.. tip:: *Milestone* 🚧 ⛲ 🛠️ Golden Penta ⭐ 25.08 (21)

Changelog
---------
.. versionadded::    25.08
   |br| Initial builder implementation (21).
   |br| added list comprehension (23).
   |br| added read and post to head + body hero (24).
   |br| add custom macro (30).

|   **Open Source Notification:** This file is part of open source program **Alite**
|   **Copyright © 2025  Carlo Oliveira** <carlo@nce.ufrj.br>,
"""
from collections import namedtuple
from browser import document as doc, html as ht

NO_DICT = {}
NO_E = "<-- {} -->"


class TemplateBuilder:
    """A builder class for creating HTML templates dynamically.

    This class provides methods to parse template data and generate HTML elements
    using Brython's HTML components. It supports basic HTML elements and list comprehensions
    for generating repeated elements.

    Attributes
    ----------
    HTML : namedtuple
        A collection of HTML element constructors for common tags.
    names : dict
        A dictionary storing named elements for reference during template parsing.

    Examples
    --------
    >>> builder = TemplateBuilder()
    >>> template_data = {"h1_0": {"text": "Hello World"}}
    >>> elements = builder.build(template_data)
    """
    MACRO = {}

    @staticmethod
    def title(kwargs):
        doc.title = kwargs
        return NO_E.format(kwargs)

    @staticmethod
    def head(*kwargs):
        return [doc.head <= ents for ents in kwargs]

    @staticmethod
    def body(*kwargs):
        return [doc.body <= ents for ents in kwargs]

    @staticmethod
    def macro(*kwargs):

        return [TemplateBuilder.MACRO.update(**kw) for kw in kwargs if isinstance(kw, dict)]
        # return [TemplateBuilder.MACRO.update(**kw) for kw in kwargs]

    HTML = namedtuple('HTML', "n d h a z s p x r u l y i k m H B M T")(
        n=ht.NAV, d=ht.DIV, h=ht.H1, a=ht.A, z=ht.SECTION, s=ht.SPAN, p=ht.P, x=ht.H2, r=ht.HR, u=ht.UL,
        l=ht.LI, y=ht.H4, i=ht.IMG, k=ht.LINK, m=ht.META, H=head, B=body, M=macro, T=title)

    def __init__(self):
        """Initialize the TemplateBuilder with HTML element references and an empty names, macros dictionary."""
        super().__init__()  # noqa
        self.t = TemplateBuilder.HTML
        self.d = TemplateBuilder.HTML._asdict()
        self.names = {}
        self.macros = {}
        self.fix = False
        tb = self

        class WebElement:
            def __init__(self, tg):
                def warned(t, k, y):
                    return NO_E.format(f"@@ {tb.MACRO} t:{t}, k:{y}, {k}, IS no macro @@")

                def make_(tg_, **kw):
                    xkw = kw.copy()
                    tb.MACRO[f"m-{tg_[1:-1]}"] = tb.macro(**kw or dict(Class="navbar-item"))
                    # self.MACRO[f"m-{tg_[1:-1]}"] = self.macro(d, **kw or dict(Class="navbar-item"))
                    _m = tb.MACRO[f"m-{tg_[1:-1]}"]
                    print(f"@@->case 'n', {tg_}, kw, {xkw},tag {_m.tag},dom_node {_m.dom_node} a: {_m.arguments}")
                    return [NO_E.format(f"define macro m-{tg_[1:-1]}")]

                def listing(kw, *_):
                    print(f"@@->listing , kw, {kw},tag")
                    tb.MACRO["m-c"].go(kw["l_y"]) if "l_y" in kw else NO_E.format(" is no lc")
                    return [NO_E.format(f"{tg, kw} is no lc")]

                self.tg = self.fix = tg
                m = f"m-{tg[1:-1]}"
                _ = NO_E.format(f"@@ {tb.MACRO} IS no macro @@")

                self.kind = dict(
                    h=self.html_tag, d=self.html_tag,
                    e=lambda tg_, **kw: [warned(tg_, kw, "e")],
                    m=lambda tg_, m_=m, **kw: [tb.MACRO[m_].go(**kw) if m_ in tb.MACRO else warned(tg_, kw, "m "+m_)],
                    x=make_,
                    n=lambda tg_, m_=m, **kw: [tb.MACRO.update({m_: tb.macro(**kw)})] or warned(tg_, kw, "n"),
                    l=listing,
                    w=lambda tg_, kw: [tb.MACRO["m-c"].go(kw["l_y"]) if "l_y" in kw else warned(tg_, kw, "l")],
                )

            def parse(self, tg, **kwargs):
                # tg = self.tg
                print("parse", tg, self.kind.get(tg[0], self.kind["e"]), **kwargs)  # if "m" in tg else None
                if (not isinstance(tg, str)) or (len(tg) < 3):
                    return [NO_E.format(tg + "beginner")]
                return self.kind.get(tg[0], self.kind["e"])(tg, **kwargs)

            def process_macro(self, macro):
                """Process a macro definition."""
                arg = macro.pop("__0", False) if isinstance(macro, dict) else macro
                # arg = macro.get("__0", False)
                match str(type(arg)):
                    case "<class 'bool'>":
                        return False
                    case "<class 'str'>":
                        return tb.macros.get(arg, arg)
                    case "---<class 'list'>":
                        return [NO_E.format(str(arg) + " is no list")]  # [self.macro_with_list("x", **macro)]
                    case "<class 'dict'>" | "<class 'tomlib.DynamicInlineTableDict'>" | "<class 'list'>":
                        return [self.parse(k, **v) for k, v in arg.items()]
                    case _:
                        print("process_macro", arg, type(arg))
                        return [NO_E.format(str(arg) + " is no macro")]

            def html_tag(self, tg, **kw):
                tags = tb.t._asdict()

                h_t = self.html_tag
                if tg[1] not in tags:

                    print("@@@ - html_tag", tg, kw)
                    return self.parse(tg, **kw)
                    # return [kw]
                elif tg[1] in "HBM":
                    def go_parse(tg_, kw_):
                        return h_t(tg_, **kw_) if isinstance(kw_, dict) else h_t(tg_, **dict(__0=kw_))

                    self.fix = tg
                    _parse = [_tg for tag, arg in kw.items()
                              if (tag[2] not in "_") and (isinstance(arg, dict) or isinstance(arg, list))
                              for _tg in go_parse(tag, arg)]
                    coded = tags[tg[1]](*_parse)
                    tb.macros[f"{tg}_{self.fix}_" if self.fix else tg] = coded if coded else NO_E.format(
                        tg + str(kw) + " is no coded")
                    return [coded]
                arg = self.process_macro(kw)
                try:
                    coded = tags[tg[1]](**kw) if (arg is False) or isinstance(arg, bool) else tags[tg[1]](arg, **kw)
                except Exception as mx:
                    print(mx, tg, kw, arg)
                    _ = NO_E.format(tg + str(kw) + " is empty coded")  # tags[tg[1]](**kw)
                    coded = self.process_macro({tg: kw})  # tags[tg[1]](**kw)
                msg = NO_E.format(tg + str(kw) + " is empty coded")
                tb.macros[f"{tg}_{self.fix}_" if self.fix else tg] = coded if coded else msg
                return [coded]

        class MacroGen:
            def __init__(self, _0=False, _node_=None, _tag_="a", _arg_=False, _is_list_=False, **kwargs):
                self._sub_args, kwargs = [k[2:] for k in kwargs.values() if k.startswith("__")], {
                    k: v for k, v in kwargs.items() if not k.startswith("__")}
                self.arguments = _0
                self.dom_node = _node_ or doc.body
                self.tag, self.arg = _tag_, _arg_
                self.default = {k: v for k, v in kwargs.items() if k not in self._sub_args}
                # x, y = "l", self.attrs['l-y']
                self.go = self.list_go if _is_list_ else self.cmd_go
                print(f"MacroGen(self, _0=({_0}), **kwargs: {kwargs}) default: {self.default}",
                      f"arg=({self.arguments}), self._sub_args: {self._sub_args} tg ag = {self.tag, self.arg}")

            def cmd_go(self, __0=False, **kwargs):
                sub_args = {k: v for k, v in kwargs.items() if k in self._sub_args}
                kwargs = {k: v for k, v in kwargs.items() if k not in self._sub_args}
                __0 = [tb.MACRO[self.arguments].go(**sub_args)] if self.arguments else (__0 or kwargs.pop("__0", False))
                kw_list = dict(list(self.default.items()) + list(kwargs.items()))
                print(f"cmd_go(self, __0=({__0}), **kwargs: {kwargs}), kw_list: {kw_list}) sub_args:{sub_args} 0:{__0}",
                      f"arg=({self.arguments}), self._sub_args: {self._sub_args}  default: {self.default}")
                return tb.d[self.tag](__0, **kw_list) if __0 else tb.d[self.tag](**kw_list)
                # _ = self.dom_node <= (tb.d[self.tag](__0, **kw_list) if __0 else tb.d[self.tag](**kw_list))
                # return NO_E.format("MG")

            def list_go(self, y=(), **_):
                print(f"MacroGen dom:{self.dom_node} t-a-k-l", self.tag, self.arg, y)
                return [self.cmd_go(elt.pop("__0", False), **elt) for elt in y]

        self.macro = MacroGen
        self.web = WebElement

        class WebList:
            def __init__(self, dom_node=None, macro_node=None):
                self.dom_node = dom_node or doc.head
                self.macro = macro_node or dict(rel="stylesheet")
                # x, y = "l", self.attrs['l-y']

            def go(self, y):
                def add(els):
                    # return {k: v for k, v in list(self.macro.items()) + [els]}
                    return {k: v for k, v in list(self.macro.items()) + list(els.items())}

                print(y)
                # _ = [self.dom_node <= tb.t.k(add(y))]
                _ = [self.dom_node <= tb.t.k(**add(elt)) for elt in y]

        self.MACRO["m-c"] = WebList()
        self.list = WebList

    def parse_template(self, data, fix=False):  # noqa
        """Parse template data and generate corresponding HTML elements.

        This method processes a dictionary of template specifications and converts them
        into HTML elements. It handles both single elements and list comprehensions.

        Parameters
        ----------
        data : dict
            A dictionary where keys represent element identifiers and values are
            dictionaries of attributes for those elements.
        fix : str, optional
            A suffix appended to each macro name.

        Returns
        -------
        list
            A list of generated HTML elements.

        Raises
        ------
        ValueError
            If an element identifier format is not recognized.
        """

        def process_macro(macro):
            """Process a macro definition."""
            arg = macro.pop("__0", False) if isinstance(macro, dict) else macro
            # arg = macro.get("__0", False)
            match str(type(arg)):
                case "<class 'bool'>":
                    return False
                case "<class 'str'>":
                    return self.macros.get(arg, arg)
                case "---<class 'list'>":
                    return [NO_E.format(str(arg) + " is no list")]  # [self.macro_with_list("x", **macro)]
                case "<class 'dict'>" | "<class 'tomlib.DynamicInlineTableDict'>" | "<class 'list'>":
                    return [_do_parse(k, **v) for k, v in arg.items()]
                case _:
                    print("process_macro", arg, type(arg))
                    return [NO_E.format(str(arg) + " is no macro")]

        def _do_parse(tg, **kw):
            print(tg, **kw) if "m" in tg else None
            if (not isinstance(tg, str)) or (len(tg) < 3):
                return [NO_E.format(tg + "begin")]
            match tg[0]:
                case 'm':  # return macro execution
                    print("case 'm'", tg, "case 'list'", kw, )
                    # print(kw["l_y"]if "l_y" in kw else "l_y")
                    m = f"m-{tg[1:-1]}"
                    warn = NO_E.format(f"@@ {self.MACRO} IS no macro @@")
                    return [self.MACRO[m].go(**kw) if m in self.MACRO else warn]
                    # return [self.MACRO[m].go(kw.pop("__0", False), **kw) if m in self.MACRO else warn]
                    # return [NO_E.format(f"{m, kw} is no parse macro")]
                case 'n':  # define a new macro
                    xkw = kw.copy()
                    self.MACRO[f"m-{tg[1:-1]}"] = self.macro(**kw or dict(Class="navbar-item"))
                    # self.MACRO[f"m-{tg[1:-1]}"] = self.macro(d, **kw or dict(Class="navbar-item"))
                    m = self.MACRO[f"m-{tg[1:-1]}"]
                    print(f"@@->case 'n', {tg}, kw, {xkw},tag {m.tag},dom_node {m.dom_node} a: {m.arguments}")
                    return [NO_E.format(f"define macro m-{tg[1:-1]}")]
                case 'h' | 'd':
                    if tg[1] not in tags:
                        return [kw]
                    elif tg[1] in "HBM":
                        def go_parse(tg_, kw_):
                            return _do_parse(tg_, **kw_) if isinstance(kw_, dict) else _do_parse(tg_, **dict(__0=kw_))
                        self.fix = tg
                        _parse = [_tg for tag, arg in kw.items()
                                  if (tag[2] not in "_") and (isinstance(arg, dict) or isinstance(arg, list))
                                  for _tg in go_parse(tag, arg)]
                        coded = tags[tg[1]](*_parse)
                        self.macros[f"{tg}_{self.fix}_" if self.fix else tg] = coded if coded else NO_E.format(
                            tg + str(kw) + " is no coded")
                        return [coded]
                    # arg = kw.pop("__0", False)
                    # arg = [self.macros.get(a, a) for a in arg] if isinstance(arg, list) else self.macros.get(arg, arg)
                    # arg = arg if isinstance(arg, list) else [arg]
                    arg = process_macro(kw)
                    try:
                        coded = tags[tg[1]](**kw) if (arg is False) or isinstance(arg, bool) else tags[tg[1]](arg, **kw)
                    except Exception as mx:
                        print(mx)
                        coded = False  # tags[tg[1]](**kw)
                    msg = NO_E.format(tg + str(kw) + " is empty coded")
                    self.macros[f"{tg}_{self.fix}_" if self.fix else tg] = coded if coded else msg
                    return [coded]
                case 'l':  # return self.list_comprehension(**kw)
                    # print("case 'l'", tg, kw, "case 'list'", self.list_comprehension(**kw))
                    # print(kw["l_y"]if "l_y" in kw else "l_y")
                    self.MACRO["m-c"].go(kw["l_y"]) if "l_y" in kw else NO_E.format(" is no lc")
                    return [NO_E.format(f"{tg, kw} is no lc")]
                case _:
                    return [NO_E.format(tg + "end")]

        tags = self.t._asdict()
        # print("data", data)
        # [print("t:", type(kw), kw, end=",") for t, grp in data.items() for tag, kw in grp.items() if "m" in tag]

        code = [entity for tag, kw in data.items() for entity in self.web(tag).parse(tag, **kw)]
        # code = [entity for tag, kw in data.items() for entity in _do_parse(tag, **kw)]
        # print("code", code)
        return code

    def build(self, data: dict = None):
        """Build and render the complete HTML template.

        This is the main entry point for generating HTML from template data.
        It registers all named elements, parses the template, and attaches
        the resulting elements to the document head.

        Parameters
        ----------
        data : dict, optional
            A dictionary containing the template specification. If None,
            an empty template is generated.

        Returns
        -------
        list
            A list of all generated HTML elements.
        """

        def register_names(fix, dicionario):
            for k, v in dicionario.items():
                if k[0] in "hd" and k[-1] in "0123456789_":
                    self.names[f"{k}_{fix}_"] = v
                register_names(f"{k}", v) if isinstance(v, dict) else None

        # print("build_data", data)

        register_names("", data) if data is not None else None
        data = self.parse_template(data or {})
        # print("Building HTML elements...", self.macros, "@@dataXX", data)
        # doc.title = "LABASE"
        return data


def _populate_html():
    """Create template data for common HTML head elements.

    This function generates a template specification for common HTML head
    elements including CSS stylesheets and favicon.
    https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.0/css/all.min.css


    Returns
    -------
    dict
        A dictionary containing template specifications for head elements.
    """
    # libs = "bulma/1.0.4/css/bulma.min.css font-awesome/7.0.0/css/all.min.css /css/labase.css".split()
    # dt = [dict(href=lb) for lb in libs]
    # di = dict(rel="shortcut icon", href="/_media/suucurijuba.png", type="image/x-icon")
    # tg = dict(hk_0=dict(rel="stylesheet"), lk0=dict(l_x="hk_0_dH0_", l_y=dt), hk1=di)
    # _ = dict(dH0=tg, dT0={"__0": "LABASE"}, dB0=dict(hh0=dict(__0="HALO", alt="HALO")))
    from tomlib import loads
    with open("alite/labase.toml", "rb") as f:
        xt = """
[dM0]
nwi0 = {_tag_="i", width="26", height="28"}
nwb0 = {_0="m-wi", src="__src", alt="__alt", _tag_="a", Class="navbar-item"}
nwm0 = {_tag_="a", _arg_=true, _is_list_=true, Class="navbar-item"}
mwm0 = [{__0="Sobre", href="#sobre"}, {__0="Projetos", href="#projetos"}]
nwmm0 = {_tag_="a", _arg_=true, _is_list_=false, Class="navbar-item"}
# mmm0 = {__0="Equipe", href="#Equipe"}
# dB0.hd9 = {__0={mwmm0 = {__0="Equipe", href="#Equipe"}}, alt="HALO"}
dB0.hd8 = {__0={mwb0 = {src="/_media/suucurijuba.png", alt="labase", href="#root"}}}
dH0.hkl0 = {rel="stylesheet", href="/css/bulma.min.css"}
dH0.hkl1 = {rel="stylesheet", href="/css/labase.css"}

        """
        cf = loads(f.read().decode("utf-8") + xt)
    # cf = loads(file)
    # print(cf)
    return cf


def main():
    """Main function to demonstrate the TemplateBuilder functionality.

    This function creates a TemplateBuilder instance, populates it with
    common HTML elements, and builds the template.
    """
    TemplateBuilder().build(_populate_html())


if __name__ == "__main__":
    main()
