"""
File Classification System
Classifies uploaded files based on their content type and properties
"""

import os
import mimetypes
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
import json


class FileClassifier:
    """Classifies files based on content type and metadata"""
    
    # Category definitions based on MIME types and extensions
    CATEGORIES = {
        'documents': {
            'mime_types': ['application/pdf', 'application/msword', 
                          'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                          'application/vnd.ms-excel',
                          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                          'application/vnd.ms-powerpoint',
                          'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                          'text/plain', 'text/rtf'],
            'extensions': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf', '.odt', '.ods']
        },
        'images': {
            'mime_types': ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 
                          'image/svg+xml', 'image/webp', 'image/tiff'],
            'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff', '.tif', '.ico']
        },
        'videos': {
            'mime_types': ['video/mp4', 'video/mpeg', 'video/quicktime', 
                          'video/x-msvideo', 'video/x-matroska', 'video/webm'],
            'extensions': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm', '.m4v', '.mpg', '.mpeg']
        },
        'audio': {
            'mime_types': ['audio/mpeg', 'audio/wav', 'audio/ogg', 
                          'audio/webm', 'audio/aac', 'audio/flac'],
            'extensions': ['.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac', '.wma', '.opus']
        },
        'archives': {
            'mime_types': ['application/zip', 'application/x-rar-compressed', 
                          'application/x-tar', 'application/gzip', 
                          'application/x-7z-compressed'],
            'extensions': ['.zip', '.rar', '.tar', '.gz', '.7z', '.bz2', '.xz', '.tgz']
        },
        'code': {
            'mime_types': ['text/x-python', 'text/x-java', 'text/x-c', 
                          'text/html', 'text/css', 'application/javascript',
                          'application/json', 'application/xml'],
            'extensions': ['.py', '.java', '.c', '.cpp', '.h', '.hpp', '.js', '.ts', 
                          '.html', '.css', '.json', '.xml', '.php', '.rb', '.go', 
                          '.rs', '.swift', '.kt', '.sh', '.bash', '.sql', '.yaml', '.yml']
        },
        'data': {
            'mime_types': ['text/csv', 'application/json', 'application/xml',
                          'application/vnd.sqlite3'],
            'extensions': ['.csv', '.json', '.xml', '.db', '.sqlite', '.sql', '.parquet']
        }
    }
    
    def __init__(self, upload_dir: str = 'uploads'):
        """
        Initialize the FileClassifier
        
        Args:
            upload_dir: Base directory for uploaded files
        """
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
        
        # Create category subdirectories
        for category in self.CATEGORIES.keys():
            (self.upload_dir / category).mkdir(exist_ok=True)
        
        # Create an 'other' category for unclassified files
        (self.upload_dir / 'other').mkdir(exist_ok=True)
        
        # Metadata file to track uploaded files
        self.metadata_file = self.upload_dir / 'metadata.json'
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """Load metadata from file"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_metadata(self):
        """Save metadata to file"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def _calculate_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def classify_file(self, file_path: str) -> str:
        """
        Classify a file based on its MIME type and extension
        
        Args:
            file_path: Path to the file to classify
            
        Returns:
            Category name
        """
        # Get file extension and MIME type
        ext = Path(file_path).suffix.lower()
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # Check each category
        for category, rules in self.CATEGORIES.items():
            # Check MIME type
            if mime_type and mime_type in rules['mime_types']:
                return category
            
            # Check extension
            if ext in rules['extensions']:
                return category
        
        # Default to 'other' if no match
        return 'other'
    
    def upload_file(self, source_path: str, preserve_name: bool = True) -> Dict:
        """
        Upload and classify a file
        
        Args:
            source_path: Path to the source file
            preserve_name: Whether to preserve the original filename
            
        Returns:
            Dictionary with upload information
        """
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"File not found: {source_path}")
        
        # Get file info
        source_file = Path(source_path)
        file_name = source_file.name
        file_size = source_file.stat().st_size
        file_hash = self._calculate_hash(source_path)
        
        # Check if file already exists (by hash)
        if file_hash in self.metadata:
            return {
                'status': 'duplicate',
                'message': 'File already uploaded',
                'existing_file': self.metadata[file_hash]
            }
        
        # Classify the file
        category = self.classify_file(source_path)
        
        # Determine destination path
        if preserve_name:
            dest_name = file_name
        else:
            dest_name = f"{file_hash}{source_file.suffix}"
        
        dest_path = self.upload_dir / category / dest_name
        
        # Handle filename conflicts
        counter = 1
        original_dest_path = dest_path
        while dest_path.exists():
            stem = original_dest_path.stem
            suffix = original_dest_path.suffix
            dest_path = original_dest_path.parent / f"{stem}_{counter}{suffix}"
            counter += 1
        
        # Copy file to destination
        import shutil
        shutil.copy2(source_path, dest_path)
        
        # Store metadata
        file_info = {
            'original_name': file_name,
            'stored_name': dest_path.name,
            'category': category,
            'size': file_size,
            'hash': file_hash,
            'path': str(dest_path.relative_to(self.upload_dir))
        }
        
        self.metadata[file_hash] = file_info
        self._save_metadata()
        
        return {
            'status': 'success',
            'message': 'File uploaded and classified',
            'file_info': file_info
        }
    
    def list_files(self, category: Optional[str] = None) -> List[Dict]:
        """
        List uploaded files
        
        Args:
            category: Optional category filter
            
        Returns:
            List of file information dictionaries
        """
        files = list(self.metadata.values())
        
        if category:
            files = [f for f in files if f['category'] == category]
        
        return files
    
    def get_statistics(self) -> Dict:
        """Get statistics about uploaded files"""
        stats = {
            'total_files': len(self.metadata),
            'categories': {}
        }
        
        for file_info in self.metadata.values():
            category = file_info['category']
            if category not in stats['categories']:
                stats['categories'][category] = {
                    'count': 0,
                    'total_size': 0
                }
            stats['categories'][category]['count'] += 1
            stats['categories'][category]['total_size'] += file_info['size']
        
        return stats
