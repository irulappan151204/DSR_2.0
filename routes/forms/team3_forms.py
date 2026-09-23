# routes/forms/team3_forms.py
from flask import request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
from extensions import db
from critical import can_audit
from models import Team3Audit, Team3NewAudit, FileStorage

def register_team3_forms(app):
    """Register all Team 3 (Audit) form submission routes."""
    @app.route('/submit_team3_audit', methods=['POST'])
    @login_required
    def submit_team3_audit():
        # Audit DSR rows may only be filed by the audit team (or MD/Admin); this
        # endpoint previously accepted submissions from any logged-in user.
        if not can_audit(current_user):
            return jsonify({'error': 'You are not authorized to submit audit data.'}), 403
        try:
            frequencies = request.form.getlist('frequency[]')
            components = request.form.getlist('audit_components[]')
            audit_bys = request.form.getlist('audit_by[]')
            times = request.form.getlist('audit_time[]')
            issues = request.form.getlist('issue_nature[]')
            remarks = request.form.getlist('audit_remarks[]')

            for i in range(len(frequencies)):
                if not frequencies[i] or not components[i] or not audit_bys[i] or not times[i] or not issues[i]:
                    continue  # skip incomplete rows

                audit_entry = Team3Audit(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    frequency=frequencies[i],
                    audit_components=components[i],
                    audit_by=audit_bys[i],
                    audit_time=times[i],
                    issue_nature=issues[i],
                    audit_remarks=remarks[i]
                )
                db.session.add(audit_entry)

            db.session.commit()
            return jsonify({'message': 'Team 3 audit data submitted successfully!'})
        except Exception:
            db.session.rollback()
            app.logger.exception('Error submitting audit')
            return jsonify({'error': 'Failed to submit audit.'}), 500


    @app.route('/submit_new_audit', methods=['POST'])
    @login_required
    def submit_new_audit():
        # Same restriction as /submit_team3_audit: audit team, MD or Admin only.
        if not can_audit(current_user):
            return jsonify({'error': 'You are not authorized to submit audit data.'}), 403
        try:
            frequencies = request.form.getlist('frequency[]')
            components = request.form.getlist('component[]')
            audited_bys = request.form.getlist('audited_by[]')
            staff_names = request.form.getlist('staff_name[]')
            grades = request.form.getlist('grade[]')
            sections = request.form.getlist('section[]')
            specifications = request.form.getlist('specification[]')
            issues = request.form.getlist('issue_nature[]')
            remarks = request.form.getlist('remark[]')

            # Handle file uploads (one file per row, aligned by index)
            media_files = request.files.getlist('media_file[]')

            for i in range(len(frequencies)):
                # Skip empty/incomplete rows
                if not frequencies[i] or not components[i] or not audited_bys[i] or not grades[i] or not sections[i] or not issues[i]:
                    continue

                media_file_id = None
                # Attach file if provided for this row
                if i < len(media_files):
                    file = media_files[i]
                    if file and file.filename:
                        # Max 200MB guard
                        file.seek(0, 2)
                        file_size = file.tell()
                        file.seek(0)
                        if file_size > 200 * 1024 * 1024:
                            return jsonify({'error': f'File {file.filename} is too large. Maximum size is 200MB.'}), 400

                        file_data = file.read()
                        original_filename = secure_filename(file.filename)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{timestamp}_{original_filename}"
                        mime_type = file.content_type or 'application/octet-stream'

                        file_record = FileStorage(
                            filename=filename,
                            original_filename=original_filename,
                            file_data=file_data,
                            file_size=file_size,
                            mime_type=mime_type,
                            uploaded_by=current_user.user_id
                        )
                        db.session.add(file_record)
                        db.session.flush()
                        media_file_id = file_record.file_id

                audit_entry = Team3NewAudit(
                    team_id=current_user.team_id,
                    submitted_by=current_user.user_id,
                    frequency=frequencies[i],
                    component=components[i],
                    audited_by=audited_bys[i],
                    staff_name=staff_names[i],
                    grade=grades[i],
                    section=sections[i],
                    specification=specifications[i],
                    issue_nature=issues[i],
                    remark=remarks[i],
                    media_file_id=media_file_id
                )
                db.session.add(audit_entry)

            db.session.commit()
            return jsonify({'message': 'New audit data submitted successfully!'})
        except Exception:
            db.session.rollback()
            app.logger.exception('Error submitting new audit')
            return jsonify({'error': 'Failed to submit new audit.'}), 500


