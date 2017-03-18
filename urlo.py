"""
asdf
"""
import datetime
import os
import sqlite3
import uuid

import falcon
import hug


ACCESS_KEY = os.environ['URLO_ACCESS_KEY']

conn = sqlite3.connect('data/urlo.db')
cur = conn.cursor()
cur.execute('''
create table if not exists urlo (
    id text primary key,
    url text,
    created_at text
);
''')

@hug.get('/')
@hug.cli()
def redirect(u):
    c = conn.cursor()
    c.execute('''
    select url
    from urlo
    where id=?
    ''', (u,))
    result = c.fetchall()
    if len(result) == 0:
        raise falcon.HTTPBadRequest('Not found', 'No url matched.')
    else:
        (url,) = result[0]
        return hug.redirect.permanent(url)

@hug.post('/')
@hug.cli()
def create(url, access_key, response):
    if access_key != ACCESS_KEY:
        raise falcon.HTTPUnauthorized('Unauthorized', 'access_key does not match', 'access_key')
    while True:
        c = conn.cursor()
        ident = uuid.uuid4().hex[:6]
        c.execute('''
        select id
        from urlo
        where id=?
        ''', (ident,))
        result = c.fetchall()
        if len(result) == 0:
            break
    c.execute('''
    insert into urlo
    values (?, ?, ?)
    ''', (ident, url, datetime.datetime.utcnow().isoformat()))
    conn.commit()
    return {
        'ok': True,
        'id': ident
    }

@hug.get('/auth')
def auth(access_key):
    if access_key == ACCESS_KEY:
        return {
            'ok': True
        }
    else:
        raise falcon.HTTPUnauthorized('Unauthorized', 'access_key does not match', 'access_key')
