import os
from io import BytesIO
from flask import send_file, send_from_directory, jsonify
from flask_login import login_required
from models import FileStorage

def register_files_routes(app):
    """Register file serving routes (database BLOB and legacy filesystem)."""
    @app.route('/file/<int:file_id>')
    @login_required
    def serve_file(file_id):
        """Serve uploaded files from database BLOB storage"""
        try:
            file_record = FileStorage.query.get_or_404(file_id)

            response = send_file(
                BytesIO(file_record.file_data),
                mimetype=file_record.mime_type,
                as_attachment=False,
                download_name=file_record.original_filename
            )
            response.headers['Cache-Control'] = 'public, max-age=31536000'
            return response
        except Exception:
            return jsonify({'error': 'File not found'}), 404

    @app.route('/uploads/<path:filename>')
    @login_required
    def serve_legacy_file(filename):
        """Serve uploaded files securely from filesystem (legacy)"""
        try:
            return send_from_directory(os.path.join(app.root_path, 'static', 'uploads'), filename)
        except Exception:
            return jsonify({'error': 'File not found'}), 404
