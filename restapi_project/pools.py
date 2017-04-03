from __future__ import absolute_import, division, print_function
from twisted.internet import reactor
from twisted.enterprise.adbapi import ConnectionPool


def create_pool(size, filename):
    """ migratins/mydatabase.sqlite """
    pool = ConnectionPool('sqlite3',
                          filename,
                          cp_max=size,
                          check_same_thread=False,
                          cp_noisy=True,
                          cp_reconnect=True)
    return pool


def _get_all_records(txn):
    txn.execute("SELECT * FROM registered_members")
    result = txn.fetchall()
    if result:
        return result
    else:
        return None


def get_all_records(dbpool):
    return dbpool.runInteraction(_get_all_records)


def print_result(res):
    if not res:
        print('No records found')
    for element in res:
        print(element)


if __name__ == '__main__':
    dbpool = create_pool(2, './migrations/project_db.sqlite')
    get_all_records(dbpool).addCallback(print_result)
    reactor.run()
