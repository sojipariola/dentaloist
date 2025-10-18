import os
import uuid
from flask import current_app, request, g, jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from datetime import datetime
from typing import Dict, Any, List, Optional
import imghdr
from werkzeug.utils import secure_filename
from datetime import timedelta

# Import auth and tenancy utilities
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit
from models import db

upload_bp = Blueprint("Uploads", __name__, url_prefix="/uploads", description="File uploads & AI analysis")

# RBAC Permission Constants
PERMISSION_UPLOAD_FILES = 'upload_files'
PERMISSION_VIEW_UPLOADS = 'view_uploads'
PERMISSION_DELETE_UPLOADS = 'delete_uploads'
PERMISSION_ANALYZE_IMAGES = 'analyze_images'

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'rtf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def analyze_image_placeholder(filepath: str, tenant_id: str, user_id: int) -> dict:
    """Enhanced image analysis with tenant context"""
    # In production, this would integrate with actual AI services
    return {
        "analysis_id": str(uuid.uuid4()),
        "findings": ["No obvious caries", "Recommend further review"],
        "confidence": 0.65,
        "analysis_type": "dental_xray",
        "timestamp": datetime.utcnow().isoformat(),
        "analyzed_by": user_id,
        "tenant_id": tenant_id
    }

def allowed_file(filename: str, file_type: str = 'image') -> bool:
    """Check if file extension is allowed"""
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    if file_type == 'image':
        return ext in ALLOWED_IMAGE_EXTENSIONS
    elif file_type == 'document':
        return ext in ALLOWED_DOCUMENT_EXTENSIONS
    else:
        return ext in ALLOWED_IMAGE_EXTENSIONS.union(ALLOWED_DOCUMENT_EXTENSIONS)

def validate_image_file(file_stream) -> Dict[str, Any]:
    """Validate image file integrity and type"""
    validation_result = {
        'is_valid': True,
        'errors': [],
        'file_type': None,
        'dimensions': None
    }
    
    # Check file signature
    file_type = imghdr.what(None, h=file_stream.read(1024))
    file_stream.seek(0)  # Reset stream position
    
    if not file_type:
        validation_result['is_valid'] = False
        validation_result['errors'].append('Invalid image file format')
        return validation_result
    
    validation_result['file_type'] = file_type
    
    # Basic size validation (prevent extremely large images)
    file_stream.seek(0, 2)  # Seek to end
    file_size = file_stream.tell()
    file_stream.seek(0)  # Reset stream position
    
    if file_size > MAX_FILE_SIZE:
        validation_result['is_valid'] = False
        validation_result['errors'].append(f'File size exceeds maximum limit of {MAX_FILE_SIZE // (1024*1024)}MB')
    
    return validation_result

def get_upload_folder(tenant_id: str, file_type: str = 'images') -> str:
    """Get upload folder path for tenant"""
    base_path = current_app.config.get("UPLOAD_FOLDER", "./uploads")
    tenant_folder = os.path.join(base_path, tenant_id, file_type)
    
    # Create directory if it doesn't exist
    os.makedirs(tenant_folder, exist_ok=True)
    
    return tenant_folder

def save_upload_metadata(tenant_id: str, user_id: int, filename: str, file_type: str, 
                        analysis_result: Dict[str, Any] = None) -> Dict[str, Any]:
    """Save upload metadata to database"""
    from ..models import FileUpload
    
    upload = FileUpload(
        tenant_id=tenant_id,
        user_id=user_id,
        filename=filename,
        original_filename=analysis_result.get('original_filename', '') if analysis_result else '',
        file_type=file_type,
        file_size=analysis_result.get('file_size', 0) if analysis_result else 0,
        mime_type=analysis_result.get('mime_type', ''),
        analysis_result=analysis_result,
        uploaded_at=datetime.utcnow()
    )
    
    db.session.add(upload)
    db.session.commit()
    
    return upload.to_dict()

