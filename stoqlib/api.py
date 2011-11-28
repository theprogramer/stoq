# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2011 Async Open Source
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU Lesser General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
##
## Author(s): Stoq Team <stoq-devel@async.com.br>
##
##

"""Stoqlib API

Singleton object which makes it easier to common stoqlib APIs without
having to import their symbols.
"""

from contextlib import contextmanager

from kiwi.component import get_utility

from stoqlib.lib.parameters import sysparam, is_developer_mode
from stoqlib.lib.interfaces import IStoqConfig
from stoqlib.database.runtime import (get_connection, new_transaction,
                                      rollback_and_begin, finish_transaction)
from stoqlib.database.runtime import (get_current_branch,
                                      get_current_station, get_current_user)


class StoqAPI(object):
    def get_connection(self):
        return get_connection()

    def new_transaction(self):
        return new_transaction()

    def finish_transaction(self, trans, model):
        return finish_transaction(trans, model)

    def rollback_and_begin(self, trans):
        rollback_and_begin(trans)

    def get_current_branch(self, conn):
        return get_current_branch(conn)

    def get_current_station(self, conn):
        return get_current_station(conn)

    def get_current_user(self, conn):
        return get_current_user(conn)

    @contextmanager
    def trans(self):
        """Creates a new transaction and commits/closes it when done.

        It should be used as:

          with api.trans() as trans:
              ...
              trans.retval = True
              ...

        When the execution of the with statement has finished this
        will commit the object, close the transaction.
        trans.retval will be used to determine if the transaction
        should be committed or rolled back (via finish_transaction)
        """
        trans = self.new_transaction()
        yield trans
        retval = bool(trans.retval)
        if self.finish_transaction(trans, retval):
            trans.committed = True
        else:
            trans.committed = False
        trans.close()

    @property
    def config(self):
        return get_utility(IStoqConfig)

    def sysparam(self, conn):
        return sysparam(conn)

    def is_developer_mode(self):
        return is_developer_mode()

api = StoqAPI()

