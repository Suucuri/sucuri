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

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <https://is.gd/3Udt>`_.
|   `Labase <https://labase.github.io/>`_ - `NCE <https://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.
"""
from random import shuffle, sample, choice


class Control:
    """O jogo da afetividade.
    Registra a preferência de emoções em relação a uma imagem
    """

    def __init__(self, gui, capacidade=2):
        self._chosen = self._round = self._fotos = self._emo = None
        self._todas = list(range(48 * 2))
        # emo = self
        self.capacidade, self.gui = capacidade, gui
        self._sentir = "Amor Raiva Tristeza Alegria Surpresa Medo".split()
        self._msg = {}
    
    def play(self):
        """Inicia o jogo da afetividade."""
        shuffle(self._todas)
        # encoded = "".join([chr(ord("0")+lt) for lt in self._todas])
        self._round = 1
        self._fotos = [self._todas.pop() for _ in range(self._round+1)]
        bet = [(a, b) for a in range(1, 7) for b in range(1, 5) if a >= b]
        self._emo = sample(self._sentir, 4)
        self._chosen = [(0, choice(EMO[cs])) if cs in self._emo else (1, cs) for cs in self._sentir]
        return self._todas, bet, self._fotos, self._chosen


EMO = {'Raiva': ['Fúria', 'Ódio', 'Ressentimento', 'Indignação', 'Hostilidade'],
       'Amor': ['Afeição', 'Adoração', 'Paixão', 'Devoção', 'Compaixão'],
       'Alegria': ['Felicidade', 'Euforia', 'Deleite', 'Entusiasmo', 'Contentamento'],
       'Tristeza': ['Luto', 'Mágoa', 'Melancolia', 'Desespero', 'Solidão'],
       'Medo': ['Ansiedade', 'Terror', 'Pânico', 'Pavor', 'Horror'],
       'Surpresa': ['Espanto', 'Choque', 'Assombro', 'Descrença', 'Admiração']}
