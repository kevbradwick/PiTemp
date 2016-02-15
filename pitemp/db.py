from MySQLdb import connect

from pitemp import get_config


def execute(sql, data=None, fetch_all=False):
    """
    :param sql: string
    :param data: dict
    :param fetch_all: bool
    :return:
    """
    host = get_config('host', 'localhost')
    username = get_config('username', 'root')
    password = get_config('password', '')
    db_name = get_config('database', 'tempi')

    con = connect(host, username, password, db_name)
    cur = con.cursor()
    cur.execute(sql, data)
    con.commit()

    result = None
    if fetch_all:
        result = cur.fetchall()

    con.close()
    return result
