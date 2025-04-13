#!/usr/bin/env python
# noinspection GrazieInspection
"""Main Engine for Emotion Game.

Classes neste módulo:
    - :py:class:`Control` Emotion game controller.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    25.03
   |br| Initial module implementation (24).
   |br| Add Foto, Sentir (30).

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <https://is.gd/3Udt>`_.
|   `Labase <https://labase.github.io/>`_ - `NCE <https://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.
"""
from collections import namedtuple
from random import shuffle, sample, choice

DATA = namedtuple('DATA', ('text', 'tip', 'origin'))


def no_op(*_args):
    pass


class Step:
    def __init__(self):
        self._nome = self._actor = self._action = self._text = self._tag = None
        self._tip = []

    def start(self):
        pass

    def handle_event(self, data):
        pass

    def proceed_game(self):
        pass


class Parte:
    def __init__(self, nome):
        # self._nome = self._text = nome
        self._nome = self._text = str(nome)
        # print("Inicia parte", self.__class__.__name__, nome)
        self._actor = self._action = self._tag = None

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text += f", {text}"
        if self._tag is not None:
            self._tag.innerHTML = self._text

    def start(self):
        pass


class Control:
    """O jogo da afetividade.
    Registra a preferência de emoções em relação a uma imagem
    """

    def __init__(self, gui, capacidade=2):
        self._current_step = self.gui = gui
        # self._current = namedtuple("Current", "step, handler")(Step(), no_op)
        self._chosen = self._round = self._fotos = self._emo = None
        self._todas = list(range(48 * 2))
        self.capacidade, self.gui = capacidade, gui
        gui.subscribe(self.__class__.__name__, "play", self.play)
        gui.subscribe(self.__class__.__name__, "handle_event", self.handle_event)
        self._sentir = "Amor Raiva Tristeza Alegria Surpresa Medo".split()
        self._msg = {}
        self.__part = namedtuple("Parts", "name, list")
        self.__step = namedtuple("Step", "recruit, round, select, choose, vote, score")
        self._part = self._parts_builder()
        self._step = self._steps_builder()
        gui.subscribe(self.__class__.__name__, "proceed_game", self.__proceed_game)

    def __proceed_game(self):
        self._current_step.proceed_game()

    def _parts_builder(self):
        class Sentir(Parte):
            def build(self):
                pass

        class Foto(Parte):
            def build(self):
                pass

        class Ficha(Parte):
            def build(self):
                pass

        return self.__part(
            namedtuple("Part", "foto, sentir, ficha")(Foto, Sentir, Ficha),
            namedtuple("AllParts", "foto, sentir, ficha")(list(), list(), list()))

    def _steps_builder(self):
        ctrl = self

        class Recruit(Step):
            def start(self):
                print(self.__class__.__name__, " Recruit _step_one")
                # ctrl._part.list.foto.extend([ctrl._part.name.foto(i) for i in range(ctrl._round + 1)])
                ctrl._part.list.foto.append(ctrl._part.name.foto(ctrl._todas.pop()))
                ctrl._emo = sample(ctrl._sentir, 4)

        class Round(Step):
            def start(self):
                print(self.__class__.__name__, "Round _step_one")
                # ctrl._part.list.foto.extend([ctrl._part.name.foto(i) for i in range(ctrl._round + 1)])
                ctrl._part.list.foto.append(ctrl._part.name.foto(ctrl._todas.pop()))
                ctrl._emo = sample(ctrl._sentir, 4)
                ctrl._chosen = [(0, choice(EMO[cs])) if cs in ctrl._emo else (1, cs) for cs in ctrl._sentir]
                ctrl._part.list.sentir.clear()
                ctrl._part.list.sentir.extend([ctrl._part.name.sentir(i) for i in ctrl._chosen])

            def proceed_game(self):
                print(self.__class__.__name__, "proceed_game")
                ctrl._step.select.start()

        class Select(Step):
            def start(self):
                # ctrl._part.list.foto.extend([ctrl._part.name.foto(i) for i in range(ctrl._round + 1)])
                ctrl._current_step = self
                self._action = self._step_one
                print(self.__class__.__name__, "Select _start")

            def _step(self, data: DATA):
                foto: Parte = ctrl._part.list.foto[int(data.origin)]
                foto.text = data.text
                self._tip.append(DATA(data.text, foto, data.origin))
                ctrl.gui.execute("view_update")
                self._action = self._step_one
                self._action()
                print(self.__class__.__name__, "Select _step")

            def _step_one(self):
                self._action = self._step_two
                ctrl.gui.execute("view_update")
                print("Select _step_one")

            def _step_two(self):
                self._action = self._step_three
                ctrl.gui.execute("view_update")
                print("Select _step_two")

            def _step_three(self):
                self._action = self._step_one
                ctrl.gui.execute("view_update")
                print("Select _step_three")
                ctrl._step.choose.start()

            def handle_event(self, data):
                print(self.__class__.__name__, "handle_event", data)
                self._action()
                #
                # self._step(data)

        class Choose(Select):
            def start(self):
                ctrl._current_step = self
                self._action = self._step_one
                print(self.__class__.__name__, "Choose _start")

            def _step_three(self):
                self._action = self._step_one
                ctrl._step.vote.start()

        class Vote(Select):
            def _step_three(self):
                self._action = self._step_one
                ctrl._step.score.start()

            pass

        class Score(Select):
            def _step_three(self):
                self._action = self._step_one
                ctrl._step.round.start()

            pass

        return self.__step(
            recruit=Recruit(), round=Round(), select=Select(), choose=Choose(), vote=Vote(), score=Score())

    def play(self):
        """Inicia o jogo da afetividade."""
        shuffle(self._todas)
        # encoded = "".join([chr(ord("0")+lt) for lt in self._todas])
        self._round = 1
        # self._fotos = [self._todas.pop() for _ in range(self._round + 1)]
        bet = [(a, b) for a in range(1, 7) for b in range(1, 5) if a >= b]
        # self._emo = sample(self._sentir, 4)
        # self._chosen = [(0, choice(EMO[cs])) if cs in self._emo else (1, cs) for cs in self._sentir]
        self._part.list.foto.append(self._part.name.foto(self._todas.pop()))
        self._current_step = self._step.round
        # print("Inicia o jogo da afetividade", self._current_step)
        self._current_step.start()
        # return self._todas, bet, self._fotos, self._chosen
        return self._todas, bet, [ft.text for ft in self._part.list.foto], self._chosen

    def handle_event(self, data):
        print("Control handle_event", self._current_step, data)
        self._current_step.handle_event(data)


EMO = {'Raiva': ['Fúria', 'Ódio', 'Ressentimento', 'Indignação', 'Hostilidade'],
       'Amor': ['Afeição', 'Adoração', 'Paixão', 'Devoção', 'Compaixão'],
       'Alegria': ['Felicidade', 'Euforia', 'Deleite', 'Entusiasmo', 'Contentamento'],
       'Tristeza': ['Luto', 'Mágoa', 'Melancolia', 'Desespero', 'Solidão'],
       'Medo': ['Ansiedade', 'Terror', 'Pânico', 'Pavor', 'Horror'],
       'Surpresa': ['Espanto', 'Choque', 'Assombro', 'Descrença', 'Admiração']}

if __name__ == '__main__':
    class _Test:
        def subscribe(self, *args):
            pass

        def update(self, data: DATA):
            _ = self
            print(data._asdict())


    test = _Test()
    c = Control(test)
    tds, bets, fts, chs = c.play()
    [c.handle_event(DATA(text=f"start{i}", tip=test, origin=0)) for i in range(11)]