@upload_bp.route("")
class UploadImage(MethodView):
    @rate_limit(limit=20, period=3600)  # 20 uploads per hour
    @jwt_required()
    @tenant_required
    @permission_required(PERMISSION_UPLOAD_FILES)
    def post(self):
        """
        Upload file with tenant isolation and AI analysis
        """
        try:
            current_user_obj = get_current_user()
            tenant_id = current_user_obj.tenant_id
            user_id = current_user_obj.id
            
            if "file" not in request.files:
                abort(400, message="No file part in request")
            
            f = request.files["file"]
            if f.filename == "":
                abort(400, message="Empty filename")
            
            # Secure filename and validate
            original_filename = secure_filename(f.filename)
            if not allowed_file(original_filename):
                abort(400, message=f"File type not allowed. Allowed types: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}")
            
            # Validate image file
            validation_result = validate_image_file(f.stream)
            if not validation_result['is_valid']:
                abort(400, message=f"File validation failed: {', '.join(validation_result['errors'])}")
            
            # Generate unique filename
            file_ext = original_filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4()}.{file_ext}"
            
            # Determine upload folder based on file type
            upload_folder = get_upload_folder(tenant_id, 'images')
            save_path = os.path.join(upload_folder, unique_filename)
            
            # Save file
            f.stream.seek(0)  # Reset stream after validation
            f.save(save_path)
            
            # Analyze image if user has permission
            analysis_result = None
            if current_user_obj.has_permission(PERMISSION_ANALYZE_IMAGES):
                analysis_result = analyze_image_placeholder(save_path, tenant_id, user_id)
            
            # Save upload metadata
            upload_metadata = {
                'original_filename': original_filename,
                'file_size': os.path.getsize(save_path),
                'mime_type': f'mime/{validation_result["file_type"]}',
                'file_type': validation_result["file_type"]
            }
            
            if analysis_result:
                upload_metadata.update(analysis_result)
            
            saved_metadata = save_upload_metadata(tenant_id, user_id, unique_filename, 'image', upload_metadata)
            
            # Create audit trail entry
            _create_audit_trail(tenant_id, user_id, 'upload', 'file', saved_metadata['id'], 
                               f'File uploaded: {original_filename}')
            
            return {
                "message": "File uploaded successfully",
                "upload": {
                    "id": saved_metadata['id'],
                    "filename": unique_filename,
                    "original_filename": original_filename,
                    "file_size": upload_metadata['file_size'],
                    "uploaded_at": saved_metadata['uploaded_at'],
                    "analysis": analysis_result,
                    "download_url": f"/uploads/{saved_metadata['id']}/download",
                    "tenant_id": tenant_id
                }
            }, 201
            
        except Exception as e:
            abort(500, message=f"Upload failed: {str(e)}")

