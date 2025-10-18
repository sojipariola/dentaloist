# routes/files.py
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models import FileRecord, db
import uuid
import os

files_bp = Blueprint('files', __name__, url_prefix='/api/files')

@files_bp.route('/', methods=['GET'])
@login_required
def get_files():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category')
        patient_id = request.args.get('patient_id')
        
        query = FileRecord.query
        
        if patient_id:
            query = query.filter(FileRecord.patient_id == patient_id)
        if category:
            query = query.filter(FileRecord.category == category)
        
        files = query.order_by(FileRecord.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'files': [file.to_dict() for file in files.items],
            'total': files.total,
            'pages': files.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@files_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        patient_id = request.form.get('patient_id')
        category = request.form.get('category', 'general')
        
        # Generate unique filename
        filename = f"{uuid.uuid4()}_{file.filename}"
        filepath = os.path.join('uploads', filename)
        
        # Save file
        file.save(filepath)
        
        # Create file record
        file_record = FileRecord(
            name=file.filename,
            type=file.content_type,
            size=os.path.getsize(filepath),
            path=filepath,
            category=category,
            uploaded_by=current_user.id,
            patient_id=patient_id
        )
        
        db.session.add(file_record)
        db.session.commit()
        
        return jsonify({
            'message': 'File uploaded successfully',
            'file': file_record.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500