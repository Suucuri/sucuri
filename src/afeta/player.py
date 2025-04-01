#!/usr/bin/env python
# noinspection GrazieInspection
"""Automated NPC to fake emotions.

Classes neste módulo:
    - :py:funct: message NPC Player.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    25.03
   |br| Initial server implementation (30).

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
"""
from browser import bind, self  # as master
# from src.afeta.controle import Control
# PLAYER = lambda: 0


class Player:
    PLAYER = object

    def __init__(self):
        # global PLAYER
        Player.PLAYER = self
        self.count = 0
        # PLAYER = self.do_count
        # self.bind(elf.message, "message")

    def do_count(self):
        self.count += 1
        return self.count


@bind(self, "message")
def message(evt):
    """Handle a message sent by the main script.
    evt.data is the message body.
    """
    try:
        self.send(Player.PLAYER.do_count())
    except ValueError:
        self.send('-1')


Player()
