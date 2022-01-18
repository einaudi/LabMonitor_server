# -*- coding: utf-8 -*-

import datetime

import psycopg2
import config as cfg


conn = psycopg2.connect(database=cfg.DB_NAME)
cur = conn.cursor()
print('Successfully onnected to {0} database'.format(cfg.DB_NAME))

# FUNCTIONS
# Table creation
def create_table(tab_name, col_settings):

    cmd = '''CREATE TABLE IF NOT EXISTS {0} (
        id SERIAL PRIMARY KEY UNIQUE,
        time TIMESTAMP NOT NULL,
        localization varchar(255),
        device varchar(255)'''.format(tab_name)

    for col_name, col_type in col_settings.items():
        cmd += ',\n{0} {1}'.format(col_name, col_type)
    
    cmd += ');'

    cur.execute(cmd)
    conn.commit()

def add_columns(tab_name, col_settings):

    for col_name, col_type in col_settings.items():
        cmd = '''ALTER TABLE {0}
        ADD {1} {2};'''.format(tab_name, col_name, col_type)

        cur.execute(cmd)
        conn.commit()

# Data insertion
def insert_data(tab_name, data):

    d = datetime.datetime.utcnow()
    t = d.strftime(r"%Y-%m-%d %H:%M:%S")

    cmdHead = '''INSERT INTO {0} (time, localization, device'''.format(tab_name)
    cmdValue = '''VALUES (\'{0}\', \'{1}\', \'{2}\''''.format(
        t,
        data.pop('localization'),
        data.pop('device')
    )

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
    except Exception as e:
        print('Error on command: {0}'.format(cmd))
        print(e)
    conn.commit()

# Misc
def list_tables():

    cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
    ret = []
    for table in cur.fetchall():
        ret.append(table[0])

    return ret

def fetch_last(tables):

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


if __name__ == '__main__':

    tabs = list_tables()
    print('Tables in database {0}:'.format(cfg.DB_NAME))
    print(tabs)
    fetch_last(tabs)


    tab_name = 'main'
    col_settings = {
        'temperature' : 'real',
        'humidity' : 'real',
        'pressure' : 'real'
    }

    create_table(tab_name, col_settings)
    # add_columns(tab_name, col_settings)
