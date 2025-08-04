#!/usr/bin/env python3
"""
comms.config - Configuration loading and management

Handles loading configuration from JSON files in various locations.
"""

import json
from pathlib import Path
from typing import Dict, Optional, Any


def load_config() -> Optional[Dict[str, Any]]:
    """Load configuration from available sources."""
    config_locations = [
        Path.cwd() / "comms.json",
        Path.home() / ".comms.json",
        Path.cwd() / ".comms.json",
    ]
    
    for config_path in config_locations:
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                print(f"📄 Loaded configuration from: {config_path}")
                return config
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️ Error loading config from {config_path}: {e}")
                continue
    
    return None


def get_default_config() -> Dict[str, Any]:
    """Get the default configuration."""
    return {
        "preserve_patterns": [
            r"#[0-9a-fA-F]{3,8}\\b",
            r"https?://[^\\s]+",
            r"#!/[^\\n]+",
            r"#pragma\\s+",
            r"#include\\s+",
            r"#define\\s+",
            r"#if\\w*\\s+",
            r"#endif\\b",
            r"#undef\\s+",
            r"#error\\s+",
            r"#warning\\s+",
        ],
        "backup_directory": ".backup",
        "supported_extensions": [
            ".py", ".js", ".ts", ".jsx", ".tsx",
            ".java", ".c", ".cpp", ".h", ".hpp",
            ".cs", ".php", ".go", ".rs", ".swift",
            ".kt", ".scala", ".css", ".scss", ".sass",
            ".less", ".html", ".htm", ".xml",
            ".sh", ".bash", ".zsh", ".fish", ".ps1",
            ".rb", ".pl", ".pm", ".r", ".sql",
            ".yaml", ".yml", ".m", ".lua"
        ]
    }


def create_default_config(path: Optional[Path] = None) -> Path:
    """Create a default configuration file."""
    if path is None:
        path = Path.cwd() / "comms.json"
    
    config = get_default_config()
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    return path


def update_config(updates: Dict[str, Any], path: Optional[Path] = None) -> bool:
    """Update configuration file with new values."""
    if path is None:
        config_locations = [
            Path.cwd() / "comms.json",
            Path.home() / ".comms.json",
            Path.cwd() / ".comms.json",
        ]
        

        for config_path in config_locations:
            if config_path.exists():
                path = config_path
                break
        else:
            path = config_locations[0]
    
    try:

        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = get_default_config()
        

        config.update(updates)
        

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        return True
        
    except (json.JSONDecodeError, IOError) as e:
        print(f"❌ Error updating config: {e}")
        return False


def validate_config(config: Dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate configuration structure and values."""
    errors = []
    

    if 'preserve_patterns' in config:
        if not isinstance(config['preserve_patterns'], list):
            errors.append("preserve_patterns must be a list")
        else:
            for i, pattern in enumerate(config['preserve_patterns']):
                if not isinstance(pattern, str):
                    errors.append(f"preserve_patterns[{i}] must be a string")
    

    if 'backup_directory' in config:
        if not isinstance(config['backup_directory'], str):
            errors.append("backup_directory must be a string")
    

    if 'supported_extensions' in config:
        if not isinstance(config['supported_extensions'], list):
            errors.append("supported_extensions must be a list")
        else:
            for i, ext in enumerate(config['supported_extensions']):
                if not isinstance(ext, str):
                    errors.append(f"supported_extensions[{i}] must be a string")
                elif not ext.startswith('.'):
                    errors.append(f"supported_extensions[{i}] must start with '.'")
    
    return len(errors) == 0, errors
