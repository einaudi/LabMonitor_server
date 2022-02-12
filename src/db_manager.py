# -*- coding: utf-8 -*-

import datetime

import psycopg2

import src.config as cfg


def log_to_file(mes):

    with open(cfg.LOG_FILE, 'a') as f:
        d = datetime.datetime.now()
        t = d.strftime(r"%Y-%m-%d %H:%M:%S")
        
        f.write('{0} : {1}\n'.format(t, mes))

def db_connect():
    try:
        conn = psycopg2.connect(
            host=cfg.DB_HOST,
            database=cfg.DB_NAME,
            user=cfg.DB_USER,
            password=cfg.DB_PSWD
        )
        cur = conn.cursor()

        return conn, cur
    except Exception as e:
        log_to_file('Error occured during connecting to database: {0}'.format(e))

# FUNCTIONS
# Table/column creation
def add_table(tab_name, col_settings, sensor=True):

    conn, cur = db_connect()

    if sensor:
        cmd = '''CREATE TABLE IF NOT EXISTS {0} (
            id SERIAL PRIMARY KEY UNIQUE,
            time TIMESTAMP NOT NULL,
            localization varchar(255),
            device varchar(255)'''.format(tab_name)
    else:
        cmd = '''CREATE TABLE IF NOT EXISTS {0} (
        id SERIAL PRIMARY KEY UNIQUE,
        time TIMESTAMP NOT NULL'''.format(tab_name)

    for col_name, col_type in col_settings.items():
        cmd += ',\n{0} {1}'.format(col_name, col_type)
    
    cmd += ');'
    # print(cmd)

    try:
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        log_to_file('Error occured during adding new table: {0}'.format(e))
    finally:
        conn.close()

def add_table_simple(tab_name, col_settings):

    conn, cur = db_connect()

    cmd = '''CREATE TABLE IF NOT EXISTS {0} (
        id SERIAL PRIMARY KEY UNIQUE,
        time TIMESTAMP NOT NULL'''.format(tab_name)

    for col_name, col_type in col_settings.items():
        cmd += ',\n{0} {1}'.format(col_name, col_type)
    
    cmd += ');'

    try:
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        log_to_file('Error occured during adding new table: {0}'.format(e))
    finally:
        conn.close()

def add_columns(tab_name, col_settings):

    conn, cur = db_connect()

    for col_name, col_type in col_settings.items():
        try:
            cmd = '''ALTER TABLE {0}
            ADD {1} {2};'''.format(tab_name, col_name, col_type)

            cur.execute(cmd)
            conn.commit()
        except Exception as e:
            log_to_file('Error occured during adding new column: {0}'.format(e))
        
    conn.close()

# Data insertion
def insert_data(tab_name, data):

    conn, cur = db_connect()

    d = datetime.datetime.utcnow()
    t = d.strftime(r"%Y-%m-%d %H:%M:%S")

    cmdHead = '''INSERT INTO {0} (time'''.format(tab_name)
    cmdValue = '''VALUES (\'{0}\''''.format(
        t
    )

    for key, value in data.items():
        cmdHead += ', {0}'.format(key)
        try:
            value = float(value)
            cmdValue += ', {0:.4e}'.format(value)
        except TypeError:
            cmdValue += ', \'{0}\''.format(value)

    cmdHead += ')\n'
    cmdValue += ');'

    cmd = cmdHead + cmdValue

    try:
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        log_to_file('Error occured during data insertion: {0}'.format(e))
    finally:
        conn.close()

def insert_data_simple(tab_name, data):

    conn, cur = db_connect()

    d = datetime.datetime.utcnow()
    t = d.strftime(r"%Y-%m-%d %H:%M:%S")

    cmdHead = '''INSERT INTO {0} (time'''.format(tab_name)
    cmdValue = '''VALUES (\'{0}\''''.format(t)

    for key, value in data.items():
        cmdHead += ', {0}'.format(key)
        try:
            value = float(value)
            cmdValue += ', {0:.4e}'.format(value)
        except TypeError:
            cmdValue += ', \'{0:.4e}\''.format(value)

    cmdHead += ')\n'
    cmdValue += ');'

    cmd = cmdHead + cmdValue

    try:
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        log_to_file('Error occured during data insertion: {0}'.format(e))
    finally:
        conn.close()

# Table/column removal
def remove_table(tab_name):

    conn, cur = db_connect()

    cmd = '''DROP TABLE {0};'''.format(tab_name)

    try:
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        log_to_file('Error occured during removing table: {0}'.format(e))
    finally:
        conn.close()

def remove_column(tab_name, col_name):

    conn, cur = db_connect()

    cmd = '''
    ALTER TABLE {0}
    DROP COLUMN {1};'''.format(tab_name, col_name)

    try:
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        log_to_file('Error occured during removing column: {0}'.format(e))
    finally:
        conn.close()

# Misc
def list_tables():

    conn, cur = db_connect()

    try:
        cur.execute("""SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'""")
    except Exception as e:
        log_to_file('Error occured during listing tables: {0}'.format(e))
    ret = []
    for table in cur.fetchall():
        ret.append(table[0])

    conn.close()

    return ret

def get_db_tree():

    conn, cur = db_connect()

    # Get tables
    ret = {}
    try:
        cur.execute("""SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'""")
        for table in cur.fetchall():
            ret[table[0]] = {}
            # Get columns
            cur.execute("""SELECT * FROM information_schema.columns WHERE 
            table_schema = 'public' AND
            table_name = \'{0}\';""".format(table[0]))
            for column in cur.fetchall():
                # print(column)
                ret[table[0]][column[3]] = {
                    'type' : column[7]
                }
    except Exception as e:
        log_to_file('error occured during traversing databse: {0}'.format(e))
    finally:
        conn.close()

    return ret

def fetch_last(tables):

    conn, cur = db_connect()

    for table in tables:
            cur.execute(
                '''SELECT * FROM {0} ORDER BY id
                '''.format(table)
            )
            rows = cur.fetchall()
            if cur.rowcount:
                print('\nTable: ', table)
                print('Total count: ', cur.rowcount)
                print(rows[-1])
            else:
                print('\nNo rows in ', table)

    conn.close()


if __name__ == '__main__':

    tabs = list_tables()
    print('Tables in database {0}:'.format(cfg.DB_NAME))
    print(tabs)
    fetch_last(tabs)
    db_tree = get_db_tree()
    print('DB tree:')
    print(db_tree)


    tab_name = 'test'
    col_settings = {
        'col1' : 'real',
        'col2' : 'real'
    }

    # create_table(tab_name, col_settings)
    # add_columns(tab_name, col_settings)
