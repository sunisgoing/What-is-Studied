#!/usr/bin/env python3
"""
CLI interface for the file classification system
"""

import sys
import argparse
from pathlib import Path
from file_classifier import FileClassifier


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def upload_command(args):
    """Handle upload command"""
    classifier = FileClassifier(args.upload_dir)
    
    for file_path in args.files:
        print(f"\nUploading: {file_path}")
        try:
            result = classifier.upload_file(file_path, preserve_name=not args.hash_names)
            
            if result['status'] == 'success':
                info = result['file_info']
                print(f"  ✓ Success!")
                print(f"  Category: {info['category']}")
                print(f"  Size: {format_size(info['size'])}")
                print(f"  Stored as: {info['stored_name']}")
            elif result['status'] == 'duplicate':
                print(f"  ⚠ Duplicate file (already uploaded)")
                existing = result['existing_file']
                print(f"  Original: {existing['original_name']}")
                print(f"  Category: {existing['category']}")
        except Exception as e:
            print(f"  ✗ Error: {e}")


def list_command(args):
    """Handle list command"""
    classifier = FileClassifier(args.upload_dir)
    
    files = classifier.list_files(category=args.category)
    
    if not files:
        if args.category:
            print(f"No files found in category: {args.category}")
        else:
            print("No files uploaded yet")
        return
    
    print(f"\nFound {len(files)} file(s):")
    print("-" * 80)
    
    for file_info in files:
        print(f"Name: {file_info['original_name']}")
        print(f"  Category: {file_info['category']}")
        print(f"  Size: {format_size(file_info['size'])}")
        print(f"  Path: {file_info['path']}")
        print()


def stats_command(args):
    """Handle stats command"""
    classifier = FileClassifier(args.upload_dir)
    stats = classifier.get_statistics()
    
    print(f"\nFile Classification Statistics")
    print("=" * 80)
    print(f"Total files: {stats['total_files']}")
    print()
    
    if stats['categories']:
        print("By Category:")
        print("-" * 80)
        for category, data in sorted(stats['categories'].items()):
            print(f"  {category:15} : {data['count']:4} files, {format_size(data['total_size']):>12}")
    else:
        print("No files uploaded yet")


def categories_command(args):
    """Handle categories command"""
    classifier = FileClassifier(args.upload_dir)
    
    print("\nSupported Categories:")
    print("=" * 80)
    
    for category, rules in FileClassifier.CATEGORIES.items():
        print(f"\n{category.upper()}")
        print(f"  Extensions: {', '.join(rules['extensions'][:10])}")
        if len(rules['extensions']) > 10:
            print(f"              ... and {len(rules['extensions']) - 10} more")


def main():
    parser = argparse.ArgumentParser(
        description='File Classification System - Upload and categorize files by content',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--upload-dir',
        default='uploads',
        help='Base directory for uploads (default: uploads)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Upload command
    upload_parser = subparsers.add_parser('upload', help='Upload and classify files')
    upload_parser.add_argument(
        'files',
        nargs='+',
        help='Files to upload'
    )
    upload_parser.add_argument(
        '--hash-names',
        action='store_true',
        help='Store files with hash-based names instead of original names'
    )
    
    # List command
    list_parser = subparsers.add_parser('list', help='List uploaded files')
    list_parser.add_argument(
        '--category',
        help='Filter by category'
    )
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    
    # Categories command
    categories_parser = subparsers.add_parser('categories', help='List supported categories')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    if args.command == 'upload':
        upload_command(args)
    elif args.command == 'list':
        list_command(args)
    elif args.command == 'stats':
        stats_command(args)
    elif args.command == 'categories':
        categories_command(args)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
