import logging
import time

from sqlalchemy import sql, Column, Table, MetaData
from sqlalchemy.dialects.sqlite import pysqlite
from twisted.internet import defer, task

from restapi_project.pools import create_pool


class SelectAllAction(object):
    def __init__(self, pool, table_name, data_cols):
        self.log = logging.getLogger(self.__class__.__name__)
        self.pool = pool
        self.table_name = table_name

        self.meta = MetaData()
        self.data_cols = [Column(name) for name in data_cols]
        self.meta = MetaData()
        self.table = Table(self.table_name,
                           self.meta,
                           *tuple(self.data_cols))

    @defer.inlineCallbacks
    def __call__(self):
        self.log.debug('calling...: %s', self.table_name)
        ct = time.time()
        result = yield self.pool.runInteraction(self.thr_execute)
        self.log.debug('call: %s  finished in %.4fs', self.table_name, time.time()-ct)
        defer.returnValue(result)

    def thr_execute(self, txn):
        stmt = sql.select([self.table])
        compiled = stmt.compile(dialect=pysqlite.dialect(paramstyle="named"))
        raw_sql = unicode(compiled)
        self.log.debug('sql: %s', repr(raw_sql))
        txn.execute(raw_sql)
        result = txn.fetchall()
        return result


@defer.inlineCallbacks
def main(_):
    logging.basicConfig(level=logging.DEBUG)
    dbpool = create_pool(2, './migrations/project_db.sqlite')
    select_action = SelectAllAction(dbpool, 'registered_members', ('id',
                                                                   'f_name',
                                                                   'l_name',
                                                                   'email',
                                                                   'phone',
                                                                   'primary_skill'))
    result = yield select_action()
    for line in result:
        print(line)


if __name__ == '__main__':
    task.react(main)