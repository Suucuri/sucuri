import unittest
from datetime import datetime
from unittest import mock
from unittest.mock import ANY, call
# mock.patch('vista.Body')
from afeta.controle import Control, Step  # , DATA

SOON = datetime.now().now()


class TestControl(unittest.TestCase):
    def setUp(self):
        hub = mock.Mock()
        self.hub = hub
        self.control = Control(self.hub)
        self.cl = [call('Control', 'play', ANY), call('Control', 'handle_event', ANY),
                   call('Control', 'proceed_game', ANY)]

    def test_control_creation(self):
        self.assertIsInstance(self.control, Control)
        self.hub.subscribe.assert_called()
        self.hub.subscribe.assert_has_calls(self.cl, any_order=True)
        self.hub.subscribe.assert_any_call('Control', 'play', ANY)
        self.assertIsInstance(a := self.control._step.recruit, Step, a)
        self.assertEqual(self.control._part.list.foto, [])

    def test_recruit_step(self):
        self.control.handle_event(None)
        self.hub.execute.assert_called()
        self.hub.execute.assert_any_call('open_modal', ANY)

    def test_round_step(self):
        self._run_step(ext=(0, 0))
        self.hub.execute.assert_any_call('show_fotos', ANY)

    def test_register_step(self):
        [self.control.handle_event(dt) for dt in [None, (datetime.now(), [1, 2, 3, 4, 5])]]
        self.hub.execute.assert_any_call('foto_sync', ANY)

    def _run_step(self, evt=None, ext=()):
        dn = (datetime.now(), [1, 2, 3, 4, 5])
        ev = evt or ([None, dn, dn, dn, (SOON, [1, 2, 3, 4, 5])] + list(ext))
        [self.control.handle_event(dt) for dt in ev]

    def test_sync_step(self):
        self._run_step()
        self.hub.execute.assert_any_call('foto_sync', ANY)

    def test_don_modal_step(self):
        dn = (datetime.now(), [1, 2, 3, 4, 5])
        self._run_step([None, dn, dn, dn, dn, dn])
        self.hub.execute.assert_any_call('done_modal', ANY)

    def test_sel_foto_step(self):
        self._run_step(ext=(0, 0, 0))
        # foto_list = self.control._part.list.foto
        foto_list = self.control._fotos
        self.assertIn(5, foto_list)
        self.hub.execute.assert_any_call('foto_sel', 0)
        self.hub.execute.assert_any_call('emo_all')

    def test_sel_emo_step(self):
        self._run_step(ext=(0, 0, 0, 3))
        self.hub.execute.assert_any_call('emo_foto', ANY)
        # self.hub.execute.assert_any_call('emo_foto', (5, 3))

    def test_sel_foto_emo_step2(self):
        self._run_step(ext=(0, 0, 0, 3, 1))
        self.hub.execute.assert_any_call('foto_sel', 1)
        self.control.handle_event(2)
        self.hub.execute.assert_any_call('emo_foto', (1, 2))
        self.hub.execute.assert_any_call('sel_done', [(0, 3), (1, 2)])
        # self.hub.execute.assert_any_call('sel_done', ANY)
        # self.assertEqual(self.control._tip, [])

    def test_voting_step(self):
        self._run_step(ext=(0, 0, 0, 3, 1, 2, [(1, 1), (0, 0)]))
        self.hub.execute.assert_any_call('foto_party', ANY)
        self.control.handle_event([(0, 3), (1, 2)])
        self.hub.execute.assert_any_call('foto_party', [(1, 1), (0, 0), (0, 3), (1, 2)])
        self.control.handle_event([(1, 0), (2, 1)])
        self.hub.execute.assert_any_call('foto_party', [(1, 1), (0, 0), (0, 3), (1, 2), (1, 0), (2, 1)])
        self.control.handle_event([(1, 1)])
        self.hub.execute.assert_any_call('foto_sel', ANY)
        # self.control.handle_event(2)
        # self.hub.execute.assert_any_call('emo_foto', (1, 2))


"""
class TestControl(unittest.TestCase):
    def setUp(self):
        hub = mock.Mock()
        self.hub = hub
        self.control = Control(self.hub)
        self.cl = [call('Control', 'play', ANY), call('Control', 'handle_event', ANY),
                   call('Control', 'proceed_game', ANY)]

    def test_control_creation(self):
        self.assertIsInstance(self.control, Control)
        self.hub.subscribe.assert_called()
        self.hub.subscribe.assert_has_calls(self.cl, any_order=True)
        self.hub.subscribe.assert_any_call('Control', 'play', ANY)
        self.assertIsInstance(a := self.control._step.recruit, Step, a)
        self.assertEqual(self.control._part.list.foto, [])

        # self.assertEqual(True, False)  # add assertion here

    def test_recruit_step(self):
        self.control.play()
        self.assertEqual(len(self.control._part.list.foto), 2)
        self.assertEqual(len(self.control._current_step._tip), 0)
        self.assertEqual(self.control._current_step._action, None)
        self.assertEqual(self.control._current_step.__class__.__name__, "Round")

    def test_select_step_one(self):
        self.control.play()
        self.control._current_step.proceed_game()
        self.assertEqual(len(self.control._part.list.foto), 2)
        self.assertEqual(len(self.control._current_step._tip), 0)
        self.assertIsNotNone(self.control._current_step._action)
        self.assertEqual("_step_one", self.control._current_step._action.__name__)
        self.assertEqual("Select", self.control._current_step.__class__.__name__, )
        self.hub.execute.assert_has_calls([], any_order=True)

    def test_select_step_two(self):
        self.control.play()
        self.control._current_step.proceed_game()
        self.control.handle_event(DATA("foto", 0, 0))
        self.assertEqual(2, len(self.control._part.list.foto))
        self.assertEqual(1, len(self.control._current_step._tip))
        self.assertEqual("_step_two", self.control._current_step._action.__name__)
        self.assertEqual("Select", self.control._current_step.__class__.__name__, )
        self.hub.execute.assert_has_calls([call("view_update")], any_order=True)
        self.hub.execute.assert_called_once_with("view_update")

    def test_select_step_three(self):
        self.control.play()
        self.control._current_step.proceed_game()
        self.control.handle_event(DATA("love", 1, 0))
        self.control.handle_event(DATA("hate", 0, 1))
        self.assertEqual(2, len(self.control._part.list.foto))
        self.assertEqual([' love', ' hate'], [x._text.split(",")[1] for x in self.control._part.list.foto])
        self.assertEqual(2, len(self.control._current_step._tip))
        self.assertEqual("_step_three", self.control._current_step._action.__name__)
        self.assertEqual("Select", self.control._current_step.__class__.__name__, )
        # self.hub.execute.assert_called_once_with("view_update")
        self.hub.execute.assert_has_calls([call("view_update"), call("view_update")], any_order=True)
"""

if __name__ == '__main__':
    unittest.main()
