import unittest
from unittest import mock
from unittest.mock import ANY, call
# mock.patch('vista.Body')
from afeta.controle import Control, Step, DATA


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


if __name__ == '__main__':
    unittest.main()
