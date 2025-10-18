# backend/app/utils/file_storage.py

import os
import uuid
from datetime import datetime
from flask import current_app, send_file, abort, g
from werkzeug.utils import secure_filename
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from PIL import Image
import magic
import hashlib
from pathlib import Path
import logging
from io import BytesIO
from functools import wraps

logger = logging.getLogger(__name__)

class FileStorage:
    """Unified file storage interface supporting local and cloud storage"""
    
    def __init__(self, app=None):
        self.storage_type = 'local'  # default
        self.s3_client = None
        self.s3_bucket = None
        self.local_storage_path = None
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize file storage with Flask app configuration"""
        self.storage_type = app.config.get('FILE_STORAGE_TYPE', 'local')
        
        if self.storage_type == 's3':
            self._init_s3_storage(app)
        else:
            self._init_local_storage(app)
    
    def _init_s3_storage(self, app):
        """Initialize Amazon S3 storage"""
        try:
            self.s3_bucket = app.config.get('S3_BUCKET_NAME')
            aws_access_key = app.config.get('AWS_ACCESS_KEY_ID')
            aws_secret_key = app.config.get('AWS_SECRET_ACCESS_KEY')
            aws_region = app.config.get('AWS_REGION', 'us-east-1')
            
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=aws_region
            )
            
            # Test connection
            self.s3_client.head_bucket(Bucket=self.s3_bucket)
            logger.info("S3 storage initialized successfully")
            
        except (NoCredentialsError, ClientError) as e:
            logger.error(f"Failed to initialize S3 storage: {e}")
            # Fallback to local storage
            self.storage_type = 'local'
            self._init_local_storage(app)
    
    def _init_local_storage(self, app):
        """Initialize local file storage"""
        self.local_storage_path = app.config.get(
            'LOCAL_STORAGE_PATH', 
            os.path.join(app.instance_path, 'uploads')
        )
        
        # Create storage directory if it doesn't exist
        os.makedirs(self.local_storage_path, exist_ok=True)
        logger.info(f"Local storage initialized at: {self.local_storage_path}")
    
    def save_file(self, file, category, tenant_id, patient_id=None, subfolder=None):
        """
        Save a file with proper organization and security
        
        Args:
            file: File object from request
            category: File category (medical_records, scans, xrays, prescriptions, etc.)
            tenant_id: Organization/tenant ID
            patient_id: Patient ID (optional)
            subfolder: Additional subfolder (optional)
        
        Returns:
            dict: File metadata including storage path
        """
        try:
            # Validate file
            self._validate_file(file)
            
            # Generate secure filename
            original_filename = secure_filename(file.filename)
            file_extension = os.path.splitext(original_filename)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}{file_extension}"
            
            # Build storage path
            storage_path = self._build_storage_path(
                category, tenant_id, patient_id, subfolder, unique_filename
            )
            
            # Read file content
            file_content = file.read()
            
            # Generate file hash for integrity checking
            file_hash = self._generate_file_hash(file_content)
            
            # Process image files if needed
            if self._is_image_file(file_extension):
                file_content = self._process_image(file_content, file_extension)
            
            # Save file based on storage type
            if self.storage_type == 's3':
                final_path = self._save_to_s3(file_content, storage_path, file.content_type)
            else:
                final_path = self._save_to_local(file_content, storage_path)
            
            # Return file metadata
            return {
                'original_filename': original_filename,
                'storage_filename': unique_filename,
                'storage_path': final_path,
                'file_size': len(file_content),
                'mime_type': file.content_type,
                'file_hash': file_hash,
                'uploaded_at': datetime.utcnow().isoformat(),
                'storage_type': self.storage_type
            }
            
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise
    
    def get_file(self, storage_path, as_attachment=False):
        """
        Retrieve a file from storage
        
        Args:
            storage_path: Path where file is stored
            as_attachment: Whether to force download
        
        Returns:
            Flask response with file
        """
        try:
            if self.storage_type == 's3':
                return self._get_from_s3(storage_path, as_attachment)
            else:
                return self._get_from_local(storage_path, as_attachment)
                
        except FileNotFoundError:
            abort(404, "File not found")
        except Exception as e:
            logger.error(f"Error retrieving file: {e}")
            abort(500, "Failed to retrieve file")
    
    def delete_file(self, storage_path):
        """
        Delete a file from storage
        
        Args:
            storage_path: Path to file to delete
        """
        try:
            if self.storage_type == 's3':
                self._delete_from_s3(storage_path)
            else:
                self._delete_from_local(storage_path)
                
            logger.info(f"File deleted: {storage_path}")
            
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            raise
    
    def get_file_url(self, storage_path, expires_in=3600):
        """
        Generate a presigned URL for temporary file access (S3 only)
        
        Args:
            storage_path: Path to file
            expires_in: URL expiration time in seconds
        
        Returns:
            str: Presigned URL or None if not using S3
        """
        if self.storage_type != 's3':
            return None
        
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.s3_bucket,
                    'Key': storage_path
                },
                ExpiresIn=expires_in
            )
            return url
        except Exception as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None
    
    def file_exists(self, storage_path):
        """Check if a file exists in storage"""
        try:
            if self.storage_type == 's3':
                self.s3_client.head_object(Bucket=self.s3_bucket, Key=storage_path)
                return True
            else:
                return os.path.exists(os.path.join(self.local_storage_path, storage_path))
        except:
            return False
    
    def _build_storage_path(self, category, tenant_id, patient_id, subfolder, filename):
        """
        Build organized storage path structure
        Format: {category}/{tenant_id}/{patient_id}/{subfolder}/{filename}
        """
        path_parts = [category, str(tenant_id)]
        
        if patient_id:
            path_parts.append(str(patient_id))
        
        if subfolder:
            path_parts.append(subfolder)
        
        path_parts.append(filename)
        return os.path.join(*path_parts)
    
    def _validate_file(self, file):
        """Validate file for security and size constraints"""
        if not file or file.filename == '':
            raise ValueError("No file provided")
        
        # Check file size
        max_size = current_app.config.get('MAX_FILE_SIZE', 50 * 1024 * 1024)  # 50MB default
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > max_size:
            raise ValueError(f"File size exceeds maximum allowed size of {max_size} bytes")
        
        # Check file type
        allowed_mime_types = current_app.config.get(
            'ALLOWED_MIME_TYPES', 
            [
                'image/jpeg', 'image/png', 'image/gif', 'image/tiff',
                'application/pdf', 
                'text/plain',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            ]
        )
        
        # Read first 2048 bytes for MIME type detection
        file_content = file.read(2048)
        file.seek(0)
        
        mime_type = magic.from_buffer(file_content, mime=True)
        if mime_type not in allowed_mime_types:
            raise ValueError(f"File type {mime_type} not allowed")
    
    def _generate_file_hash(self, file_content):
        """Generate SHA-256 hash of file content for integrity checking"""
        return hashlib.sha256(file_content).hexdigest()
    
    def _is_image_file(self, file_extension):
        """Check if file is an image based on extension"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp'}
        return file_extension.lower() in image_extensions
    
    def _process_image(self, file_content, file_extension):
        """
        Process image files (resize, compress, etc.)
        """
        try:
            if current_app.config.get('PROCESS_IMAGES', True):
                image = Image.open(BytesIO(file_content))
                
                # Resize if too large
                max_dimension = current_app.config.get('MAX_IMAGE_DIMENSION', 2048)
                if max(image.size) > max_dimension:
                    image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
                
                # Convert to appropriate format and compress
                output_buffer = BytesIO()
                
                if file_extension in ['.jpg', '.jpeg']:
                    image.save(output_buffer, format='JPEG', quality=85, optimize=True)
                elif file_extension == '.png':
                    image.save(output_buffer, format='PNG', optimize=True)
                else:
                    # For other formats, save as is
                    return file_content
                
                return output_buffer.getvalue()
            
            return file_content
            
        except Exception as e:
            logger.warning(f"Image processing failed: {e}")
            return file_content  # Return original if processing fails
    
    def _save_to_s3(self, file_content, storage_path, content_type):
        """Save file to Amazon S3"""
        try:
            self.s3_client.put_object(
                Bucket=self.s3_bucket,
                Key=storage_path,
                Body=file_content,
                ContentType=content_type,
                ACL='private'  # Private by default for medical data
            )
            return storage_path
        except Exception as e:
            logger.error(f"S3 upload failed: {e}")
            raise
    
    def _save_to_local(self, file_content, storage_path):
        """Save file to local storage"""
        try:
            full_path = os.path.join(self.local_storage_path, storage_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'wb') as f:
                f.write(file_content)
            
            return storage_path
        except Exception as e:
            logger.error(f"Local file save failed: {e}")
            raise
    
    def _get_from_s3(self, storage_path, as_attachment):
        """Retrieve file from Amazon S3"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.s3_bucket,
                Key=storage_path
            )
            
            file_content = response['Body'].read()
            mime_type = response['ContentType']
            
            return self._create_file_response(file_content, storage_path, mime_type, as_attachment)
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise FileNotFoundError(f"File not found in S3: {storage_path}")
            raise
    
    def _get_from_local(self, storage_path, as_attachment):
        """Retrieve file from local storage"""
        try:
            full_path = os.path.join(self.local_storage_path, storage_path)
            
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"File not found: {full_path}")
            
            # Determine MIME type
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(full_path)
            
            return send_file(
                full_path,
                mimetype=mime_type,
                as_attachment=as_attachment,
                download_name=os.path.basename(storage_path)
            )
            
        except FileNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Local file retrieval failed: {e}")
            raise
    
    def _delete_from_s3(self, storage_path):
        """Delete file from Amazon S3"""
        try:
            self.s3_client.delete_object(
                Bucket=self.s3_bucket,
                Key=storage_path
            )
        except Exception as e:
            logger.error(f"S3 delete failed: {e}")
            raise
    
    def _delete_from_local(self, storage_path):
        """Delete file from local storage"""
        try:
            full_path = os.path.join(self.local_storage_path, storage_path)
            if os.path.exists(full_path):
                os.remove(full_path)
        except Exception as e:
            logger.error(f"Local file delete failed: {e}")
            raise
    
    def _create_file_response(self, file_content, filename, mime_type, as_attachment):
        """Create Flask response for file content"""
        from flask import Response
        
        response = Response(file_content, mimetype=mime_type)
        
        if as_attachment:
            response.headers['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'
        else:
            response.headers['Content-Disposition'] = f'inline; filename="{os.path.basename(filename)}"'
        
        response.headers['Content-Length'] = str(len(file_content))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response

# Global file storage instance
file_storage = FileStorage()

# Convenience functions
def save_medical_file(file, category, tenant_id, patient_id=None, subfolder=None):
    """Convenience function to save medical files"""
    return file_storage.save_file(file, category, tenant_id, patient_id, subfolder)

def get_medical_file(storage_path, as_attachment=False):
    """Convenience function to retrieve medical files"""
    return file_storage.get_file(storage_path, as_attachment)

def delete_medical_file(storage_path):
    """Convenience function to delete medical files"""
    return file_storage.delete_file(storage_path)

def get_medical_file_url(storage_path, expires_in=3600):
    """Convenience function to get file URL"""
    return file_storage.get_file_url(storage_path, expires_in)

def medical_file_exists(storage_path):
    """Convenience function to check if file exists"""
    return file_storage.file_exists(storage_path)

# Decorator for file operation permissions
def require_file_permission(permission):
    """Decorator to check file access permissions"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Implement your permission checking logic here
            # For example, check if user has access to the specific file
            storage_path = kwargs.get('storage_path')
            if storage_path and not _check_file_access(storage_path, g.user):
                abort(403, "Access to file denied")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def _check_file_access(storage_path, user):
    """Check if user has access to a specific file"""
    # Extract information from storage path
    # Format: {category}/{tenant_id}/{patient_id}/{subfolder}/{filename}
    path_parts = storage_path.split('/')
    
    if len(path_parts) < 2:
        return False
    
    category, tenant_id = path_parts[0], path_parts[1]
    
    # Check tenant access
    if str(user.organization_id) != tenant_id:
        return False
    
    # Additional permission checks based on category and user role
    if category == 'medical_records':
        return user.has_permission('view_clinical_records')
    elif category == 'scans' or category == 'xrays':
        return user.has_permission('view_medical_images')
    # Add more category-specific checks as needed
    
    return user.has_permission('view_files')

