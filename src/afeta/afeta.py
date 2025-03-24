#!/usr/bin/env python
# noinspection GrazieInspection
"""Main Engine for Emotion Game.

Classes neste módulo:
    - :py:class:`Act` Database registry classes.
    - :py:class:`Afeto` Emotion game engine.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    25.03
   |br| Initial game implementation (22).

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <https://is.gd/3Udt>`_.
|   `Labase <https://labase.github.io/>`_ - `NCE <https://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.
"""
import uuid
from collections import namedtuple
from datetime import datetime as dt
from random import shuffle
from unittest.mock import Mock


class Act:
    ACT = namedtuple("Acts", ["a", "p"])(Mock, Mock)

    def __init__(self):
        def now():
            return dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        class Action:
            def __init__(self):
                self.begin = None
                self.start = None
                self.end = None
                self.actor = []

            def waiting(self):
                self.begin = now()

            def join(self, actor):
                self.start = now()
                self.actor.append(actor)

            def ending(self):
                self.end = now()

            def starting(self):
                self.start = now()

            def _repr(self):
                name = type(self).__name__[:2]
                return {name: [self.begin, self.end]}

            def __repr__(self):
                name = type(self).__name__[:2]
                entry = {name: []}
                entry.update(self._repr())
                return entry.__repr__()

        class Play(Action):
            def __init__(self):
                super().__init__()
                self.short_id = str(uuid.uuid4().fields[-1])[:9]

            def _id(self):
                return self.short_id

            def _repr(self):
                return {"Pl": [self.begin, self.end]}

        class Round(Play):
            def _repr(self):
                sup = super()._id()
                rep = {"Ro": [self.begin, self.end, "Pl" + sup]}
                # rep.update(sup)
                return rep

        class Selection(Round):
            def _repr(self):
                sup = super()._repr()
                rep = {"Se": [self.begin, self.end]}
                rep.update(sup)
                return rep

        class Voting(Round):
            def _repr(self):
                sup = super()._repr()
                rep = {"Vo": [self.begin, self.end]}
                rep.update(sup)
                return rep

        class Turn(Round):
            def __init__(self, kind, chosen):
                super().__init__()
                self.kind = kind  # foto, emotion, bet
                self.choice = chosen

            def _repr(self):
                sup = super()._id()

                rep = {"Tu": ["Ro" + sup, self.begin, self.end, self.choice, self.kind]}
                # rep.update(sup)
                return rep

        Act.ACT = namedtuple("Acts", ["a", "p", "r", "s", "v", "t"])(
            Action, Play, Round, Selection, Voting, Turn)


class Afeto:
    """O jogo da afetividade.
    Registra a preferência de emoções em relação a uma imagem
    """

    def __init__(self, capacidade, gui):
        emo = self

        class Step:
            def __init__(self, nexter):
                self.next = nexter
                self.todas = None
                self.todos = 0

            def go(self, msg):
                _ = self
                emo.send(msg)

            def get(self, msg):
                ack = self.do_get(msg)
                self.ack(ack) if ack else None
                pass

            def ack(self, msg):
                self.todos += 1 if msg else 0
                self.next.go(_ack) if (_ack := self.do_ack(msg)) else None

            def do_ack(self, msg: dict) -> dict:
                _ = self, msg
                return {}

            def do_get(self, msg: dict) -> dict:
                _ = self, msg
                return {}

        class Play(Step):
            """Wait for players and share foto distribution"""
            def do_get(self, msg):
                emo.todas = self.todas = self.todas or [int(ord(lt)-ord("á")+10)for lt in msg]

            def do_ack(self, msg: dict) -> dict:
                _msg = emo.round() if self.todos == (emo.capacidade - 1) else {}
                return _msg

        class Round(Step):
            """Play a round with selection and voting"""
            def do_get(self, msg):
                emo.round(msg)

        self.proceed = namedtuple("Proceed", ["p", "r", "s", "v", "t"])(*([10] * 5))
        self._step = []
        for stp in [Step, Round, Play]:
            self._step.append(stp(self._step[-1] if self._step else None))
        self.capacidade, self.gui = capacidade, gui
        self._msg = {}
        self.todas = list(range(48 * 2))
        shuffle(self.todas)
        encoded = "".join([chr(ord("0")+lt) for lt in self.todas])
        self._round = 1
        self.fotos = [self.todas.pop() for _ in range(self._round+1)]
        self.current = Play(Step)
        self.current.go(dict(todas=encoded))

    def round(self, msg):
        """Aguarda todos os jogadores entrarem na partida"""
        def handle_selection(_msg):
            self._msg.update(_msg)
            self.current.next.go(dict(foto=1))
        self._msg = {}
        self.gui.play(handle_selection)
        pass

    def send(self, msg):
        pass

    def receive(self, msg):
        self.current.get(msg)


if __name__ == '__main__':
    def test():
        a = Act()
        p = a.ACT.p()
        r = a.ACT.r()
        s = a.ACT.s()
        t = a.ACT.t(0, 1)
        _ = p.waiting() or p.join("me") or p.ending()
        _ = r.waiting() or r.join("me") or r.ending()
        _ = s.waiting() or s.join("me") or s.ending()
        _ = t.waiting() or t.join("me") or t.ending()
        print(t)

    Afeto(2, object())
    test()
