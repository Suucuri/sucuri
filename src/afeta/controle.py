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
import uuid
from collections import namedtuple
from datetime import datetime
from random import shuffle, sample, choice
from typing import override

DATA = namedtuple('DATA', ('text', 'tip', 'origin'))
ME, BET = uuid.uuid4().urn[9:], [(a, b) for a in range(1, 7) for b in range(1, 5) if a >= b]


def no_op(*_args):
    pass


class Step:
    def __init__(self):
        self._nome = self._actor = self._action = self._text = self._tag = None
        self._tip = self._states = []
        self._state = self._actor = {}

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
        # self._chosen = self._fotos = self._emo = None
        self._todas = list(range(48 * 2))
        shuffle(self._todas)
        self._me, self._bet = ME, BET
        self._current_step = self._current_state = self.gui = gui
        self._sentir = "Amor Raiva Tristeza Alegria Surpresa Medo".split()
        self._emo = sample(self._sentir, 4)
        self._chosen = [(0, choice(EMO[cs])) if cs in self._emo else (1, cs) for cs in self._sentir]
        _, _emo = self._emo.remove(cx := choice(self._emo)), cx
        self._foto_emo_bet = choice([0, 1]), _emo, -1
        self._fotos = []
        print("ME self._foto_emo_bet", ME, self._foto_emo_bet)

        # self._current = namedtuple("Current", "step, handler")(Step(), no_op)
        self._timed_todas_fotos = (datetime.now(), self._todas, self._chosen)
        self.capacidade, self.gui, self._round = capacidade, gui, 0
        gui.subscribe(self.__class__.__name__, "play", self.play)
        gui.subscribe(self.__class__.__name__, "handle_event", self.handle_event)
        self._msg = {}
        self.__part = namedtuple("Parts", "name, list")
        self.__step = namedtuple("Step", "recruit, round, select, choose, vote, score")
        self._part = self._parts_builder()
        self._step = self._steps_builder()
        self._current_state = self._state_builder()
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

    def _state_builder(self):
        ctrl = self

        class StatIter:
            def __init__(self, seq):
                self.seq = seq

            def __iter__(self):
                return self

            def __next__(self):
                self.seq.pop(0)

        class State(Step):

            def _execute(self, method, *args):
                _ = self
                # print("State _execute", method, *args)
                ctrl.gui.execute(method, *args)

            def _do_build(self):
                _ = self
                return []

            def build(self, **state):
                self._state.update(state)
                return self._do_build()

        class Inicio(State):
            @override
            def _do_build(self):
                sy = self._sync__z
                return [self.launch_modal__z, self.register__z, sy, sy, sy, self.done_modal__z]

            def launch_modal__z(self, *_):
                self._execute("open_modal", ctrl._timed_todas_fotos)
                # return lambda ttf: self.launch_modal__z(ttf) if self._state["count"] else None

            def register__z(self, registry):
                _ = registry
                self._execute("foto_sync", ctrl._timed_todas_fotos)
                # return lambda ttf: self.launch_modal__z(ttf) if self._state["count"] else None

            def _sync__z(self, timed_todas_fotos):
                ctrl._timed_todas_fotos = min(ctrl._timed_todas_fotos, timed_todas_fotos)
                self._fotos = [ctrl._todas.pop(0)]
                self._execute("foto_sync", ctrl._timed_todas_fotos)
                # return lambda ttf: self.launch_modal__z(ttf) if self._state["count"] else None

            def done_modal__z(self, *_):
                ctrl._todas = fotos = ctrl._timed_todas_fotos[1]
                ctrl._bet = BET
                ctrl._fotos.append(fotos.pop())
                ctrl._fotos.append(fotos.pop())
                self._execute("done_modal", None)
                # ctrl._part.list.foto.append(fotos.pop())

        class Rodada(State):
            @override
            def _do_build(self):
                # fe, em = self.foto_emo__z, self.emo_foto__z
                return [self.start__z]

            def start__z(self, *_):
                ctrl._round += 1
                ctrl._bet.pop(bt) if (bt := int(ctrl._foto_emo_bet[-1])) > 0 else None
                ctrl._fotos.pop(int(ctrl._foto_emo_bet[0]))
                ctrl._fotos.append(ctrl._todas.pop())
                self._execute("show_fotos", ctrl._fotos)

        class Selecionando(State):
            @override
            def _do_build(self):
                fe, em = self.foto_emo__z, self.emo_foto__z
                return [fe, em, fe, self.emo_foto_done__z]

            def foto_emo__z(self, foto):
                xal, _ = self._state["ops"]
                self._execute("foto_sel", foto)
                self._execute("emo_all")
                self._state["foto"] = foto
                # foto.text = data.text
                # _foto: Parte = ctrl._part.list.foto[int(foto)]
                self._actor[foto] = None
                # return lambda ttf: self.launch_modal__z(ttf) if self._state["count"] else None

            def emo_foto__z(self, emo):
                _, xfo = self._state["ops"]
                self._execute(xfo, (self._state["foto"], emo))
                self._tip.append((self._state["foto"], emo))
                # return lambda ttf: self.launch_modal__z(ttf) if self._state["count"] else None

            def emo_foto_done__z(self, emo):
                self.emo_foto__z(emo)
                self._execute("sel_done", self._tip)
                print("emo_foto_done__z", self._tip)
                # self._tip.clear()

                # return lambda ttf: self.launch_modal__z(ttf) if self._state["count"] else None

        class Votando(State):
            def _do_build(self):
                cd, vt, cf = self.candidates__z, self.vote__z, self.confirma__z
                return [cd, cd, cd, vt, cf]

            def candidates__z(self, cdn):
                xal, *_ = self._state["ops"]
                self._tip.extend(cdn)
                print("candidates__z", xal, self._tip, cdn)
                self._execute(xal, self._tip)

            def vote__z(self, cdn):
                xal, mark, *_ = self._state["ops"]
                self._execute(mark, cdn)
                self._tip.append(cdn)

            def confirma__z(self, cdn):
                xal, mark, feito = self._state["ops"]
                self._execute(mark, cdn)
                self._tip.append(cdn)
                self._execute(feito, self._tip)

        def bs(sx):
            return Selecionando().build(foto=None, ops=sx)
        ss, sb = "emo_all emo_foto".split(), "bet_all bet_foto".split()
        __vt = Votando().build(ops="foto_party foto_sel sync_fotos".split())
        __states, __round, __ini = [], Rodada().build(count=3), Inicio().build(count=3)
        # [__states.extend(seq) for seq in [__ini, __round, bs(ss), bs(ss), __vt, bs(sb), bs(sb), __vt]]
        [__states.extend(seq) for seq in [__ini, __round, bs(ss), __vt, bs(sb), bs(sb), __vt]]
        return StatIter(__states)

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
        # print("Control handle_event", self._current_step, data)
        self._current_state.seq.pop(0)(data)

    def _handle_event(self, data):
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
