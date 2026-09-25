import logging
from datetime import datetime, timedelta
from extensions import db
from models.notes import Note
from timezone_utils import now_ist

logger = logging.getLogger(__name__)

def parse_reminder_datetime(date_str):
    """Safely parse datetime string from HTML datetime-local input or ISO format."""
    if not date_str:
        return None
    date_str = str(date_str).strip()
    if not date_str or date_str.lower() in ('null', 'none', ''):
        return None
    for fmt in ('%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        logger.warning(f"Unable to parse reminder datetime: {date_str}")
        return None

def get_notes_counts(user_id):
    """Get accurate counts for tab badges and filter pills."""
    curr_time = now_ist().replace(tzinfo=None)
    
    total_active = Note.query.filter_by(user_id=user_id, is_archived=False, is_done=False).count()
    pinned = Note.query.filter_by(user_id=user_id, is_archived=False, is_done=False, is_pinned=True).count()
    with_reminders = Note.query.filter(
        Note.user_id == user_id,
        Note.is_archived == False,
        Note.is_done == False,
        Note.reminder_at.isnot(None)
    ).count()
    due_reminders = Note.query.filter(
        Note.user_id == user_id,
        Note.is_archived == False,
        Note.is_done == False,
        Note.reminder_at.isnot(None),
        Note.reminder_at <= curr_time,
        Note.reminder_seen == False
    ).count()
    upcoming_reminders = Note.query.filter(
        Note.user_id == user_id,
        Note.is_archived == False,
        Note.is_done == False,
        Note.reminder_at.isnot(None),
        Note.reminder_at > curr_time
    ).count()
    completed = Note.query.filter_by(user_id=user_id, is_archived=False, is_done=True).count()
    archived = Note.query.filter_by(user_id=user_id, is_archived=True).count()
    
    return {
        'all': total_active,
        'pinned': pinned,
        'reminders': with_reminders,
        'due_reminders': due_reminders,
        'upcoming_reminders': upcoming_reminders,
        'completed': completed,
        'archived': archived
    }

def get_notes_for_user(user_id, filter_type='all', search_query=None, color=None, priority=None):
    """Fetch and filter notes for a specific user."""
    curr_time = now_ist().replace(tzinfo=None)
    query = Note.query.filter_by(user_id=user_id)
    
    if filter_type == 'archived':
        query = query.filter_by(is_archived=True)
    elif filter_type in ('done', 'completed'):
        query = query.filter_by(is_archived=False, is_done=True)
    elif filter_type == 'pinned':
        query = query.filter_by(is_archived=False, is_done=False, is_pinned=True)
    elif filter_type == 'reminders':
        query = query.filter(Note.is_archived == False, Note.is_done == False, Note.reminder_at.isnot(None))
    elif filter_type == 'due':
        query = query.filter(
            Note.is_archived == False,
            Note.is_done == False,
            Note.reminder_at.isnot(None),
            Note.reminder_at <= curr_time,
            Note.reminder_seen == False
        )
    elif filter_type == 'everything':
        query = query.filter_by(is_archived=False)
    else:
        # Default: all active (uncompleted, unarchived)
        query = query.filter_by(is_archived=False, is_done=False)
        
    if search_query:
        search_term = f"%{search_query.strip()}%"
        query = query.filter(
            db.or_(
                Note.title.ilike(search_term),
                Note.content.ilike(search_term)
            )
        )
        
    if color and color != 'all':
        query = query.filter_by(color=color)
        
    if priority and priority != 'all':
        query = query.filter_by(priority=priority)
        
    # Sort: Pinned first, then incomplete before completed, then updated_at descending
    notes = query.order_by(Note.is_done.asc(), Note.is_pinned.desc(), Note.updated_at.desc()).all()
    return notes

def create_note(user_id, data):
    """Create a new note."""
    title = (data.get('title') or '').strip()
    content = (data.get('content') or '').strip()
    if not content:
        raise ValueError("Note content cannot be empty.")
        
    color = data.get('color', 'default')
    priority = data.get('priority', 'medium')
    is_pinned = bool(data.get('is_pinned', False))
    reminder_at = parse_reminder_datetime(data.get('reminder_at'))
    
    note = Note(
        user_id=user_id,
        title=title if title else None,
        content=content,
        color=color,
        priority=priority,
        is_pinned=is_pinned,
        is_done=False,
        is_archived=False,
        reminder_at=reminder_at,
        reminder_seen=False
    )
    db.session.add(note)
    db.session.commit()
    logger.info(f"User {user_id} created note ID {note.id}")
    return note

def update_note(note_id, user_id, data):
    """Update an existing note ensuring user ownership."""
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return None
        
    content = data.get('content')
    if content is not None:
        content = content.strip()
        if not content:
            raise ValueError("Note content cannot be empty.")
        note.content = content
        
    if 'title' in data:
        note.title = (data.get('title') or '').strip() or None
    if 'color' in data:
        note.color = data.get('color') or 'default'
    if 'priority' in data:
        note.priority = data.get('priority') or 'medium'
    if 'is_pinned' in data:
        note.is_pinned = bool(data.get('is_pinned'))
    if 'is_archived' in data:
        note.is_archived = bool(data.get('is_archived'))
    if 'is_done' in data:
        note.is_done = bool(data.get('is_done'))
        if note.is_done:
            note.completed_at = now_ist().replace(tzinfo=None)
            note.reminder_seen = True
        else:
            note.completed_at = None
        
    if 'reminder_at' in data:
        new_reminder = parse_reminder_datetime(data.get('reminder_at'))
        if new_reminder != note.reminder_at:
            note.reminder_at = new_reminder
            note.reminder_seen = False # reset seen status if reminder changed
            
    note.updated_at = now_ist().replace(tzinfo=None)
    db.session.commit()
    logger.info(f"User {user_id} updated note ID {note.id}")
    return note

def delete_note(note_id, user_id):
    """Delete a note permanently."""
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return False
    db.session.delete(note)
    db.session.commit()
    logger.info(f"User {user_id} deleted note ID {note_id}")
    return True

def toggle_done(note_id, user_id):
    """Toggle the completed (done) state of a note."""
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return None
    note.is_done = not note.is_done
    if note.is_done:
        note.completed_at = now_ist().replace(tzinfo=None)
        note.reminder_seen = True # silence active reminder
    else:
        note.completed_at = None
        if note.reminder_at and note.reminder_at > now_ist().replace(tzinfo=None):
            note.reminder_seen = False
    note.updated_at = now_ist().replace(tzinfo=None)
    db.session.commit()
    logger.info(f"User {user_id} toggled done status for note {note_id}: {note.is_done}")
    return note

def toggle_pin(note_id, user_id):
    """Toggle the pinned state of a note."""
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return None
    note.is_pinned = not note.is_pinned
    note.updated_at = now_ist().replace(tzinfo=None)
    db.session.commit()
    return note

def toggle_archive(note_id, user_id):
    """Toggle the archived state of a note."""
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return None
    note.is_archived = not note.is_archived
    note.updated_at = now_ist().replace(tzinfo=None)
    db.session.commit()
    return note

def dismiss_reminder(note_id, user_id):
    """Mark reminder as seen / dismissed."""
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return False
    note.reminder_seen = True
    db.session.commit()
    return True

def snooze_reminder(note_id, user_id, minutes=15):
    """Snooze a reminder by adding minutes from current time."""
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return None
    curr_time = now_ist().replace(tzinfo=None)
    note.reminder_at = curr_time + timedelta(minutes=int(minutes))
    note.reminder_seen = False
    note.updated_at = curr_time
    db.session.commit()
    logger.info(f"User {user_id} snoozed note {note_id} by {minutes} mins")
    return note

def get_due_reminders_for_user(user_id):
    """Return all notes with active due reminders."""
    curr_time = now_ist().replace(tzinfo=None)
    return Note.query.filter(
        Note.user_id == user_id,
        Note.is_archived == False,
        Note.is_done == False,
        Note.reminder_at.isnot(None),
        Note.reminder_at <= curr_time,
        Note.reminder_seen == False
    ).order_by(Note.reminder_at.asc()).all()

def get_upcoming_reminders_for_user(user_id, limit=5):
    """Return upcoming reminders for dropdown preview."""
    curr_time = now_ist().replace(tzinfo=None)
    return Note.query.filter(
        Note.user_id == user_id,
        Note.is_archived == False,
        Note.is_done == False,
        Note.reminder_at.isnot(None),
        Note.reminder_at > curr_time
    ).order_by(Note.reminder_at.asc()).limit(limit).all()

def get_pending_reminders_context(current_user):
    """Context processor helper for template injection across all pages."""
    if not current_user or not getattr(current_user, 'is_authenticated', False):
        return {
            'has_pending_reminders': False,
            'pending_reminders_count': 0,
            'active_notes_count': 0,
            'upcoming_reminders_count': 0
        }
    try:
        curr_time = now_ist().replace(tzinfo=None)
        due_count = Note.query.filter(
            Note.user_id == current_user.user_id,
            Note.is_archived == False,
            Note.is_done == False,
            Note.reminder_at.isnot(None),
            Note.reminder_at <= curr_time,
            Note.reminder_seen == False
        ).count()
        
        active_notes = Note.query.filter_by(
            user_id=current_user.user_id,
            is_archived=False,
            is_done=False
        ).count()
        
        upcoming_count = Note.query.filter(
            Note.user_id == current_user.user_id,
            Note.is_archived == False,
            Note.is_done == False,
            Note.reminder_at.isnot(None),
            Note.reminder_at > curr_time
        ).count()

        return {
            'has_pending_reminders': due_count > 0,
            'pending_reminders_count': due_count,
            'active_notes_count': active_notes,
            'upcoming_reminders_count': upcoming_count
        }
    except Exception as e:
        logger.debug(f"Error computing pending reminders context: {e}")
        return {
            'has_pending_reminders': False,
            'pending_reminders_count': 0,
            'active_notes_count': 0,
            'upcoming_reminders_count': 0
        }
