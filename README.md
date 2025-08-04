# Comment Remover CLI

[![PyPI version](https://badge.fury.io/py/comment-remover-cli.svg)](https://badge.fury.io/py/comment-remover-cli)
[![Python Support](https://img.shields.io/pypi/pyversions/comment-remover-cli.svg)](https://pypi.org/project/comment-remover-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-accuracy Python tool for removing comments from programming files while preserving important code patterns such as color codes, URLs, and preprocessor directives.

## Features

- **Universal Language Support**: 20+ programming languages including Python, JavaScript, TypeScript, C/C++, Java, C#, Go, Rust, HTML, CSS, SQL, PHP, Ruby, and Shell scripts
- **Safe Operation**: Automatic backup creation before processing
- **Undo Capability**: Restore original files from backup
- **Configurable Settings**: JSON-based configuration system
- **Demo Mode**: Generate test files for validation
- **High Performance**: Efficient processing of entire directory trees
- **Recursive Scanning**: Processes all subdirectories automatically
- **Robust Error Handling**: Graceful handling of permission errors and encoding issues

## Installation

### From PyPI (Recommended)
```bash
pip install comment-remover-cli
```

### From Source
```bash
git clone https://github.com/guider23/Comms.git
cd Comms
pip install .
```

## Quick Start

```bash
# Remove comments from current directory
python -m comms.cli

# Remove comments from specific directory
python -m comms.cli /path/to/your/project

# Create demo files for testing
python -m comms.cli --demo

# Restore files from backup
python -m comms.cli --undo

# Display help information
python -m comms.cli --help
```

## Command Line Options

```bash
python -m comms.cli [directory] [options]

Options:
  -h, --help     Show help message and exit
  --demo         Create demo files with comments for testing
  --undo         Restore files from most recent backup
  --config FILE  Use custom configuration file (default: config.json)
```

## Supported Languages

| Language | Extensions | Line Comments | Block Comments |
|----------|------------|---------------|----------------|
| Python | .py | # | """ """ or ''' ''' |
| JavaScript/TypeScript | .js, .jsx, .ts, .tsx | // | /* */ |
| Java | .java | // | /* */ |
| C/C++ | .c, .cpp, .h, .hpp | // | /* */ |
| C# | .cs | // | /* */ |
| Go | .go | // | /* */ |
| Rust | .rs | // | /* */ |
| PHP | .php | // | /* */ |
| Ruby | .rb | # | =begin =end |
| Shell/Bash | .sh, .bash | # | - |
| SQL | .sql | -- | /* */ |
| HTML | .html, .htm | - | <!-- --> |
| CSS | .css | - | /* */ |
| SCSS/Sass | .scss, .sass | // | /* */ |
| Lua | .lua | -- | --[[ ]] |
| Swift | .swift | // | /* */ |
| Kotlin | .kt, .kts | // | /* */ |

## Pattern Preservation

The tool intelligently preserves:

- **Color codes**: `#FF5733`, `#123ABC`
- **URLs**: `https://example.com`, `http://site.com`
- **Shebangs**: `#!/usr/bin/env python`
- **C Preprocessor**: `#include`, `#define`, `#if`, `#endif`, etc.
- **Content in strings**: Comments inside quoted strings remain untouched

## Example Usage

### Before Processing

**Python file:**
```python
#!/usr/bin/env python3
# This is a comment to remove
import requests  # Another comment

def get_data():
    """This docstring stays"""
    url = "https://api.example.com"  # URL preserved
    color = "#FF5733"  # Color code preserved
    # This comment will be removed
    return requests.get(url)
```

### After Processing

**Python file:**
```python
#!/usr/bin/env python3
import requests

def get_data():
    """This docstring stays"""
    url = "https://api.example.com"
    color = "#FF5733"
    return requests.get(url)
```

## Configuration

Create a `config.json` file to customize behavior:

```json
{
  "languages": {
    "python": {
      "extensions": [".py"],
      "line_comment": "#",
      "block_comment_start": "\"\"\"",
      "block_comment_end": "\"\"\""
    },
    "javascript": {
      "extensions": [".js", ".jsx"],
      "line_comment": "//",
      "block_comment_start": "/*",
      "block_comment_end": "*/"
    }
  },
  "backup_enabled": true,
  "backup_directory": ".backup",
  "skip_patterns": [
    "node_modules/",
    ".git/",
    "__pycache__/"
  ]
}
```

## Safety Features

### Automatic Backups
- All original files are backed up to `.backup/` directory
- Backup directory structure mirrors your project structure
- Previous backups are overwritten on each run

### Undo Operation
```bash
# Restore from most recent backup
python -m comms.cli --undo
```

### Pre-execution Warning
The tool displays:
- Number of files to be processed
- File types detected
- Clear warning about the operation
- Requires explicit confirmation

## Error Handling

- **Permission errors**: Gracefully skipped with warnings
- **Encoding issues**: Uses UTF-8 with error tolerance
- **Backup failures**: File processing is skipped if backup fails
- **Malformed files**: Processing continues with error reporting

## Advanced Usage

### Custom Configuration
```bash
python -m comms.cli --config custom-config.json /my/project
```

### Processing Specific File Types
Edit `config.json` to limit processing to specific languages or add new ones.

### Integration with Build Systems
```bash
# In your build script
python -m comms.cli src/ --config production-config.json
```

## Technical Details

### String Handling
- Properly handles escaped quotes in strings
- Supports single, double, and triple-quoted strings (Python)
- Preserves multiline strings and docstrings

### Comment Detection
- State-machine based parsing for accuracy
- Context-aware comment detection
- Handles nested comment structures

### Performance
- Processes files sequentially for reliability
- Memory-efficient line-by-line processing for large files
- Minimal I/O operations

## Requirements

- Python 3.6 or higher
- No external dependencies
- Cross-platform (Windows, macOS, Linux)

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/guider23/Comms.git
cd Comms
pip install -e .
```

### Running Tests

```bash
python -m pytest tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Report bugs on [GitHub Issues](https://github.com/guider23/Comms/issues)
- **PyPI Package**: [comment-remover-cli](https://pypi.org/project/comment-remover-cli/)
- **Documentation**: Full docs at [GitHub Repository](https://github.com/guider23/Comms)

## Changelog

### v1.1.0
- Professional documentation
- Improved error handling
- Enhanced pattern preservation
- Updated PyPI package

### v1.0.0
- Initial release
- Support for 20+ programming languages
- Automatic backup and undo functionality
- Configurable settings

---

**Made for developers who value clean, production-ready code.**