@upload_bp.route("/<upload_id>")
class UploadManagement(MethodView):
    @rate_limit(limit=100, period=3600)
    @jwt_required()
    @tenant_required
    @permission_required(PERMISSION_VIEW_UPLOADS)
    def get(self, upload_id):
        """
        Get upload metadata by ID with tenant isolation
        """
        try:
            current_user_obj = get_current_user()
            tenant_id = current_user_obj.tenant_id
            
            from ..models import FileUpload
            query = multi_tenant_query(FileUpload.query, tenant_id)
            upload = query.filter_by(id=upload_id).first()
            
            if not upload:
                abort(404, message="Upload not found")
            
            return {
                "upload": upload.to_dict(include_details=True)
            }, 200
            
        except Exception as e:
            abort(500, message=f"Failed to retrieve upload: {str(e)}")
    
    @rate_limit(limit=30, period=3600)
    @jwt_required()
    @tenant_required
    @permission_required(PERMISSION_DELETE_UPLOADS)
    def delete(self, upload_id):
        """
        Delete upload with tenant isolation
        """
        try:
            current_user_obj = get_current_user()
            tenant_id = current_user_obj.tenant_id
            user_id = current_user_obj.id
            
            from ..models import FileUpload
            query = multi_tenant_query(FileUpload.query, tenant_id)
            upload = query.filter_by(id=upload_id).first()
            
            if not upload:
                abort(404, message="Upload not found")
            
            # Delete physical file
            file_path = os.path.join(get_upload_folder(tenant_id, upload.file_type), upload.filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Create audit trail before deletion
            _create_audit_trail(tenant_id, user_id, 'delete', 'file', upload.id, 
                               f'File deleted: {upload.original_filename}')
            
            # Delete database record
            db.session.delete(upload)
            db.session.commit()
            
            return {
                "message": "Upload deleted successfully",
                "deleted_id": upload_id
            }, 200
            
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Failed to delete upload: {str(e)}")

@upload_bp.route("/<upload_id>/download")
class DownloadUpload(MethodView):
    @rate_limit(limit=60, period=3600)
    @jwt_required()
    @tenant_required
    @permission_required(PERMISSION_VIEW_UPLOADS)
    def get(self, upload_id):
        """
        Download uploaded file with tenant isolation
        """
        try:
            current_user_obj = get_current_user()
            tenant_id = current_user_obj.tenant_id
            
            from ..models import FileUpload
            query = multi_tenant_query(FileUpload.query, tenant_id)
            upload = query.filter_by(id=upload_id).first()
            
            if not upload:
                abort(404, message="Upload not found")
            
            file_path = os.path.join(get_upload_folder(tenant_id, upload.file_type), upload.filename)
            
            if not os.path.exists(file_path):
                abort(404, message="File not found on server")
            
            # Create audit trail entry
            _create_audit_trail(tenant_id, current_user_obj.id, 'download', 'file', upload.id, 
                               f'File downloaded: {upload.original_filename}')
            
            # In a real implementation, you'd use send_file or similar
            return {
                "message": "Download ready",
                "download_url": f"/protected/{tenant_id}/files/{upload.filename}",
                "filename": upload.original_filename,
                "mime_type": upload.mime_type
            }, 200
            
        except Exception as e:
            abort(500, message=f"Download failed: {str(e)}")

@upload_bp.route("/<upload_id>/analyze")
class AnalyzeImage(MethodView):
    @rate_limit(limit=10, period=3600)  # Limit analysis requests
    @jwt_required()
    @tenant_required
    @permission_required(PERMISSION_ANALYZE_IMAGES)
    def post(self, upload_id):
        """
        Analyze uploaded image with AI
        """
        try:
            current_user_obj = get_current_user()
            tenant_id = current_user_obj.tenant_id
            user_id = current_user_obj.id
            
            from ..models import FileUpload
            query = multi_tenant_query(FileUpload.query, tenant_id)
            upload = query.filter_by(id=upload_id).first()
            
            if not upload:
                abort(404, message="Upload not found")
            
            if upload.file_type != 'image':
                abort(400, message="Analysis only available for image files")
            
            file_path = os.path.join(get_upload_folder(tenant_id, upload.file_type), upload.filename)
            
            if not os.path.exists(file_path):
                abort(404, message="File not found on server")
            
            # Perform analysis
            analysis_result = analyze_image_placeholder(file_path, tenant_id, user_id)
            
            # Update upload record with analysis results
            upload.analysis_result = analysis_result
            upload.analyzed_at = datetime.utcnow()
            upload.analyzed_by = user_id
            db.session.commit()
            
            # Create audit trail entry
            _create_audit_trail(tenant_id, user_id, 'analyze', 'file', upload.id, 
                               'Image analysis completed')
            
            return {
                "message": "Image analysis completed",
                "analysis": analysis_result,
                "upload_id": upload_id
            }, 200
            
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Analysis failed: {str(e)}")

@upload_bp.route("/list")
class ListUploads(MethodView):
    @rate_limit(limit=100, period=3600)
    @jwt_required()
    @tenant_required
    @permission_required(PERMISSION_VIEW_UPLOADS)
    def get(self):
        """
        List uploads with filtering and pagination
        """
        try:
            current_user_obj = get_current_user()
            tenant_id = current_user_obj.tenant_id
            
            # Pagination parameters
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 20, type=int), 100)
            
            # Filter parameters
            file_type = request.args.get('file_type')
            user_id = request.args.get('user_id', type=int)
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            
            from ..models import FileUpload
            query = multi_tenant_query(FileUpload.query, tenant_id)
            
            # Apply filters
            if file_type:
                query = query.filter(FileUpload.file_type == file_type)
            if user_id:
                query = query.filter(FileUpload.user_id == user_id)
            if start_date:
                try:
                    start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                    query = query.filter(FileUpload.uploaded_at >= start_dt)
                except ValueError:
                    abort(400, message="Invalid start_date format")
            if end_date:
                try:
                    end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                    query = query.filter(FileUpload.uploaded_at <= end_dt)
                except ValueError:
                    abort(400, message="Invalid end_date format")
            
            # Pagination
            uploads = query.order_by(FileUpload.uploaded_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            return {
                "uploads": [upload.to_dict() for upload in uploads.items],
                "pagination": {
                    "page": uploads.page,
                    "per_page": uploads.per_page,
                    "total": uploads.total,
                    "pages": uploads.pages
                },
                "filters": {
                    "file_type": file_type,
                    "user_id": user_id,
                    "start_date": start_date,
                    "end_date": end_date
                }
            }, 200
            
        except Exception as e:
            abort(500, message=f"Failed to list uploads: {str(e)}")

@upload_bp.route("/stats")
class UploadStats(MethodView):
    @rate_limit(limit=60, period=3600)
    @jwt_required()
    @tenant_required
    @permission_required(PERMISSION_VIEW_UPLOADS)
    def get(self):
        """
        Get upload statistics and analytics
        """
        try:
            current_user_obj = get_current_user()
            tenant_id = current_user_obj.tenant_id
            
            days = int(request.args.get('days', 30))
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            from ..models import FileUpload
            query = multi_tenant_query(FileUpload.query, tenant_id)
            uploads = query.filter(FileUpload.uploaded_at.between(start_date, end_date))
            
            stats = {
                "total_uploads": uploads.count(),
                "total_size_bytes": uploads.with_entities(db.func.sum(FileUpload.file_size)).scalar() or 0,
                "by_file_type": _get_uploads_by_type(tenant_id, start_date, end_date),
                "by_user": _get_uploads_by_user(tenant_id, start_date, end_date),
                "analysis_stats": _get_analysis_stats(tenant_id, start_date, end_date)
            }
            
            return {
                "stats": stats,
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "days": days
                }
            }, 200
            
        except Exception as e:
            abort(500, message=f"Failed to get upload stats: {str(e)}")

