import logging
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from services.notes_service import (
    get_notes_for_user,
    get_notes_counts,
    create_note,
    update_note,
    delete_note,
    toggle_done,
    toggle_pin,
    toggle_archive,
    dismiss_reminder,
    snooze_reminder,
    get_due_reminders_for_user,
    get_upcoming_reminders_for_user
)

logger = logging.getLogger(__name__)

notes_bp = Blueprint('notes', __name__, url_prefix='/api/notes')

@notes_bp.route('', methods=['GET'])
@login_required
def list_notes():
    """Retrieve filtered notes and counts for current user."""
    filter_type = request.args.get('filter', 'all')
    search_query = request.args.get('search')
    color = request.args.get('color')
    priority = request.args.get('priority')
    
    notes = get_notes_for_user(
        user_id=current_user.user_id,
        filter_type=filter_type,
        search_query=search_query,
        color=color,
        priority=priority
    )
    counts = get_notes_counts(current_user.user_id)
    
    return jsonify({
        'success': True,
        'notes': [n.to_dict() for n in notes],
        'counts': counts
    })

@notes_bp.route('', methods=['POST'])
@login_required
def add_note():
    """Create a new note for the current user."""
    data = request.get_json(silent=True) or request.form.to_dict()
    try:
        note = create_note(current_user.user_id, data)
        counts = get_notes_counts(current_user.user_id)
        return jsonify({
            'success': True,
            'message': 'Note created successfully!',
            'note': note.to_dict(),
            'counts': counts
        }), 201
    except ValueError as ve:
        return jsonify({'success': False, 'message': str(ve)}), 400
    except Exception as e:
        logger.exception("Failed to create note")
        return jsonify({'success': False, 'message': 'An error occurred while creating note.'}), 500

@notes_bp.route('/<int:note_id>', methods=['GET'])
@login_required
def get_single_note(note_id):
    """Retrieve a single note."""
    from models.notes import Note
    note = Note.query.filter_by(id=note_id, user_id=current_user.user_id).first()
    if not note:
        return jsonify({'success': False, 'message': 'Note not found'}), 404
    return jsonify({'success': True, 'note': note.to_dict()})

@notes_bp.route('/<int:note_id>', methods=['PUT'])
@notes_bp.route('/<int:note_id>/update', methods=['POST'])
@login_required
def edit_note(note_id):
    """Update note details."""
    data = request.get_json(silent=True) or request.form.to_dict()
    try:
        note = update_note(note_id, current_user.user_id, data)
        if not note:
            return jsonify({'success': False, 'message': 'Note not found or access denied'}), 404
        counts = get_notes_counts(current_user.user_id)
        return jsonify({
            'success': True,
            'message': 'Note updated successfully!',
            'note': note.to_dict(),
            'counts': counts
        })
    except ValueError as ve:
        return jsonify({'success': False, 'message': str(ve)}), 400
    except Exception as e:
        logger.exception(f"Failed to update note {note_id}")
        return jsonify({'success': False, 'message': 'Failed to update note.'}), 500

@notes_bp.route('/<int:note_id>/toggle-done', methods=['POST'])
@login_required
def toggle_note_done(note_id):
    """Toggle completion status for a note."""
    note = toggle_done(note_id, current_user.user_id)
    if not note:
        return jsonify({'success': False, 'message': 'Note not found or access denied'}), 404
    counts = get_notes_counts(current_user.user_id)
    return jsonify({
        'success': True,
        'is_done': note.is_done,
        'message': 'Marked as completed!' if note.is_done else 'Restored to active!',
        'note': note.to_dict(),
        'counts': counts
    })

@notes_bp.route('/<int:note_id>/delete', methods=['POST', 'DELETE'])
@login_required
def remove_note(note_id):
    """Delete a note."""
    success = delete_note(note_id, current_user.user_id)
    if not success:
        return jsonify({'success': False, 'message': 'Note not found or access denied'}), 404
    counts = get_notes_counts(current_user.user_id)
    return jsonify({
        'success': True,
        'message': 'Note deleted successfully!',
        'counts': counts
    })

@notes_bp.route('/<int:note_id>/pin', methods=['POST'])
@login_required
def pin_note(note_id):
    """Toggle note pin status."""
    note = toggle_pin(note_id, current_user.user_id)
    if not note:
        return jsonify({'success': False, 'message': 'Note not found or access denied'}), 404
    counts = get_notes_counts(current_user.user_id)
    return jsonify({
        'success': True,
        'is_pinned': note.is_pinned,
        'note': note.to_dict(),
        'counts': counts
    })

@notes_bp.route('/<int:note_id>/archive', methods=['POST'])
@login_required
def archive_note(note_id):
    """Toggle note archive status."""
    note = toggle_archive(note_id, current_user.user_id)
    if not note:
        return jsonify({'success': False, 'message': 'Note not found or access denied'}), 404
    counts = get_notes_counts(current_user.user_id)
    return jsonify({
        'success': True,
        'is_archived': note.is_archived,
        'note': note.to_dict(),
        'counts': counts
    })

@notes_bp.route('/<int:note_id>/dismiss-reminder', methods=['POST'])
@login_required
def dismiss_note_reminder(note_id):
    """Dismiss a due reminder."""
    success = dismiss_reminder(note_id, current_user.user_id)
    if not success:
        return jsonify({'success': False, 'message': 'Note not found or access denied'}), 404
    counts = get_notes_counts(current_user.user_id)
    return jsonify({
        'success': True,
        'message': 'Reminder marked as seen',
        'counts': counts
    })

@notes_bp.route('/<int:note_id>/snooze', methods=['POST'])
@login_required
def snooze_note_reminder(note_id):
    """Snooze a note reminder by specified minutes (default 15)."""
    data = request.get_json(silent=True) or request.form.to_dict()
    minutes = data.get('minutes', 15)
    try:
        minutes = int(minutes)
    except (ValueError, TypeError):
        minutes = 15

    note = snooze_reminder(note_id, current_user.user_id, minutes=minutes)
    if not note:
        return jsonify({'success': False, 'message': 'Note not found or access denied'}), 404
    counts = get_notes_counts(current_user.user_id)
    return jsonify({
        'success': True,
        'message': f'Reminder snoozed for {minutes} minutes',
        'note': note.to_dict(),
        'counts': counts
    })

@notes_bp.route('/summary', methods=['GET'])
@login_required
def notes_summary():
    """Return counts, due reminders, and upcoming reminders for the global navbar and background worker."""
    counts = get_notes_counts(current_user.user_id)
    due_reminders = get_due_reminders_for_user(current_user.user_id)
    upcoming_reminders = get_upcoming_reminders_for_user(current_user.user_id, limit=5)
    return jsonify({
        'success': True,
        'counts': counts,
        'due_reminders': [n.to_dict() for n in due_reminders],
        'upcoming_reminders': [n.to_dict() for n in upcoming_reminders]
    })
