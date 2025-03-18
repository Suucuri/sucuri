#!/usr/bin/env python
# noinspection GrazieInspection
""" Web service main.

Classes neste módulo:
    - :py:class:`DirectoryHandler` handle all routes from web.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>
.. codeauthor:: Craig Campbell <https://craig.is>

Changelog
---------
.. versionchanged::    25.03
   |br| Revert to enable serving index from root (15).

|   **Open Source Notification:** This file is part of open source program **Suucurijuba**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   # Copyright (c) 2018, Craig Campbell
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <https://is.gd/3Udt>`_.
|   `Labase <https://labase.github.io/>`_ - `NCE <https://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.
"""
import tomllib


class Coop:
    def __init__(self, pair, members):
        self.group = pair
        self.members = members
        self.lead = members[0]

    def ping(self, send, member, msg):
        [send(m, 0, msg) for m in self.members if m != member]


class Lead(Coop):
    def ping(self, send, member, msg):
        [send(m, 1, msg) for m in self.members if m != member and (member == self.lead)]


class Tutor(Coop):
    def ping(self, send, member, msg):
        [send(m, 1 if m == self.lead else 0, msg) for m in self.members if m != member]


class Monitor(Coop):
    def ping(self, send, member, msg):
        send(self.lead, 2, msg) if member is not self.lead else None


class Db:
    ALL = {}
    MEMBERS = {}

    def __init__(self):
        self.db = Db.ALL
        self.members = Db.MEMBERS

    def do(self, msg):
        def mapeia(grupo, payload):
            mapa = dict(c=Coop, l=Lead, t=Tutor, m=Monitor)
            ator = mapa[grupo[0]](grupo, payload)
            print(decoded)
            self.db[grupo] = ator
            [self.members.update({m: self.members.get(m, set()).union(ator)}) for m in payload]
            for m in payload:
                self.members[m] = self.members[m].union({ator}) if m in self.members else {ator}
        decoded = tomllib.loads(msg)
        [mapeia(it, payload) for it, payload in decoded.items()]

    def add(self, **kwargs):
        self.db.update(**kwargs)

    def rem(self, entry):
        self.db.pop(entry)

    def receive(self, send, msg):
        decoded = tomllib.loads(msg)
        [act.ping(send, grp, **mss) for grp, mss in decoded.items() for act in self.members[grp]]


def main():
    def snd(dst, csl, msg):
        print(dst, csl, msg)
    db = Db()
    ad = """coop_0=['m1', 'm2']
coop_1=['m3', 'm4']
lead_2=['m3', 'm5']"""
    db.do(ad)
    assert isinstance(db.db['coop_0'], Coop) and ('m1' in db.db['coop_0'].members), db.db['coop_0'].members
    assert isinstance(db.db['coop_1'], Coop) and ('m3' in db.db['coop_1'].members), db.db['coop_0'].members
    assert isinstance(db.db['lead_2'], Lead) and ('m3' in db.db['lead_2'].members), db.db['lead_2'].members
    assert isinstance(db.db['lead_2'], Lead) and ('m3' == db.db['lead_2'].lead), db.db['lead_2'].members
    assert db.members['m1'] == {db.db['coop_0']}, db.members['m1']
    assert db.members['m3'].issuperset({db.db['lead_2'], db.db['coop_1']}), db.members['m3']
    pn = """['m1']
msg='s0'
[m3]
msg='s3'
[m5]
msg='s2'
    """
    db.receive(snd, pn)


if __name__ == '__main__':
    main()
