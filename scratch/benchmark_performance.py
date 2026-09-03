import sys
sys.path.insert(0, '.')
import time
from app import app
from models import User
from sqlalchemy import event
from extensions import db, cache

with app.app_context():
    query_count = 0
    query_time = 0.0

    @event.listens_for(db.engine, 'before_cursor_execute')
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        global query_count
        query_count += 1
        context._query_start_time = time.time()

    @event.listens_for(db.engine, 'after_cursor_execute')
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        global query_time
        total = time.time() - context._query_start_time
        query_time += total

    sujatha = User.query.filter_by(username='sujatha').first()
    md = User.query.filter_by(username='auditteam').first()

    endpoints = [
        ('Sujatha', sujatha.user_id, '/actions'),
        ('Sujatha', sujatha.user_id, '/lead/dashboard?team=team1'),
        ('MD', md.user_id, '/md/dashboard?team=all'),
        ('Sujatha', sujatha.user_id, '/statistics'),
        ('Sujatha', sujatha.user_id, '/critical'),
        ('Sujatha', sujatha.user_id, '/my_history'),
    ]

with app.test_client() as client:
    print('--- PERFORMANCE BENCHMARK ---')
    for user_label, uid, ep in endpoints:
        with app.app_context():
            cache.clear()
        query_count = 0
        query_time = 0.0

        with client.session_transaction() as sess:
            sess['_user_id'] = str(uid)
            sess['_fresh'] = True

        t0 = time.time()
        resp = client.get(ep)
        t1 = time.time()

        print(f'{user_label:7s} | {ep:32s} | HTTP {resp.status_code} | Total: {t1-t0:6.3f}s | SQL Queries: {query_count:3d} | SQL Time: {query_time:6.3f}s')