# Helper functions
def _create_audit_trail(tenant_id: str, user_id: int, action: str, resource_type: str, resource_id: int, details: str):
    """Create an audit trail entry"""
    from ..models import AuditTrail
    
    audit_entry = AuditTrail(
        tenant_id=tenant_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    
    db.session.add(audit_entry)

def _get_uploads_by_type(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, int]:
    """Get upload count by file type"""
    from ..models import FileUpload
    query = multi_tenant_query(FileUpload.query, tenant_id)
    type_counts = query.filter(FileUpload.uploaded_at.between(start_date, end_date))\
                      .group_by(FileUpload.file_type)\
                      .with_entities(FileUpload.file_type, db.func.count(FileUpload.id))\
                      .all()
    
    return {file_type: count for file_type, count in type_counts}

def _get_uploads_by_user(tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
    """Get upload statistics by user"""
    from ..models import FileUpload, User
    query = multi_tenant_query(FileUpload.query.join(User), tenant_id)
    user_stats = query.filter(FileUpload.uploaded_at.between(start_date, end_date))\
                     .group_by(User.id, User.first_name, User.last_name)\
                     .with_entities(
                         User.id,
                         User.first_name,
                         User.last_name,
                         db.func.count(FileUpload.id),
                         db.func.sum(FileUpload.file_size)
                     ).all()
    
    return [{
        'user_id': user_id,
        'user_name': f"{first_name} {last_name}",
        'upload_count': count,
        'total_size_bytes': total_size or 0
    } for user_id, first_name, last_name, count, total_size in user_stats]

def _get_analysis_stats(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get analysis statistics"""
    from ..models import FileUpload
    query = multi_tenant_query(FileUpload.query, tenant_id)
    analyzed_files = query.filter(
        FileUpload.uploaded_at.between(start_date, end_date),
        FileUpload.analysis_result.isnot(None)
    )
    
    total_analyzed = analyzed_files.count()
    total_uploads = query.filter(FileUpload.uploaded_at.between(start_date, end_date)).count()
    
    return {
        'analyzed_files': total_analyzed,
        'analysis_rate': (total_analyzed / total_uploads * 100) if total_uploads > 0 else 0,
        'recent_analyses': analyzed_files.order_by(FileUpload.analyzed_at.desc()).limit(5).count()
    }

# Error handlers
@upload_bp.errorhandler(400)
def handle_bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

@upload_bp.errorhandler(403)
def handle_forbidden(error):
    return jsonify({'error': 'Forbidden', 'message': 'Insufficient permissions'}), 403

@upload_bp.errorhandler(404)
def handle_not_found(error):
    return jsonify({'error': 'Not found', 'message': str(error)}), 404

@upload_bp.errorhandler(413)
def handle_payload_too_large(error):
    return jsonify({'error': 'File too large', 'message': 'File size exceeds maximum limit'}), 413

@upload_bp.errorhandler(429)
def handle_rate_limit_exceeded(error):
    return jsonify({'error': 'Rate limit exceeded', 'message': 'Too many requests'}), 429

@upload_bp.errorhandler(500)
def handle_internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500