import unittest
import sys
from unittest.mock import MagicMock

sys.path.append('..')
import alite.html_build as hb
from alite.html_build import TemplateBuilder as Teb


class TestHtmlBuild(unittest.TestCase):
    def setUp(self):
        self.tb = Teb()

    def test_tb(self):
        self.assertIsInstance(self.tb, Teb)

    def test_html(self):
        ti = self.tb
        from browser import html
        self.html = ti.build()
        self.assertIs(ti.k, html.LINK)
        self.assertIn(ti.k, self.html)
    def test_head_html(self):
        ti = self.tb
        tgs = {f"hk{ix}": dict(rel="stylesheet", href=f"tg{ix}") for ix in range(2)}
        self.html = ti.build(tgs)
        self.assertIn(ti.k, self.html)
        self.assertEqual(4, len(self.html), self.html)
        self.assertEqual(ti.k, self.html[0])
        self.assertEqual(4, sum(1 for _ in self.html if ti.k == _), self.html)


if __name__ == '__main__':
    unittest.main()
