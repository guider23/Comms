#!/usr/bin/env python3
"""
comms.undo - Restore files from backup

Provides functionality to restore files from .backup directory.
"""

import shutil
import time
from pathlib import Path
from typing import List, Tuple


def get_backup_files() -> List[Tuple[Path, Path]]:
    """Get list of backup files and their restore destinations."""
    backup_dir = Path(".backup")
    
    if not backup_dir.exists():
        return []
    
    backup_files = []
    for backup_file in backup_dir.rglob('*'):
        if backup_file.is_file():

            rel_path = backup_file.relative_to(backup_dir)
            original_path = Path.cwd() / rel_path
            backup_files.append((backup_file, original_path))
    
    return backup_files


def restore_file(backup_path: Path, original_path: Path) -> bool:
    """Restore a single file from backup."""
    try:

        original_path.parent.mkdir(parents=True, exist_ok=True)
        

        shutil.copy2(backup_path, original_path)
        return True
    
    except Exception as e:
        print(f"Error restoring {original_path}: {e}")
        return False


def restore_from_backup() -> int:
    """Main backup restoration function."""
    start_time = time.time()
    backup_dir = Path(".backup")
    
    if not backup_dir.exists():
        print("❌ No backup directory found (.backup/)")
        return 0
    
    print(f"🔄 Restoring files from backup: {backup_dir.absolute()}")
    

    backup_files = get_backup_files()
    
    if not backup_files:
        print("❌ No backup files found")
        return 0
    
    print(f"📁 Found {len(backup_files)} files to restore")
    

    restored_count = 0
    failed_count = 0
    
    for backup_path, original_path in backup_files:
        if restore_file(backup_path, original_path):
            print(f"✅ Restored: {original_path}")
            restored_count += 1
        else:
            print(f"❌ Failed: {original_path}")
            failed_count += 1
    
    end_time = time.time()
    
    print("\n" + "="*50)
    print("📊 RESTORE COMPLETE")
    print("="*50)
    print(f"✅ Files restored: {restored_count}")
    print(f"❌ Files failed: {failed_count}")
    print(f"⏱️  Time taken: {end_time - start_time:.2f} seconds")
    
    return restored_count


def show_backup_status() -> None:
    """Show information about current backup."""
    backup_dir = Path(".backup")
    
    if not backup_dir.exists():
        print("❌ No backup directory found")
        return
    
    backup_files = get_backup_files()
    
    if not backup_files:
        print("❌ Backup directory exists but contains no files")
        return
    
    print(f"💾 Backup Status")
    print(f"   Directory: {backup_dir.absolute()}")
    print(f"   Files: {len(backup_files)}")
    

    total_size = 0
    for backup_path, _ in backup_files:
        try:
            total_size += backup_path.stat().st_size
        except:
            pass
    

    size_str = format_size(total_size)
    print(f"   Size: {size_str}")
    

    try:
        backup_time = backup_dir.stat().st_mtime
        backup_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(backup_time))
        print(f"   Created: {backup_time_str}")
    except:
        pass


def format_size(size: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}TB"


def main():
    """CLI entry point for standalone undo functionality."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        show_backup_status()
    else:
        restored_count = restore_from_backup()
        if restored_count > 0:
            print(f"\n🎉 Successfully restored {restored_count} files!")
        else:
            print("\n❌ No files were restored")


if __name__ == "__main__":
    main()
