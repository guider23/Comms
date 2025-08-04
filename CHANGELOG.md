# Changelog

All notable changes to this project will be documented in this file.

## [1.2.1] - 2025-08-04

### 🐛 Critical Fix
- **Fixed CLI Default Behavior**: `comms` command now scans current directory instead of showing help
- **Improved User Experience**: No need to specify directory argument for current directory scanning

### 📝 Usage Changes
- `comms` (no arguments) → Scans current directory recursively ✅
- `comms --help` → Shows help menu ✅ 
- `comms /path/to/dir` → Scans specific directory ✅
- `comms --demo` → Creates demo files ✅
- `comms --undo` → Restores from backup ✅

## [1.2.0] - 2025-08-04

### 🎨 Major UI/UX Improvements
- **Beautiful CLI Interface**: Complete redesign with modern box-drawing characters and emojis
- **Real-time Progress Bars**: Visual progress tracking with `█` and `░` characters
- **Organized Output Sections**: Clean, professional sections for scan results, safety features, and timing
- **Enhanced Confirmation Prompts**: Improved user interaction with clear formatting

### 🔧 HTML Processing Enhancements
- **Fixed HTML `<style>` Tag Processing**: Now properly removes CSS comments inside `<style>` tags
- **Fixed HTML `<script>` Tag Processing**: Now properly removes JavaScript comments inside `<script>` tags
- **Improved HTML Comment Removal**: Better handling of embedded CSS/JS within HTML files
- **Preserved Patterns**: Continues to preserve color codes, URLs, and other important patterns

### 📦 Distribution Improvements
- **Clean Package Structure**: Removed unnecessary files from distribution
- **Windows Installation Script**: Added `install.bat` for easy Windows installation
- **Requirements File**: Added `requirements.txt` (no external dependencies)
- **Better Error Handling**: Improved error messages and progress display

### 🐛 Bug Fixes
- Fixed runtime warnings during package execution
- Improved backup path handling for files outside project directory
- Better progress line clearing to prevent display artifacts

### 📝 Documentation
- Updated README with new features and improved examples
- Enhanced setup.py description to mention beautiful CLI
- Added installation alternatives for different user preferences

## [1.1.0] - Previous Release
- High-accuracy comment removal for 20+ programming languages
- Automatic backup and restore functionality
- Configurable preserve patterns
- Command-line interface
- Comprehensive test suite

## [1.0.0] - Initial Release
- Basic comment removal functionality
- Support for major programming languages
- Simple CLI interface