# Configuration helper
def configure_file_storage(app):
    """Configure file storage with app settings"""
    app.config.setdefault('FILE_STORAGE_TYPE', 'local')
    app.config.setdefault('LOCAL_STORAGE_PATH', os.path.join(app.instance_path, 'uploads'))
    app.config.setdefault('MAX_FILE_SIZE', 50 * 1024 * 1024)  # 50MB
    app.config.setdefault('ALLOWED_MIME_TYPES', [
        'image/jpeg', 'image/png', 'image/gif', 'image/tiff', 'image/bmp',
        'application/pdf', 
        'text/plain',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ])
    app.config.setdefault('PROCESS_IMAGES', True)
    app.config.setdefault('MAX_IMAGE_DIMENSION', 2048)
    
    file_storage.init_app(app)



'''
# In your routes files

from app.utils.file_storage import save_medical_file, get_medical_file, delete_medical_file, require_file_permission

@bp.route('/upload-medical-record', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_clinical_records'])
def upload_medical_record_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    patient_id = request.form.get('patient_id')
    
    try:
        file_metadata = save_medical_file(
            file=file,
            category='medical_records',
            tenant_id=g.tenant_id,
            patient_id=patient_id,
            subfolder='attachments'
        )
        
        return jsonify({
            'message': 'File uploaded successfully',
            'file': file_metadata
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'File upload failed'}), 500

@bp.route('/files/<path:storage_path>', methods=['GET'])
@jwt_required()
@require_file_permission('view_files')
def download_file(storage_path):
    as_attachment = request.args.get('download', 'false').lower() == 'true'
    return get_medical_file(storage_path, as_attachment=as_attachment)

@bp.route('/files/<path:storage_path>', methods=['DELETE'])
@jwt_required()
@require_file_permission('manage_files')
def delete_file(storage_path):
    try:
        delete_medical_file(storage_path)
        return jsonify({'message': 'File deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'File deletion failed'}), 500

'''