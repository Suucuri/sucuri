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
        return [TemplateBuilder.MACRO.update(**kw) for kw in kwargs]

    HTML = namedtuple('HTML', "n d h a z s p x r u l y i k m H B M T")(
        n=ht.NAV, d=ht.DIV, h=ht.H1, a=ht.A, z=ht.SECTION, s=ht.SPAN, p=ht.P, x=ht.H2, r=ht.HR, u=ht.UL,
        l=ht.LI, y=ht.H4, i=ht.IMG, k=ht.LINK, m=ht.META, H=head, B=body, M=body, T=title)

    def __init__(self):
        """Initialize the TemplateBuilder with HTML element references and an empty names, macros dictionary."""
        super().__init__()  # noqa
        self.t = TemplateBuilder.HTML
        self.names = {}
        self.macros = {}
        self.fix = False

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
            match str(type(arg)):
                case "<class 'bool'>":
                    return False
                case "<class 'str'>":
                    return self.macros.get(arg, arg)
                case "<class 'list'>":
                    return [process_macro(a) for a in arg]
                    # return [self.macros.get(a, a) for a in arg]
                case "<class 'dict'>" | "<class 'tomlib.DynamicInlineTableDict'>":
                    return [do_parse(k, **v) for k, v in arg.items()]
                case _:
                    print("process_macro", arg, type(arg))
                    return [NO_E.format(str(arg) + " is no macro")]

        def do_parse(tg, **kw):
            if (not isinstance(tg, str)) or (len(tg) < 3):
                return [NO_E.format(tg + "begin")]
            match tg[0]:
                case 'h' | 'd':
                    if tg[1] not in tags:
                        return [kw]
                    elif tg[1] in "HBM":
                        self.fix = tg
                        _parse = [_tg for tag, arg in kw.items() if tag[2] not in "_" for _tg in do_parse(tag, **arg)]
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
                        coded = tags[tg[1]](**kw)
                    msg = NO_E.format(tg + str(kw) + " is empty coded")
                    self.macros[f"{tg}_{self.fix}_" if self.fix else tg] = coded if coded else msg
                    return [coded]
                case 'l':
                    # print("case 'l'", tg, kw, "case 'list'", self.list_comprehension(**kw))
                    return self.list_comprehension(**kw)
                case _:
                    return [NO_E.format(tg + "end")]

        tags = self.t._asdict()
        # print("data", data)
        code = [entity for tag, kw in data.items() for entity in do_parse(tag, **kw if isinstance(kw, dict) else data)]
        # print("code", code)
        return code

    def get_names(self, td):
        """Retrieve a named element from the internal registry.

        Parameters
        ----------
        td : str
            The identifier of the element to retrieve.

        Returns
        -------
        object
            The element if found, or the original identifier if not found.
        """
        return td if td not in self.names else self.names.get(td, [])

    def list_comprehension(self, l_x, l_y):
        """Generate a list of elements based on template data.

        This method implements a list comprehension-like functionality for
        generating multiple similar elements with different data.

        Parameters
        ----------
        l_x : str
            The template identifier to use for each element.
        l_y : list
            A list of dictionaries containing data for each element.

        Returns
        -------
        list
            A list of generated HTML elements.
        """
        nm = dict(self.names.get(l_x, []))
        # nm = {l_x: 0} if not isinstance(n := self.get_names(l_x), type) else n

        def do_expression(data):
            nm.update(**data)
            nmc = {l_x: nm}
            # print("do_expression", nm, "nmc", nmc, "data", data)
            return self.parse_template(nmc)[-1]

        # print("list_comprehension", l_x, "data", l_y, type(self.get_names(l_x)), "nm", nm)
        return [do_expression(data) for data in l_y]

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
    libs = "bulma/1.0.4/css/bulma.min.css font-awesome/7.0.0/css/all.min.css /css/labase.css".split()
    dt = [dict(href=lb) for lb in libs]
    di = dict(rel="shortcut icon", href="/_media/suucurijuba.png", type="image/x-icon")
    tg = dict(hk_0=dict(rel="stylesheet"), lk0=dict(l_x="hk_0_dH0_", l_y=dt), hk1=di)
    _ = dict(dH0=tg, dT0={"__0": "LABASE"}, dB0=dict(hh0=dict(__0="HALO", alt="HALO")))
    from tomlib import loads
    with open("alite/labase.toml", "rb") as f:
        cf = loads(f.read().decode("utf-8"))
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
