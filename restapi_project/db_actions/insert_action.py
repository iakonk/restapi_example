import logging
import time

from sqlalchemy import sql, Column, Table, MetaData
from sqlalchemy.dialects.sqlite import pysqlite
from twisted.internet import defer, task

from restapi_project.pools import create_pool


class InsertAction(object):

    def __init__(self, pool, table_name, data_cols):
        self.log = logging.getLogger(self.__class__.__name__)
        self.pool = pool
        self.table_name = table_name
        self.data_cols = [Column(name) for name in data_cols]

        self.meta = MetaData()
        self.table = Table(self.table_name,
                           self.meta,
                           *tuple(self.data_cols))

    @defer.inlineCallbacks
    def __call__(self, **data):
        self.log.debug('calling...: %s', self.table_name)
        ct = time.time()
        result = yield self.pool.runInteraction(self.thr_execute, **data)
        self.log.debug('call: %s finished in %.4fs', self.table_name, time.time()-ct)
        defer.returnValue(result)

    def thr_execute(self, txn, **data):
        stmt = sql.insert(self.table).values(**data)
        compiled = stmt.compile(dialect=pysqlite.dialect(paramstyle="named"))
        raw_sql = unicode(compiled)
        params = compiled.params
        self.log.debug(' sql: %s , params: %s', repr(raw_sql), params)
        try:
            txn.execute(raw_sql, params)
        except:
            raise
        return None


@defer.inlineCallbacks
def main(_):
    logging.basicConfig(level=logging.DEBUG)
    db_pool = create_pool(2, './migrations/project_db.sqlite')
    insert_action = InsertAction(db_pool,
                                 'registered_members',
                                 ('f_name', 'l_name', 'email', 'phone', 'primary_skill'))
    yield insert_action(f_name='jack', l_name='Jack Jones')


if __name__ == '__main__':
    task.react(main)