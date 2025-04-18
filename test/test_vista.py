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
                self.restore = mock.Mock(name="restore")
                self.activate = mock.Mock(name="activate")
                self._foto_sel = mock.Mock(name="_foto_sel")
                self._foto_emo = mock.Mock(name="_foto_emo")
                self._emo_sel = mock.Mock(name="_emo_sel")

            def build(self, *_):
                return self

        def mock_body(fn):
            mo = mock.Mock(name=f"body_{fn}")
            fin = PARTE._fields.index(fn)
            mo.build.return_value = MockBody(fin, str(fn))
            return mo

        # self.hub, self.body = mock.Mock("hub"), mock.Mock("body")
        # self.hub, self.body = mock.Mock(name="hub"), mock.Mock(name="body")
        self.body = PARTE(*[mock_body(fn) for fn in PARTE._fields])
        self.hub = main.Hub()
        self.mb = MockBody
        # self.hub._combo = (self.hub, self.body, self, self, self)
        self.afeto = Afeto(self.hub, self.body)
        self.cl = [call('Foto', 'show_fotos', ANY),
                   call('Foto', 'foto_sel', ANY), call('Foto', 'sel_done', ANY)]

    def test_afeta_creation(self):
        self.assertIsInstance(self.afeto, Afeto)
        # self.hub.subscribe.assert_called()
        # self.hub.subscribe.assert_has_calls(self.cl, any_order=True)
        # self.hub.subscribe.assert_any_call('Control', 'play', ANY)
        self.assertIsInstance(a := self.afeto._parts.foto, self.afeto._types.foto, a)
        self.hub.execute("build_foto", [1, 2])
        self.assertEqual(0, self.afeto._components.foto[0].nome)

    def test_handle_fotos(self):
        self.hub.execute("build_foto", [1, 2])
        self.hub.execute('show_fotos', [1, 2])
        self.assertEqual(self.afeto._parts.foto._proxy, self.body.foto)
        self.assertIsInstance(self.afeto._components.foto[0], self.mb)
        self.assertIsInstance(self.afeto._components.foto[1], self.mb)
        self.afeto._components.foto[0].restore.assert_any_call()
        self.hub.execute('foto_sel', self.afeto._components.foto[0])
        self.afeto._components.foto[0]._foto_sel.assert_any_call()
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
        # self.body.sentir.build.assert_any_call(2)
        self.hub.execute('emo_sel', self.afeto._components.sentir[0])
        self.afeto._components.sentir[0].activate.assert_any_call()
        self.hub.execute('sel_done')
        self.afeto._components.sentir[0].restore.assert_has_calls([])


if __name__ == '__main__':
    unittest.main()
