"""
Core functionality for the comment removal tool.
"""

import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional


class CommentRemover:
    """Main class for removing comments from various file types."""
    
    def __init__(self, preserve_patterns: Optional[List[str]] = None):
        """Initialize the comment remover.
        
        Args:
            preserve_patterns: List of regex patterns for comments to preserve
        """
        self.preserve_patterns = preserve_patterns or []
        self.backup_dir = Path.cwd() / '.backup'
        

        self.supported_extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'c_style',
            '.c': 'c_style',
            '.cpp': 'c_style',
            '.cc': 'c_style',
            '.cxx': 'c_style',
            '.c++': 'c_style',
            '.h': 'c_style',
            '.hpp': 'c_style',
            '.cs': 'c_style',
            '.php': 'php',
            '.go': 'c_style',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.css': 'css',
            '.scss': 'css',
            '.sass': 'css',
            '.less': 'css',
            '.html': 'html',
            '.htm': 'html',
            '.xml': 'html',
            '.sh': 'shell',
            '.bash': 'shell',
            '.zsh': 'shell',
            '.fish': 'shell',
            '.ps1': 'powershell',
            '.rb': 'ruby',
            '.pl': 'perl',
            '.pm': 'perl',
            '.r': 'r',
            '.sql': 'sql',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.m': 'matlab',
            '.lua': 'lua'
        }
    
    def create_backup(self, file_path: Path) -> bool:
        """Create a backup of the file before processing."""
        try:
            self.backup_dir.mkdir(exist_ok=True)
            

            rel_path = file_path.relative_to(Path.cwd())
            backup_path = self.backup_dir / rel_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(file_path, backup_path)
            return True
        except Exception as e:
            print(f"Warning: Could not backup {file_path}: {e}")
            return False
    
    def is_preserve_pattern(self, content: str, comment_start: int) -> bool:
        """Check if the comment-like pattern should be preserved."""

        remaining_content = content[comment_start:]
        

        for pattern in self.preserve_patterns:

            match = re.match(pattern, remaining_content)
            if match:
                return True
        return False
    
    def remove_python_comments(self, content: str) -> str:
        """Remove Python comments while preserving strings."""
        lines = content.split('\n')
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
                

            new_line = ""
            i = 0
            in_single_quote = False
            in_double_quote = False
            in_triple_single = False
            in_triple_double = False
            escape_next = False
            
            while i < len(line):
                char = line[i]
                
                if escape_next:
                    new_line += char
                    escape_next = False
                elif char == '\\' and (in_single_quote or in_double_quote):
                    new_line += char
                    escape_next = True
                elif not any([in_single_quote, in_double_quote, in_triple_single, in_triple_double]):

                    if i + 2 < len(line) and line[i:i+3] == '"""':
                        in_triple_double = True
                        new_line += line[i:i+3]
                        i += 2
                    elif i + 2 < len(line) and line[i:i+3] == "'''":
                        in_triple_single = True
                        new_line += line[i:i+3]
                        i += 2
                    elif char == '"':
                        in_double_quote = True
                        new_line += char
                    elif char == "'":
                        in_single_quote = True
                        new_line += char
                    elif char == '#':

                        if not self.is_preserve_pattern(line, i):
                            break
                        else:
                            new_line += char
                    else:
                        new_line += char
                else:

                    if in_triple_double and i + 2 < len(line) and line[i:i+3] == '"""':
                        in_triple_double = False
                        new_line += line[i:i+3]
                        i += 2
                    elif in_triple_single and i + 2 < len(line) and line[i:i+3] == "'''":
                        in_triple_single = False
                        new_line += line[i:i+3]
                        i += 2
                    elif in_double_quote and char == '"':
                        in_double_quote = False
                        new_line += char
                    elif in_single_quote and char == "'":
                        in_single_quote = False
                        new_line += char
                    else:
                        new_line += char
                
                i += 1
            
            result.append(new_line.rstrip())
        
        return '\n'.join(result)
    
    def remove_c_style_comments(self, content: str) -> str:
        """Remove C-style comments (// and /* */) while preserving strings."""
        result = ""
        i = 0
        in_single_quote = False
        in_double_quote = False
        escape_next = False
        
        while i < len(content):
            char = content[i]
            
            if escape_next:
                result += char
                escape_next = False
            elif char == '\\' and (in_single_quote or in_double_quote):
                result += char
                escape_next = True
            elif not in_single_quote and not in_double_quote:

                if char == '"':
                    in_double_quote = True
                    result += char
                elif char == "'":
                    in_single_quote = True
                    result += char
                elif i + 1 < len(content) and content[i:i+2] == '//':

                    if not self.is_preserve_pattern(content, i):

                        while i < len(content) and content[i] != '\n':
                            i += 1
                        continue
                    else:
                        result += char
                elif i + 1 < len(content) and content[i:i+2] == '/*':

                    if not self.is_preserve_pattern(content, i):
                        i += 2

                        while i + 1 < len(content) and content[i:i+2] != '*/':
                            i += 1
                        if i + 1 < len(content):
                            i += 2
                        continue
                    else:
                        result += char
                else:
                    result += char
            else:

                if in_double_quote and char == '"':
                    in_double_quote = False
                elif in_single_quote and char == "'":
                    in_single_quote = False
                result += char
            
            i += 1
        
        return result
    
    def remove_html_comments(self, content: str) -> str:
        """Remove HTML/XML comments and comments within style/script tags."""

        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        

        def clean_style_tag(match):
            style_content = match.group(1)
            cleaned_css = self.remove_css_comments(style_content)
            return f'<style{match.group(0).split("<style")[1].split(">")[0]}>{cleaned_css}</style>'
        
        content = re.sub(r'<style[^>]*>(.*?)</style>', clean_style_tag, content, flags=re.DOTALL | re.IGNORECASE)
        

        def clean_script_tag(match):
            script_content = match.group(1)
            cleaned_js = self.remove_c_style_comments(script_content)
            return f'<script{match.group(0).split("<script")[1].split(">")[0]}>{cleaned_js}</script>'
        
        content = re.sub(r'<script[^>]*>(.*?)</script>', clean_script_tag, content, flags=re.DOTALL | re.IGNORECASE)
        
        return content
    
    def remove_css_comments(self, content: str) -> str:
        """Remove CSS comments while preserving color codes and URLs."""
        result = ""
        i = 0
        in_string = False
        string_char = None
        
        while i < len(content):
            char = content[i]
            
            if not in_string:
                if char in ['"', "'"]:
                    in_string = True
                    string_char = char
                    result += char
                elif i + 1 < len(content) and content[i:i+2] == '/*':

                    if not self.is_preserve_pattern(content, i):
                        i += 2
                        while i + 1 < len(content) and content[i:i+2] != '*/':
                            i += 1
                        if i + 1 < len(content):
                            i += 2
                        continue
                    else:
                        result += char
                else:
                    result += char
            else:
                if char == string_char:
                    in_string = False
                    string_char = None
                result += char
            
            i += 1
        
        return result
    
    def remove_shell_comments(self, content: str) -> str:
        """Remove shell comments while preserving shebangs."""
        lines = content.split('\n')
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            

            if line.startswith('#!'):
                result.append(line)
                continue
            
            new_line = ""
            i = 0
            in_single_quote = False
            in_double_quote = False
            escape_next = False
            
            while i < len(line):
                char = line[i]
                
                if escape_next:
                    new_line += char
                    escape_next = False
                elif char == '\\':
                    new_line += char
                    escape_next = True
                elif not in_single_quote and not in_double_quote:
                    if char == '"':
                        in_double_quote = True
                        new_line += char
                    elif char == "'":
                        in_single_quote = True
                        new_line += char
                    elif char == '#':
                        if not self.is_preserve_pattern(line, i):
                            break
                        else:
                            new_line += char
                    else:
                        new_line += char
                else:
                    if in_double_quote and char == '"':
                        in_double_quote = False
                    elif in_single_quote and char == "'":
                        in_single_quote = False
                    new_line += char
                
                i += 1
            
            result.append(new_line.rstrip())
        
        return '\n'.join(result)
    
    def remove_sql_comments(self, content: str) -> str:
        """Remove SQL comments (-- and /* */)."""
        lines = content.split('\n')
        result = []
        
        for line in lines:
            if not line.strip():
                result.append(line)
                continue
            
            new_line = ""
            i = 0
            in_string = False
            string_char = None
            
            while i < len(line):
                char = line[i]
                
                if not in_string:
                    if char in ['"', "'"]:
                        in_string = True
                        string_char = char
                        new_line += char
                    elif i + 1 < len(line) and line[i:i+2] == '--':
                        if not self.is_preserve_pattern(line, i):
                            break
                        else:
                            new_line += char
                    else:
                        new_line += char
                else:
                    if char == string_char:
                        in_string = False
                        string_char = None
                    new_line += char
                
                i += 1
            
            result.append(new_line.rstrip())
        

        content = '\n'.join(result)
        return self.remove_c_style_comments(content)
    
    def remove_comments_by_type(self, content: str, file_type: str) -> str:
        """Remove comments based on file type."""
        if file_type == 'python':
            return self.remove_python_comments(content)
        elif file_type in ['javascript', 'typescript', 'c_style', 'rust', 'swift', 'kotlin', 'scala']:
            return self.remove_c_style_comments(content)
        elif file_type == 'html':
            return self.remove_html_comments(content)
        elif file_type == 'css':
            return self.remove_css_comments(content)
        elif file_type in ['shell', 'powershell', 'ruby', 'perl', 'r', 'yaml']:
            return self.remove_shell_comments(content)
        elif file_type == 'sql':
            return self.remove_sql_comments(content)
        elif file_type == 'php':

            content = self.remove_c_style_comments(content)
            return self.remove_shell_comments(content)
        elif file_type in ['matlab', 'lua']:
            return self.remove_shell_comments(content)
        else:
            print(f"Unsupported file type: {file_type}")
            return content
    
    def process_file(self, file_path: Path) -> bool:
        """Process a single file to remove comments."""
        try:
            suffix = file_path.suffix.lower()
            if suffix not in self.supported_extensions:
                return False
            
            file_type = self.supported_extensions[suffix]
            

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            

            processed_content = self.remove_comments_by_type(content, file_type)
            

            if processed_content != content:

                if not self.create_backup(file_path):
                    return False
                

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(processed_content)
                
                return True
            
            return False
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False
    
    def scan_directory(self, directory: Path) -> List[Path]:
        """Scan directory for supported files."""
        files = []
        try:
            for item in directory.rglob('*'):
                if item.is_file() and item.suffix.lower() in self.supported_extensions:

                    if '.backup' not in item.parts:
                        files.append(item)
        except PermissionError:
            print(f"Permission denied: {directory}")
        
        return files
    
    def run(self, target_path: str = ".", dry_run: bool = False) -> Dict[str, any]:
        """Main method to run the comment removal process."""
        target = Path(target_path).resolve()
        
        if not target.exists():
            raise FileNotFoundError(f"Target path does not exist: {target}")
        

        if target.is_file():
            files = [target] if target.suffix.lower() in self.supported_extensions else []
        else:
            files = self.scan_directory(target)
        
        if not files:
            return {
                'processed': 0,
                'modified': 0,
                'errors': 0,
                'files': [],
                'message': f"No supported files found in {target}"
            }
        
        results = {
            'processed': 0,
            'modified': 0,
            'errors': 0,
            'files': [],
            'dry_run': dry_run
        }
        
        print(f"🔍 Found {len(files)} supported files to process...")
        

        total_files = len(files)
        
        for i, file_path in enumerate(files, 1):
            try:

                progress_bar = "█" * (i * 20 // total_files) + "░" * (20 - (i * 20 // total_files))
                print(f"\r📄 [{progress_bar}] {i:3d}/{total_files} | {file_path.name[:30]:<30}", end="", flush=True)
                
                if dry_run:

                    suffix = file_path.suffix.lower()
                    if suffix in self.supported_extensions:
                        results['files'].append(str(file_path))
                        results['processed'] += 1
                else:

                    if self.process_file(file_path):
                        results['modified'] += 1
                    
                    results['files'].append(str(file_path))
                    results['processed'] += 1
                    
            except Exception as e:
                print(f"\n❌ Error with {file_path}: {e}")
                results['errors'] += 1
        

        print("\r" + " " * 80 + "\r", end="")
        
        if dry_run:
            results['message'] = f"Dry run: Would process {results['processed']} files"
        else:
            results['message'] = f"Processed {results['processed']} files, modified {results['modified']}"
        
        return results
