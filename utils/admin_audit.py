import os
from timezone_utils import now_ist

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
AUDIT_LOG_FILE = os.path.join(LOG_DIR, 'admin_audit.log')

def log_admin_action(admin, action, target_user_id, target_username, reason=None, ip_address=None):
    """Record an administrative action to the audit log."""
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        timestamp = now_ist().strftime('%Y-%m-%d %H:%M:%S IST')
        admin_info = f"Admin({admin.user_id}:{admin.username})" if admin else "System"
        reason_str = f" | Reason: {reason}" if reason else ""
        ip_str = f" | IP: {ip_address}" if ip_address else ""
        
        log_line = f"[{timestamp}] {admin_info} -> Action: {action} on Target({target_user_id}:{target_username}){reason_str}{ip_str}\n"
        
        with open(AUDIT_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_line)
    except Exception as e:
        print(f"Failed to write admin audit log: {e}")
