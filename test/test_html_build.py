"""Html Page Builder Tester.

Tests a Template builder.

Classes neste módulo:
    - :py:class:`MyBrock` Mocks Html Calls
    - :py:class:`TestHtmlBuild` Test Html calls and template code builder.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>
.. tip:: *Milestone* 🚧 ⛲ 🛠️ Golden Penta ⭐ 25.08 (21)

Changelog
---------
.. versionadded::    25.08
   |br| Initial builder implementation (21).
   |br| added list comprehension (23).

|   **Open Source Notification:** This file is part of open source program **Alite**
|   **Copyright © 2025  Carlo Oliveira** <carlo@nce.ufrj.br>,
"""
import unittest
import sys
from unittest.mock import MagicMock
sys.path.append('..')
from alite.html_build import TemplateBuilder as Teb
HTML = 'alite.html_build.TemplateBuilder.HTML'


class MyBrock:
    def __init__(self, data):
        self.data = data
        self.k = self.link
        self.d = self.link
        self.Z = self.link
        self.H = self.head
        self.kwarg = {}

    def head(self, *args, **kwargs):
        self.kwarg = kwargs
        self.data.append([self.H, args, kwargs])
        return self.H

    def link(self, *args, **kwargs):
        self.kwarg = kwargs
        self.data.append([self.k, args, kwargs])
        return self.k

    def _repr__(self):
        return f'<MyBrock args={self.kwarg}>'

    # noinspection SpellCheckingInspection
    def _asdict(self):
        e = self.link
        return dict(k=e, d=e, Z=e, H=self.head)


class TestHtmlBuild(unittest.TestCase):
    def setUp(self):
        self.tb = Teb()
        self.dt = []
        self.tb.t = MyBrock(self.dt)

    def _do_mock(self, mock_ht):
        mock_ht.return_value = MyBrock({})
        return self.tb.t

    def test_tb(self):
        self.assertIsInstance(self.tb, Teb)

    @unittest.mock.patch(HTML)
    def test_html(self, mock_ht):
        ti = self._do_mock(mock_ht)
        self.html = self.tb.build(dict(hk0=dict(rel="stylesheet")))
        self.assertEqual(ti.k, ti.link)
        self.assertIn(ti.k, self.html)

    @unittest.mock.patch(HTML)
    def test_head_html(self, mock_ht):
        ti = self._do_mock(mock_ht)
        tgs = {f"hk{ix}": dict(rel="stylesheet", href=f"tg{ix}") for ix in range(2)}
        self.html = self.tb.build(tgs)
        self.assertIn(ti.k, self.html)
        self.assertEqual(2, len(self.html), self.html)
        self.assertEqual(ti.k, self.html[0])
        self.assertEqual(2, sum(1 for _ in self.html if ti.k == _), self.html)
        self.assertIn("hk0__", self.tb.names)

    @unittest.mock.patch(HTML)
    def test_html_comprehension(self, mock_ht):
        ti = self._do_mock(mock_ht)
        dt = [dict(href="tg0"), dict(href="tg1")]
        tg = dict(hk_0=dict(rel="stylesheet"), lk0=dict(l_x="hk_0__", l_y=dt))
        self.html = self.tb.build(tg)
        self.assertIn(ti.k, self.html)
        self.assertEqual(3, len(self.tb.t.data), self.tb.t.data)
        self.assertEqual(3, len(self.html), self.html)
        self.assertEqual(ti.k, self.html[0])
        self.assertEqual(3, sum(1 for _ in self.html if ti.k == _), self.html)

    @unittest.mock.patch(HTML)
    def test_html_with_head(self, mock_ht):
        ti = self._do_mock(mock_ht)
        tgs = {"dH0": {f"hk{ix}": dict(rel="stylesheet", href=f"tg{ix}") for ix in range(2)}}
        # print("test_html_with_head", tgs)
        self.html = self.tb.build(tgs)
        self.assertIn(ti.H, self.html)
        self.assertIn("hk0_dH0_", self.tb.names)
        self.assertEqual(3, len(self.dt), self.dt)
        self.assertEqual(1, len(self.html), self.html)
        self.assertIn(ti.H, self.html)


if __name__ == '__main__':
    unittest.main()
