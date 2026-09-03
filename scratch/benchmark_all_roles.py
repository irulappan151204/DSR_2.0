import sys
import time
import tracemalloc
sys.path.insert(0, '.')
from app import app
from models import User
from sqlalchemy import event
from extensions import db, cache

with app.app_context():
    users = {
        'Team Member': User.query.filter_by(username='anita').first(),
        'Team Lead': User.query.filter_by(username='sujatha').first(),
        'MD': User.query.filter_by(username='auditteam').first(),
        'Admin': User.query.filter_by(username='admin').first(),
    }
    
    # Query counter & timer
    query_count = 0
    sql_duration = 0.0
    
    @event.listens_for(db.engine, 'before_cursor_execute')
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        global query_count
        query_count += 1
        context._query_start_time = time.perf_counter()

    @event.listens_for(db.engine, 'after_cursor_execute')
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        global sql_duration
        if hasattr(context, '_query_start_time'):
            sql_duration += (time.perf_counter() - context._query_start_time)

test_routes = [
    ('/actions', ['Team Member', 'Team Lead', 'MD', 'Admin']),
    ('/lead/dashboard?team=team1', ['Team Lead']),
    ('/md/dashboard?team=all', ['MD', 'Admin']),
    ('/statistics', ['Team Member', 'Team Lead', 'MD', 'Admin']),
    ('/my_history', ['Team Member', 'Team Lead', 'MD', 'Admin']),
    ('/critical', ['Team Member', 'Team Lead', 'MD', 'Admin']),
]

print("=" * 115)
print(f"{'Role':<12} | {'Endpoint':<32} | {'HTTP':<4} | {'Total Time':<10} | {'Queries':<8} | {'SQL Time':<10} | {'Peak Mem (KB)':<12}")
print("=" * 115)

with app.test_client() as client:
    for route, roles in test_routes:
        for role_name in roles:
            user = users[role_name]
            if not user:
                continue
                
            cache.clear()
            with client.session_transaction() as sess:
                sess['_user_id'] = str(user.user_id)
                sess['_fresh'] = True
                
            query_count = 0
            sql_duration = 0.0
            
            tracemalloc.start()
            t0 = time.perf_counter()
            resp = client.get(route)
            total_time = time.perf_counter() - t0
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            print(f"{role_name:<12} | {route:<32} | {resp.status_code:<4} | {total_time:>8.3f}s | {query_count:>7} | {sql_duration:>8.3f}s | {peak_mem / 1024:>12.1f}")

print("=" * 115)
