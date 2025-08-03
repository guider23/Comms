#!/usr/bin/env python3
"""
comms.cli - Command line interface for the comment removal tool

Provides the main CLI functionality including comment removal, undo, and demo.
"""

import sys
import time
import shutil
from pathlib import Path
from typing import List, Tuple

from .core import CommentRemover
from .undo import restore_from_backup
from .demo import create_demo_files
from .config import load_config


def show_help():
    """Show help information."""
    print("""
🔧 Comment Removal Tool

USAGE:
  comms [directory]          # Remove comments from directory
  comms --undo              # Restore files from backup
  comms --demo              # Create demo files for testing
  comms --config            # Show configuration options
  comms --help              # Show this help

EXAMPLES:
  comms                     # Current directory (recursive)
  comms /path/to/project    # Specific directory (recursive)
  comms --undo              # Restore from .backup/
  comms --demo              # Create test files in demo_files/

FEATURES:
  • Supports 20+ programming languages
  • Creates automatic backups in .backup/
  • Preserves color codes, URLs, shebangs, preprocessor directives
  • Recursive directory scanning
  • Safe operation with confirmation prompts

PRESERVED PATTERNS:
  • Color codes: #FF5733, #123ABC
  • URLs: https://example.com, http://site.com
  • Shebangs: #!/usr/bin/env python
  • C preprocessor: #include, #define, #if, #endif
  • Content inside strings
""")


def format_size(size: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}TB"


def get_directory_info(path: Path) -> Tuple[int, int]:
    """Get directory statistics: file count and total size."""
    total_files = 0
    total_size = 0
    
    try:
        for item in path.rglob('*'):
            if item.is_file() and '.backup' not in item.parts:
                total_files += 1
                total_size += item.stat().st_size
    except PermissionError:
        pass
    
    return total_files, total_size


def show_status(results: dict):
    """Show processing results in a formatted way."""
    print("\n" + "="*50)
    print("📊 PROCESSING COMPLETE")
    print("="*50)
    
    if results.get('dry_run', False):
        print(f"🔍 Dry Run Results:")
        print(f"   Files found: {results['processed']}")
        print(f"   No changes made (dry run mode)")
    else:
        print(f"📁 Files processed: {results['processed']}")
        print(f"✏️  Files modified: {results['modified']}")
        print(f"❌ Errors: {results['errors']}")
        
        if results['modified'] > 0:
            backup_path = Path('.backup')
            if backup_path.exists():
                print(f"💾 Backup created: {backup_path.absolute()}")
                print(f"🔄 To restore: comms --undo")
    
    if results.get('message'):
        print(f"\n{results['message']}")


def confirm_action(message: str) -> bool:
    """Get user confirmation for potentially destructive actions."""
    try:
        response = input(f"{message} (y/N): ").strip().lower()
        return response in ['y', 'yes']
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return False


def main():
    """Main CLI entry point."""
    args = sys.argv[1:]
    
    # Handle help
    if not args or '--help' in args or '-h' in args:
        show_help()
        return
    
    # Handle undo
    if '--undo' in args:
        backup_dir = Path('.backup')
        if not backup_dir.exists():
            print("❌ No backup directory found (.backup/)")
            return
        
        print(f"🔄 Found backup directory: {backup_dir.absolute()}")
        
        if confirm_action("Restore all files from backup?"):
            try:
                restored_count = restore_from_backup()
                print(f"✅ Restored {restored_count} files from backup")
                
                # Remove backup directory
                if confirm_action("Remove backup directory?"):
                    shutil.rmtree(backup_dir)
                    print("🗑️  Backup directory removed")
                    
            except Exception as e:
                print(f"❌ Error during restore: {e}")
        return
    
    # Handle demo
    if '--demo' in args:
        try:
            demo_dir = create_demo_files()
            print(f"✅ Demo files created in: {demo_dir}")
            print("   Run 'comms demo_files' to test the tool")
            return
        except Exception as e:
            print(f"❌ Error creating demo: {e}")
            return
    
    # Handle config
    if '--config' in args:
        try:
            config = load_config()
            print("⚙️  Current Configuration:")
            print(f"   Preserve patterns: {len(config.get('preserve_patterns', []))}")
            for pattern in config.get('preserve_patterns', []):
                print(f"     - {pattern}")
        except Exception as e:
            print(f"❌ Error loading config: {e}")
        return
    
    # Handle target directory
    target_path = args[0] if args else "."
    target = Path(target_path)
    
    if not target.exists():
        print(f"❌ Path does not exist: {target}")
        return
    
    # Load configuration
    try:
        config = load_config()
        preserve_patterns = config.get('preserve_patterns', [])
    except Exception as e:
        print(f"⚠️  Warning: Could not load config: {e}")
        preserve_patterns = []
    
    # Show directory info
    if target.is_dir():
        file_count, total_size = get_directory_info(target)
        print(f"📁 Target: {target.absolute()}")
        print(f"📊 Found: {file_count} files ({format_size(total_size)})")
        
        if file_count == 0:
            print("❌ No files found to process")
            return
        
        if not confirm_action(f"Process {file_count} files recursively?"):
            print("Operation cancelled.")
            return
    else:
        print(f"📄 Target file: {target.absolute()}")
        if not confirm_action("Process this file?"):
            print("Operation cancelled.")
            return
    
    # Process files
    try:
        print("\n🚀 Starting comment removal...")
        start_time = time.time()
        
        # Create comment remover with config
        remover = CommentRemover(preserve_patterns=preserve_patterns)
        
        # Run the process
        results = remover.run(target_path)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Show results
        show_status(results)
        print(f"⏱️  Processing time: {processing_time:.2f} seconds")
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
