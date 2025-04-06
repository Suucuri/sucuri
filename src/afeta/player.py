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
from browser import bind, timer, self as boss  # as master


class MS:
    G = {}

    @classmethod
    def x(cls, k, *args):
        return cls.G[k](*args)

# from src.afeta.controle import Control
# PLAYER = lambda: 0


class Player:
    PLAYER = object

    def __init__(self):
        ops = (self.recruit_players, self.acknowledged)
        MS.G = {k: op for k, op in zip("recruit_players acknowledged".split(), ops)}
        Player.PLAYER = self
        self.count = 0
        self.player_count = 4
        self.acknowledged_players = 0
        # PLAYER = self.do_count
        # self.bind(elf.message, "message")

    def recruit_players(self, player):
        self.player_count = player
        self.acknowledged()
        # boss.send(["error", f"recruit_players count:{self.player_count}"])

    def acknowledged(self, player=1):
        self.acknowledged_players += player
        boss.send(["new_player", self.acknowledged_players])

        if self.acknowledged_players >= self.player_count:
            boss.send(["proceed_game"])
        else:
            timer.set_timeout(self.acknowledged, 4000)
        # return self.acknowledged_players

    def do_count(self):
        self.count += 1
        return self.count


@bind(boss, "message")
def message(evt):
    """Handle a message sent by the main script.
    evt.data is the message body.
    """
    try:
        MS.x(*evt.data)
        # boss.send(["error", f"iniciou: {str(evt.data)}"])
        # self.send(Player.PLAYER.do_count())

    except Exception as va:
        boss.send(["error", str(evt.data), str(va)])


Player()
