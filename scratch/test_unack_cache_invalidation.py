import sys
sys.path.insert(0, '.')
from app import app
from models import User, Acknowledgement
from extensions import db, cache
from datetime import date, timedelta
from acknowledgements import get_report_dates_for_user

with app.app_context():
    sujatha = User.query.filter_by(username='sujatha').first()
    today = date.today()
    start_date = today - timedelta(days=30)
    report_dates = get_report_dates_for_user(sujatha, start_date, today)
    print(f"Report dates for Sujatha in last 30 days: {len(report_dates)}")
    
    # Pick an unacknowledged date or create a test date
    user_acks = {a.date: a for a in Acknowledgement.query.filter_by(user_id=sujatha.user_id).all()}
    pending_dates = [d for d in sorted(report_dates) if not (user_acks.get(d) and user_acks.get(d).acknowledged_at)]
    print(f"Pending dates before test: {len(pending_dates)}")
    
    if not pending_dates:
        # Pick the most recent report date and un-acknowledge it for the test
        test_date = sorted(report_dates)[-1]
        existing_ack = Acknowledgement.query.filter_by(user_id=sujatha.user_id, date=test_date).first()
        if existing_ack:
            db.session.delete(existing_ack)
            db.session.commit()
    else:
        test_date = pending_dates[0]
        
    print(f"Test date to acknowledge: {test_date}")

with app.test_client() as client:
    cache.clear()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(sujatha.user_id)
        sess['_fresh'] = True
        
    # Step 1: Load dashboard before acknowledgement
    resp1 = client.get('/lead/dashboard?team=team1')
    assert resp1.status_code == 200
    html1 = resp1.data.decode('utf-8')
    
    # Check cache key exists
    unack_cache_key = f"unack_count:{sujatha.user_id}:{today.isoformat()}"
    cached_val1 = cache.get(unack_cache_key)
    print(f"Step 1: Dashboard loaded. Cached unack_count = {cached_val1}")
    assert cached_val1 is not None and cached_val1 > 0
    
    # Step 2: Acknowledge the test date via POST /ack
    ack_resp = client.post('/ack', json={'date': test_date.strftime('%Y-%m-%d')})
    assert ack_resp.status_code == 200
    print(f"Step 2: Acknowledged date {test_date}. HTTP 200: {ack_resp.get_json()}")
    
    # Step 3: Verify cache key was invalidated
    cached_val2 = cache.get(unack_cache_key)
    print(f"Step 3: After /ack, cached unack_count is: {cached_val2}")
    assert cached_val2 is None, "Cache was NOT invalidated upon acknowledgement!"
    print("  [PASS] Cache successfully invalidated on report acknowledgement.")
    
    # Step 4: Reload dashboard and verify count decreased
    resp2 = client.get('/lead/dashboard?team=team1')
    assert resp2.status_code == 200
    cached_val3 = cache.get(unack_cache_key)
    print(f"Step 4: Reloaded dashboard. New cached unack_count = {cached_val3}")
    assert cached_val3 == cached_val1 - 1, f"Expected count {cached_val1 - 1}, got {cached_val3}"
    print(f"  [PASS] Count updated from {cached_val1} -> {cached_val3} immediately!")

print("\n==========================================================")
print("UNACKNOWLEDGED COUNT CACHE INVALIDATION TEST PASSED (100%)!")
print("==========================================================")
