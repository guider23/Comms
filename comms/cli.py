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
╭─────────────────────────────────────────────────────────────╮
│                   � Comment Removal Tool                   │
╰─────────────────────────────────────────────────────────────╯

┌─ USAGE ─────────────────────────────────────────────────────┐
│  comms [directory]          Remove comments from directory │
│  comms --undo              Restore files from backup       │
│  comms --demo              Create demo files for testing   │
│  comms --config            Show configuration options      │
│  comms --help              Show this help                  │
└─────────────────────────────────────────────────────────────┘

┌─ EXAMPLES ──────────────────────────────────────────────────┐
│  comms                     Current directory (recursive)   │
│  comms /path/to/project    Specific directory (recursive)  │
│  comms --undo              Restore from .backup/           │
│  comms --demo              Create test files in demo_files/│
└─────────────────────────────────────────────────────────────┘

┌─ FEATURES ──────────────────────────────────────────────────┐
│  ✨ Supports 20+ programming languages                     │
│  🛡️  Creates automatic backups in .backup/                 │
│  🎯 Preserves color codes, URLs, shebangs, preprocessors   │
│  📁 Recursive directory scanning                           │
│  🔒 Safe operation with confirmation prompts               │
└─────────────────────────────────────────────────────────────┘

┌─ PRESERVED PATTERNS ────────────────────────────────────────┐
│  🎨 Color codes: #FF5733, #123ABC                          │
│  🔗 URLs: https://example.com, http://site.com             │
│  ⚡ Shebangs: #!/usr/bin/env python                        │
│  🔧 C preprocessor:
│  📝 Content inside strings                                 │
└─────────────────────────────────────────────────────────────┘
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
    print("\n╭─────────────────────────────────────────────────────────────╮")
    print("│                  🎉 PROCESSING COMPLETE                     │")
    print("╰─────────────────────────────────────────────────────────────╯")
    
    if results.get('dry_run', False):
        print(f"┌─ DRY RUN RESULTS ───────────────────────────────────────────┐")
        print(f"│  🔍 Files found: {results['processed']:<41} │")
        print(f"│  📝 No changes made (dry run mode)                         │")
        print(f"└─────────────────────────────────────────────────────────────┘")
    else:
        print(f"┌─ RESULTS ───────────────────────────────────────────────────┐")
        print(f"│  📁 Files processed: {results['processed']:<39} │")
        print(f"│  ✏️  Files modified: {results['modified']:<40} │")
        print(f"│  ❌ Errors: {results['errors']:<48} │")
        print(f"└─────────────────────────────────────────────────────────────┘")
        
        if results['modified'] > 0:
            backup_path = Path('.backup')
            if backup_path.exists():
                print(f"\n┌─ BACKUP INFO ───────────────────────────────────────────────┐")
                print(f"│  💾 Backup created: {str(backup_path.absolute())[:40]:<40} │")
                print(f"│  🔄 To restore: comms --undo                               │")
                print(f"└─────────────────────────────────────────────────────────────┘")
    
    if results.get('message'):
        print(f"\n💬 {results['message']}")


def confirm_action(message: str) -> bool:
    """Get user confirmation for potentially destructive actions."""
    try:
        print(f"\n❓ {message}")
        response = input("   Continue? (y/N): ").strip().lower()
        return response in ['y', 'yes']
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled.")
        return False


def main():
    """Main CLI entry point."""
    args = sys.argv[1:]
    

    if '--help' in args or '-h' in args:
        show_help()
        return
    

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
                

                if confirm_action("Remove backup directory?"):
                    shutil.rmtree(backup_dir)
                    print("🗑️  Backup directory removed")
                    
            except Exception as e:
                print(f"❌ Error during restore: {e}")
        return
    

    if '--demo' in args:
        try:
            demo_dir = create_demo_files()
            print(f"✅ Demo files created in: {demo_dir}")
            print("   Run 'comms demo_files' to test the tool")
            return
        except Exception as e:
            print(f"❌ Error creating demo: {e}")
            return
    

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
    

    target_path = args[0] if args else "."
    target = Path(target_path)
    
    if not target.exists():
        print(f"❌ Path does not exist: {target}")
        return
    

    try:
        config = load_config()
        preserve_patterns = config.get('preserve_patterns', [])
    except Exception as e:
        print(f"⚠️  Warning: Could not load config: {e}")
        preserve_patterns = []
    

    if target.is_dir():
        file_count, total_size = get_directory_info(target)
        
        print("\n╭─────────────────────────────────────────────────────────────╮")
        print("│                     📁 SCAN RESULTS                         │")
        print("╰─────────────────────────────────────────────────────────────╯")
        print(f"┌─ TARGET ────────────────────────────────────────────────────┐")
        print(f"│  📂 Directory: {str(target.absolute())[:45]:<45} │")
        print(f"│  📊 Files found: {file_count:<42} │")
        print(f"│  💾 Total size: {format_size(total_size):<43} │")
        print(f"└─────────────────────────────────────────────────────────────┘")
        
        if file_count == 0:
            print("\n❌ No supported files found to process")
            return
        

        print(f"\n┌─ SAFETY FEATURES ───────────────────────────────────────────┐")
        print(f"│  🛡️  Automatic backups in .backup/ directory               │")
        print(f"│  🎯 Preserves: Colors, URLs, Shebangs, Preprocessors       │")
        print(f"│  🔄 Full restore available with: comms --undo              │")
        print(f"│  ⚠️  Previous backups will be overwritten                  │")
        print(f"└─────────────────────────────────────────────────────────────┘")
        
        if not confirm_action(f"Process {file_count} files recursively?"):
            print("\n❌ Operation cancelled.")
            return
    else:
        print(f"\n╭─────────────────────────────────────────────────────────────╮")
        print(f"│                      📄 FILE TARGET                         │")
        print(f"╰─────────────────────────────────────────────────────────────╯")
        print(f"│  📁 File: {str(target.absolute())[:50]:<50} │")
        print(f"└─────────────────────────────────────────────────────────────┘")
        
        if not confirm_action("Process this file?"):
            print("\n❌ Operation cancelled.")
            return
    

    try:
        print("\n╭─────────────────────────────────────────────────────────────╮")
        print("│                   🚀 PROCESSING STARTED                     │")
        print("╰─────────────────────────────────────────────────────────────╯")
        start_time = time.time()
        

        remover = CommentRemover(preserve_patterns=preserve_patterns)
        

        results = remover.run(target_path)
        
        end_time = time.time()
        processing_time = end_time - start_time
        

        show_status(results)
        print(f"\n┌─ TIMING ────────────────────────────────────────────────────┐")
        print(f"│  ⏱️  Processing time: {processing_time:.2f} seconds{' '*(23-len(f'{processing_time:.2f}'))} │")
        print(f"└─────────────────────────────────────────────────────────────┘")
        
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
