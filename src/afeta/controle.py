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
from random import shuffle


class Control:
    """O jogo da afetividade.
    Registra a preferência de emoções em relação a uma imagem
    """

    def __init__(self, gui, capacidade=2):
        self._round = None
        self._fotos = None
        self._todas = None
        emo = self
        self.capacidade, self.gui = capacidade, gui
        self._msg = {}
    
    def play(self):
        self._todas = list(range(48 * 2))
        shuffle(self._todas)
        encoded = "".join([chr(ord("0")+lt) for lt in self._todas])
        self._round = 1
        self._fotos = [self._todas.pop() for _ in range(self._round+1)]
