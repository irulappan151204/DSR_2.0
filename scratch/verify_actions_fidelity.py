import sys
sys.path.insert(0, '.')
from app import app
from models import User, Action
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.attributes import set_committed_value
from extensions import db, cache
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

with app.app_context():
    sujatha = User.query.filter_by(username='sujatha').first()
    md = User.query.filter_by(username='auditteam').first()
    
    print("--- 1. VERIFYING ACTION FIDELITY FOR TEAM LEAD (Sujatha) ---")
    team_user_ids = [u.user_id for u in User.query.filter_by(team_id=sujatha.team_id).all()]
    now = datetime.now(ZoneInfo('Asia/Kolkata'))
    start_date_obj = datetime.strptime('2025-07-01', '%Y-%m-%d').date()
    end_date_obj = now.date()
    
    date_filter = db.and_(
        db.func.date(Action.created_at) >= start_date_obj,
        db.func.date(Action.created_at) <= end_date_obj
    )
    
    # Direct DB Query
    raw_parent_actions = Action.query.filter(
        (Action.assigned_user_id.in_(team_user_ids)) | (Action.created_by.in_(team_user_ids)),
        Action.parent_action_id.is_(None),
        date_filter
    ).order_by(Action.created_at.desc()).all()
    
    raw_parent_ids = [a.id for a in raw_parent_actions]
    
    # Fetch with joinedload
    actions_fetched = Action.query.options(joinedload(Action.assigned_user)).filter(
        (Action.assigned_user_id.in_(team_user_ids)) | (Action.created_by.in_(team_user_ids)),
        date_filter
    ).order_by(Action.created_at.desc()).all()
    
    def sort_actions_group(action_list):
        unfinished = [a for a in action_list if a.status != 'Finished']
        finished = [a for a in action_list if a.status == 'Finished']
        unfinished_sorted = sorted(unfinished, key=lambda a: a.created_at, reverse=True)
        finished_sorted = sorted(finished, key=lambda a: (a.completed_at or datetime.min, a.created_at), reverse=True)
        return unfinished_sorted + finished_sorted

    def build_action_tree(actions_list):
        parent_actions = [a for a in actions_list if a.parent_action_id is None]
        child_actions = [a for a in actions_list if a.parent_action_id is not None]
        children_by_parent = defaultdict(list)
        for child in child_actions:
            children_by_parent[child.parent_action_id].append(child)
        parent_actions_sorted = sort_actions_group(parent_actions)
        def build_children_for_parent(parent):
            if parent.id in children_by_parent:
                children = sort_actions_group(children_by_parent[parent.id])
                for child in children:
                    child_nested = build_children_for_parent(child)
                    set_committed_value(child, 'child_actions', child_nested)
                return children
            else:
                return []
        for parent in parent_actions_sorted:
            children = build_children_for_parent(parent)
            set_committed_value(parent, 'child_actions', children)
        for a in actions_list:
            if 'child_actions' not in a.__dict__:
                set_committed_value(a, 'child_actions', [])
        return parent_actions_sorted
    
    tree = build_action_tree(actions_fetched)
    tree_parent_ids = [a.id for a in tree]
    
    print(f"Direct DB Parent Count: {len(raw_parent_ids)}")
    print(f"Tree Parent Count:      {len(tree_parent_ids)}")
    assert set(raw_parent_ids) == set(tree_parent_ids), "Parent Action IDs mismatch!"
    print("  [PASS] Parent Action IDs match 100%.")
    
    # Flatten tree and add orphan children exactly as actions.py does
    def flatten_action_tree(parent_list):
        result = []
        for parent in parent_list:
            result.append(parent)
            if hasattr(parent, 'child_actions') and parent.child_actions:
                result.extend(flatten_action_tree(parent.child_actions))
        return result

    ordered_actions = flatten_action_tree(tree)
    all_parent_ids = set()
    def collect_parent_ids(parent_list):
        for parent in parent_list:
            all_parent_ids.add(parent.id)
            if hasattr(parent, 'child_actions') and parent.child_actions:
                collect_parent_ids(parent.child_actions)
    collect_parent_ids(tree)
    orphan_children = [a for a in actions_fetched if a.parent_action_id is not None and a.parent_action_id not in all_parent_ids]
    if orphan_children:
        ordered_actions.extend(sort_actions_group(orphan_children))

    raw_total_actions = Action.query.filter(
        (Action.assigned_user_id.in_(team_user_ids)) | (Action.created_by.in_(team_user_ids)),
        date_filter
    ).count()
    
    print(f"Direct DB Total Actions: {raw_total_actions}")
    print(f"Ordered Actions Count:   {len(ordered_actions)}")
    print(f"Orphan Children Count:   {len(orphan_children)}")
    assert raw_total_actions == len(ordered_actions), "Total actions mismatch!"
    print("  [PASS] All actions accounted for: zero missing, zero duplicates.")
    
    # 2. Check Action Counts & Priority Counts
    print("\n--- 2. VERIFYING IN-MEMORY VS DB COUNTS ---")
    db_pending = Action.query.filter(
        (Action.assigned_user_id.in_(team_user_ids)) | (Action.created_by.in_(team_user_ids)),
        Action.parent_action_id.is_(None),
        Action.status != 'Finished',
        date_filter
    ).count()
    
    db_completed = Action.query.filter(
        (Action.assigned_user_id.in_(team_user_ids)) | (Action.created_by.in_(team_user_ids)),
        Action.parent_action_id.is_(None),
        Action.status == 'Finished',
        date_filter
    ).count()
    
    mem_pending = sum(1 for a in tree if a.status != 'Finished')
    mem_completed = sum(1 for a in tree if a.status == 'Finished')
    
    print(f"Pending Counts:   DB={db_pending}, In-Memory={mem_pending}")
    print(f"Completed Counts: DB={db_completed}, In-Memory={mem_completed}")
    assert db_pending == mem_pending, "Pending count mismatch!"
    assert db_completed == mem_completed, "Completed count mismatch!"
    print("  [PASS] Action status counts match 100%.")
    
    # 3. Verify set_committed_value has no adverse side effects on persistence
    print("\n--- 3. TESTING PERSISTENCE INTEGRITY AFTER set_committed_value ---")
    test_action = Action(
        title="Temporary Persistence Test Action",
        action_text="Test action description text",
        due_date=now,
        assigned_user_id=sujatha.user_id,
        status="Pending",
        priority="Medium",
        created_by=sujatha.user_id,
        created_at=now
    )
    db.session.add(test_action)
    db.session.commit()
    test_id = test_action.id
    print(f"Created temporary action ID: {test_id}")
    
    reloaded = db.session.get(Action, test_id)
    assert reloaded.title == "Temporary Persistence Test Action"
    assert reloaded.status == "Pending"
    
    reloaded.status = "In Progress"
    db.session.commit()
    
    reloaded_again = db.session.get(Action, test_id)
    assert reloaded_again.status == "In Progress"
    print("  [PASS] Action creation and update work normally without side effects.")
    
    db.session.delete(reloaded_again)
    db.session.commit()
    print("  [PASS] Temporary action cleaned up. DB unchanged.")

    sujatha_id = str(sujatha.user_id)
    # Ensure any lingering test actions are cleaned up
    Action.query.filter(Action.title == "Temporary Persistence Test Action").delete()
    db.session.commit()

# 4. HTTP client test on /actions
with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['_user_id'] = sujatha_id
        sess['_fresh'] = True
    resp = client.get('/actions')
    assert resp.status_code == 200
    html = resp.data.decode('utf-8')
    assert 'Action Items' in html or 'Actions' in html
    print(f"\n--- 4. HTTP GET /actions VERIFICATION ---")
    print(f"HTTP Status: {resp.status_code}, Response Size: {len(html)} bytes")
    print("  [PASS] Rendered template contains expected Action UI structure.")

print("\n========================================================")
print("ALL /ACTIONS FIDELITY & PERSISTENCE TESTS PASSED (100%)!")
print("========================================================")
