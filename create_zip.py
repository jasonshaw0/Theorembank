#!/usr/bin/env python3
import zipfile
import os
from pathlib import Path

def create_codebase_zip():
    """Create a zip file of the codebase excluding unnecessary files/folders"""
    
    # Define what to exclude
    exclude_dirs = {'.git', '.conda', 'Trash', '.vscode', 'dist', '__pycache__', 'node_modules'}
    exclude_files = {'.DS_Store', 'Thumbs.db'}
    
    def should_include(path):
        path_obj = Path(path)
        # Exclude directories we don't want
        for part in path_obj.parts:
            if part in exclude_dirs:
                return False
        # Exclude specific files
        if path_obj.name in exclude_files:
            return False
        return True
    
    zip_filename = 'theorembank_codebase.zip'
    
    # Create zip file
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                if should_include(file_path):
                    # Add file to zip with relative path
                    arcname = os.path.relpath(file_path, '.')
                    zipf.write(file_path, arcname)
                    print(f'Added: {arcname}')
    
    print(f'\n✅ Zip file created: {zip_filename}')
    
    # Get zip file size
    size = os.path.getsize(zip_filename)
    print(f'📦 Size: {size / 1024 / 1024:.2f} MB')

if __name__ == "__main__":
    create_codebase_zip()
