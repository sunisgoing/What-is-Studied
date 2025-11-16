#!/usr/bin/env python3
"""
Example usage of the File Classification System API
This demonstrates how to use the file_classifier module programmatically
"""

from file_classifier import FileClassifier
import os


def main():
    print("=" * 80)
    print("File Classification System - API Usage Example")
    print("=" * 80)
    
    # Initialize the classifier with a custom upload directory
    classifier = FileClassifier(upload_dir='example_uploads')
    
    print("\n1. Creating test files...")
    # Create some test files
    test_files = []
    os.makedirs('/tmp/example_files', exist_ok=True)
    
    # Document file
    with open('/tmp/example_files/report.txt', 'w') as f:
        f.write("Annual Report 2024\n" + "=" * 50 + "\nThis is a sample document.")
    test_files.append('/tmp/example_files/report.txt')
    
    # Code file
    with open('/tmp/example_files/hello.py', 'w') as f:
        f.write('#!/usr/bin/env python3\nprint("Hello, World!")\n')
    test_files.append('/tmp/example_files/hello.py')
    
    # Data file
    with open('/tmp/example_files/users.csv', 'w') as f:
        f.write('id,name,email\n1,Alice,alice@example.com\n2,Bob,bob@example.com\n')
    test_files.append('/tmp/example_files/users.csv')
    
    print(f"   Created {len(test_files)} test files")
    
    # Upload files
    print("\n2. Uploading files...")
    for file_path in test_files:
        result = classifier.upload_file(file_path)
        if result['status'] == 'success':
            info = result['file_info']
            print(f"   ✓ {info['original_name']}")
            print(f"     Category: {info['category']}")
            print(f"     Size: {info['size']} bytes")
    
    # List all files
    print("\n3. Listing all uploaded files...")
    all_files = classifier.list_files()
    for file_info in all_files:
        print(f"   - {file_info['original_name']} ({file_info['category']})")
    
    # Get statistics
    print("\n4. File statistics...")
    stats = classifier.get_statistics()
    print(f"   Total files: {stats['total_files']}")
    print("   By category:")
    for category, data in sorted(stats['categories'].items()):
        print(f"      {category}: {data['count']} files, {data['total_size']} bytes")
    
    # List files by category
    print("\n5. Files in 'code' category...")
    code_files = classifier.list_files(category='code')
    for file_info in code_files:
        print(f"   - {file_info['original_name']}")
    
    # Demonstrate duplicate detection
    print("\n6. Testing duplicate detection...")
    result = classifier.upload_file(test_files[0])
    if result['status'] == 'duplicate':
        print(f"   ⚠ Duplicate detected: {result['existing_file']['original_name']}")
    
    # Show supported categories
    print("\n7. Supported categories:")
    for category in FileClassifier.CATEGORIES.keys():
        print(f"   - {category}")
    
    print("\n" + "=" * 80)
    print("Example completed successfully!")
    print("=" * 80)


if __name__ == '__main__':
    main()
