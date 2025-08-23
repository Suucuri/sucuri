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

    def link(self, *args, **kwargs):
        self.data.append([self.k, args, kwargs])
        return self.k

    # noinspection SpellCheckingInspection
    def _asdict(self):
        return dict(k=self.link)


class TestHtmlBuild(unittest.TestCase):
    def setUp(self):
        self.tb = Teb()
        self.dt = []
        self.tb.t = MyBrock(self.dt)

    def test_tb(self):
        self.assertIsInstance(self.tb, Teb)

    @unittest.mock.patch(HTML)
    def test_html(self, mock_ht):
        mock_ht.return_value = MyBrock({})
        ti = self.tb.t
        self.html = self.tb.build(dict(hk0=dict(rel="stylesheet")))
        self.assertEqual(ti.k, ti.link)
        self.assertIn(ti.k, self.html)

    @unittest.mock.patch(HTML)
    def test_head_html(self, mock_ht):
        mock_ht.return_value = MyBrock({})
        ti = self.tb.t
        tgs = {f"hk{ix}": dict(rel="stylesheet", href=f"tg{ix}") for ix in range(2)}
        self.html = self.tb.build(tgs)
        self.assertIn(ti.k, self.html)
        self.assertEqual(2, len(self.html), self.html)
        self.assertEqual(ti.k, self.html[0])
        self.assertEqual(2, sum(1 for _ in self.html if ti.k == _), self.html)
        self.assertIn("hk0__", self.tb.names)

    @unittest.mock.patch(HTML)
    def test_html_comprehension(self, mock_ht):
        mock_ht.return_value = MyBrock({})
        ti = self.tb.t
        dt = [dict(href="tg0"), dict(href="tg1")]
        tg = dict(hk0=dict(rel="stylesheet"), lk0=dict(l_x="hk0__", l_y=dt))
        self.html = self.tb.build(tg)
        self.assertIn(ti.k, self.html)
        self.assertEqual(3, len(self.tb.t.data))
        self.assertEqual(3, len(self.html), self.html)
        self.assertEqual(ti.k, self.html[0])
        self.assertEqual(3, sum(1 for _ in self.html if ti.k == _), self.html)


if __name__ == '__main__':
    unittest.main()
