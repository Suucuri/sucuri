import unittest
from unittest import mock
from unittest.mock import ANY, call

import main
from resposta import Afeto, PARTE

ENC = "".join([chr(ord("À") + lt) for lt in range(48 * 2)])


class TestView(unittest.TestCase):
    def setUp(self):
        class MockBody:
            def __init__(self, nome=None, texto=None):
                self.nome, self.texto = nome, texto
                self.restore = mock.Mock(name=f"{texto}_restore")
                self.activate = mock.Mock(name=f"{texto}_activate")
                self._foto_sel = mock.Mock(name=f"{texto}_foto_sel")
                self._foto_emo = mock.Mock(name=f"{texto}__foto_emo")
                self._emo_sel = mock.Mock(name=f"{texto}__emo_sel")
                self._bet_sel = mock.Mock(name=f"{texto}__bet_sel")
                self.build = mock.Mock(name=f"{texto}_build")
                fin = PARTE._fields.index(nome)
                self.build.return_value = self  # MockBody(fin, str(nome))
                # self._open_modal = mock.Mock(name="_open_modal")
                # self._done_modal = mock.Mock(name="_done_modal")

            def build(self, *_):
                return self

        def mock_body(fn):
            return MockBody(nome=fn, texto=f"body_{fn}")

        def _mock_body(fn):
            # mo = mock.Mock(name=f"body_{fn}")
            mo = MockBody(nome=fn, texto=f"body_{fn}")
            fin = PARTE._fields.index(fn)
            mo.build.return_value = MockBody(fin, str(fn))
            return mo

        # self.hub, self.body = mock.Mock("hub"), mock.Mock("body")
        # self.hub, self.body = mock.Mock(name="hub"), mock.Mock(name="body")
        self.body = PARTE(*[mock_body(fn) for fn in PARTE._fields])
        self.hub = main.Hub()
        # print("TestView")
        self.hub.subscribe(self.__class__.__name__, "inicio", None)
        self.mb = MockBody
        # self.hub._combo = (self.hub, self.body, self, self, self)
        self.afeto = Afeto(self.hub, self.body)
        self.cl = [call('Foto', 'show_fotos', ANY),
                   call('Foto', 'foto_sel', ANY), call('Foto', 'sel_done', ANY)]

    def test_afeta_creation(self):
        self.assertIsInstance(self.afeto, Afeto)
        self.assertIsInstance(a := self.afeto._parts.foto, self.afeto._types.foto, a)
        self.hub.execute("build_foto", [1, 2])
        self.assertEqual("foto", self.afeto._components.foto[0].nome)
        # self.assertEqual(0, self.afeto._components.foto[0].nome)

    def test_handle_fotos(self):
        self.hub.execute("build_foto", [1, 2])
        self.hub.execute('show_fotos', [1, 2])
        self.assertEqual(self.afeto._parts.foto._proxy, self.body.foto)
        self.assertIsInstance(self.afeto._components.foto[0], self.mb)
        self.assertIsInstance(self.afeto._components.foto[1], self.mb)
        self.afeto._components.foto[0].restore.assert_any_call()
        self.afeto._components.foto[0].restore.assert_has_calls([call()])
        self.hub.execute('foto_sel', self.afeto._components.foto[0])
        self.afeto._components.foto[0]._foto_sel.assert_any_call()
        self.afeto._components.foto[0]._foto_sel.assert_has_calls([call()])
        self.hub.execute('sel_done')
        self.afeto._components.foto[0].restore.assert_has_calls([call(), call(), call(), call()])
        self.hub.execute('foto_emo', self.afeto._components.foto[0], 1)
        self.afeto._components.foto[0]._foto_emo.assert_called_once_with(1)

    def test_handle_sentir(self):
        self.hub.execute("build_sentir", [1, 2, 3, 4, 5])
        self.hub.execute('emo_all', [1, 2, 3, 4, 5])
        self.assertEqual(self.afeto._parts.sentir._proxy, self.body.sentir)
        self.assertIsInstance(self.afeto._components.sentir[0], self.mb)
        self.afeto._components.sentir[0].activate.assert_any_call()
        self.afeto._components.sentir[0].activate.assert_has_calls([call()])
        # self.body.sentir.build.assert_any_call(2)
        self.hub.execute('emo_sel', self.afeto._components.sentir[0])
        self.afeto._components.sentir[0].activate.assert_any_call()
        self.afeto._components.sentir[0].activate.assert_has_calls([call()])
        self.hub.execute('sel_done')
        self.afeto._components.sentir[0].restore.assert_has_calls([call()])
        self.afeto._components.sentir[1].restore.assert_has_calls([call()])

    def test_handle_aposta(self):
        self.hub.execute("build_ficha", [1, 2, 3, 4, 5])
        self.hub.execute('bet_all')
        self.assertEqual(self.afeto._parts.ficha._proxy, self.body.ficha)
        self.assertIsInstance(self.afeto._components.ficha[0], self.mb)
        self.afeto._components.ficha[0].activate.assert_any_call()
        # self.body.sentir.build.assert_any_call(2)
        self.hub.execute('bet_sel', self.afeto._components.ficha[0])
        self.afeto._components.ficha[0].activate.assert_any_call()
        self.hub.execute('sel_done')
        self.afeto._components.ficha[0].restore.assert_has_calls([call()])

    def test_handle_modal(self):
        self.hub.execute("build_aguarda", [0])
        self.assertIn("open_modal", self.hub._subscriber)
        # self.assertEqual(None, self.hub._subscriber["open_modal"][0][1])
        self.assertEqual(self.afeto._parts.aguarda._proxy, self.body.aguarda)
        self.assertIsInstance(a := self.afeto._components.aguarda[0], self.mb, a)
        self.hub.execute('open_modal')
        self.afeto._components.aguarda[0].activate.assert_called_once_with()
        # self.body.sentir.build.assert_any_call(2)
        self.hub.execute('done_modal')
        # self.afeto._components.aguarda[0].restore.assert_any_call()
        self.afeto._components.aguarda[0].restore.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
