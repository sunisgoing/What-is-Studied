"""
Unit tests for the file classification system
"""

import unittest
import os
import tempfile
import shutil
from pathlib import Path
from file_classifier import FileClassifier


class TestFileClassifier(unittest.TestCase):
    """Test cases for FileClassifier"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary directory for tests
        self.test_dir = tempfile.mkdtemp()
        self.upload_dir = os.path.join(self.test_dir, 'uploads')
        self.classifier = FileClassifier(self.upload_dir)
        
        # Create test files
        self.test_files_dir = os.path.join(self.test_dir, 'test_files')
        os.makedirs(self.test_files_dir)
        
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)
    
    def create_test_file(self, filename: str, content: str = "test content") -> str:
        """Helper to create a test file"""
        filepath = os.path.join(self.test_files_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath
    
    def test_classify_document(self):
        """Test classification of document files"""
        test_file = self.create_test_file('test.pdf')
        category = self.classifier.classify_file(test_file)
        self.assertEqual(category, 'documents')
        
        test_file = self.create_test_file('test.txt')
        category = self.classifier.classify_file(test_file)
        self.assertEqual(category, 'documents')
        
        test_file = self.create_test_file('test.docx')
        category = self.classifier.classify_file(test_file)
        self.assertEqual(category, 'documents')
    
    def test_classify_image(self):
        """Test classification of image files"""
        test_file = self.create_test_file('image.jpg')
        category = self.classifier.classify_file(test_file)
        self.assertEqual(category, 'images')
        
        test_file = self.create_test_file('image.png')
        category = self.classifier.classify_file(test_file)
        self.assertEqual(category, 'images')
    
    def test_classify_code(self):
        """Test classification of code files"""
        test_file = self.create_test_file('script.py', 'print("hello")')
        category = self.classifier.classify_file(test_file)
        self.assertEqual(category, 'code')
        
        test_file = self.create_test_file('app.js')
        category = self.classifier.classify_file(test_file)
        self.assertEqual(category, 'code')
    
    def test_classify_archive(self):
        """Test classification of archive files"""
        test_file = self.create_test_file('archive.zip')
        category = self.classifier.classify_file(test_file)
        self.assertEqual(category, 'archives')
    
    def test_classify_audio(self):
        """Test classification of audio files"""
        test_file = self.create_test_file('song.mp3')
        category = self.classifier.classify_file(test_file)
        self.assertEqual(category, 'audio')
    
    def test_classify_video(self):
        """Test classification of video files"""
        test_file = self.create_test_file('movie.mp4')
        category = self.classifier.classify_file(test_file)
        self.assertEqual(category, 'videos')
    
    def test_classify_data(self):
        """Test classification of data files"""
        test_file = self.create_test_file('data.csv')
        category = self.classifier.classify_file(test_file)
        self.assertEqual(category, 'data')
        
        test_file = self.create_test_file('config.json')
        category = self.classifier.classify_file(test_file)
        self.assertEqual(category, 'code')  # JSON can be both code and data
    
    def test_classify_other(self):
        """Test classification of unknown file types"""
        test_file = self.create_test_file('unknown.xyz')
        category = self.classifier.classify_file(test_file)
        self.assertEqual(category, 'other')
    
    def test_upload_file(self):
        """Test uploading a file"""
        test_file = self.create_test_file('test.txt', 'Hello World')
        result = self.classifier.upload_file(test_file)
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['file_info']['category'], 'documents')
        self.assertEqual(result['file_info']['original_name'], 'test.txt')
        
        # Verify file was copied
        uploaded_path = Path(self.upload_dir) / result['file_info']['path']
        self.assertTrue(uploaded_path.exists())
    
    def test_duplicate_detection(self):
        """Test duplicate file detection"""
        test_file = self.create_test_file('test.txt', 'Same content')
        
        # Upload first time
        result1 = self.classifier.upload_file(test_file)
        self.assertEqual(result1['status'], 'success')
        
        # Try to upload same file again
        result2 = self.classifier.upload_file(test_file)
        self.assertEqual(result2['status'], 'duplicate')
    
    def test_list_files(self):
        """Test listing files"""
        # Upload some test files
        file1 = self.create_test_file('doc1.txt', 'content for document')
        file2 = self.create_test_file('image1.png', 'content for image')
        
        self.classifier.upload_file(file1)
        self.classifier.upload_file(file2)
        
        # List all files
        all_files = self.classifier.list_files()
        self.assertEqual(len(all_files), 2)
        
        # List by category
        docs = self.classifier.list_files(category='documents')
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]['original_name'], 'doc1.txt')
        
        images = self.classifier.list_files(category='images')
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0]['original_name'], 'image1.png')
    
    def test_statistics(self):
        """Test statistics generation"""
        # Upload test files
        file1 = self.create_test_file('doc1.txt', 'a' * 100)
        file2 = self.create_test_file('doc2.pdf', 'b' * 200)
        file3 = self.create_test_file('image1.png', 'c' * 150)
        
        self.classifier.upload_file(file1)
        self.classifier.upload_file(file2)
        self.classifier.upload_file(file3)
        
        stats = self.classifier.get_statistics()
        
        self.assertEqual(stats['total_files'], 3)
        self.assertIn('documents', stats['categories'])
        self.assertIn('images', stats['categories'])
        self.assertEqual(stats['categories']['documents']['count'], 2)
        self.assertEqual(stats['categories']['images']['count'], 1)
    
    def test_file_not_found(self):
        """Test handling of non-existent files"""
        with self.assertRaises(FileNotFoundError):
            self.classifier.upload_file('/nonexistent/file.txt')
    
    def test_metadata_persistence(self):
        """Test that metadata persists across instances"""
        test_file = self.create_test_file('test.txt', 'Persistent')
        result = self.classifier.upload_file(test_file)
        file_hash = result['file_info']['hash']
        
        # Create new classifier instance with same upload dir
        new_classifier = FileClassifier(self.upload_dir)
        
        # Verify metadata was loaded
        self.assertIn(file_hash, new_classifier.metadata)
        self.assertEqual(new_classifier.metadata[file_hash]['original_name'], 'test.txt')


if __name__ == '__main__':
    unittest.main()
