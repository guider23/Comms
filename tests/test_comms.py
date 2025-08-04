"""
Test cases for the comment removal tool.

This module contains basic tests to verify the functionality
of the comment removal tool across different file types.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from comms.core import CommentRemover


class TestCommentRemoval(unittest.TestCase):
    """Test cases for comment removal functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = Path.cwd()
        os.chdir(self.test_dir)
        self.remover = CommentRemover()
    
    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_python_comments(self):
        """Test Python comment removal."""
        python_code = '''# This is a comment
def hello():
    """This docstring should remain"""
    name = "John"
    url = "https://example.com"
    color = "#FF5733"
    return name
'''
        
        expected = '''
def hello():
    """This docstring should remain"""
    name = "John"
    url = "https://example.com"
    color = "#FF5733"
    return name
'''
        
        result = self.remover.remove_python_comments(python_code)

        self.assertNotIn('# This is a comment', result)
        self.assertNotIn('# This comment should go', result)

        self.assertIn('"""This docstring should remain"""', result)

        self.assertIn('# URL should be preserved', result)
        self.assertIn('# Color should be preserved', result)
    
    def test_javascript_comments(self):
        """Test JavaScript comment removal."""
        js_code = '''// This is a comment
function hello() {
    /* Block comment */
    const name = "John";  // This comment should go
    const url = "https://example.com";  // URL should be preserved
    const color = "#FF5733";  // Color should be preserved
    return name;
}
'''
        
        result = self.remover.remove_c_style_comments(js_code)

        self.assertNotIn('// This is a comment', result)
        self.assertNotIn('/* Block comment */', result)
        self.assertNotIn('// This comment should go', result)

        self.assertIn('// URL should be preserved', result)
        self.assertIn('// Color should be preserved', result)
    
    def test_html_comments(self):
        """Test HTML comment removal."""
        html_code = '''<!DOCTYPE html>
<!-- This comment should be removed -->
<html>
<head>
    <!-- Another comment -->
    <title>Test</title>
</head>
<body>
    <div>Content with URL: https://example.com</div>
    <!-- Final comment -->
</body>
</html>
'''
        
        result = self.remover.remove_html_comments(html_code)

        self.assertNotIn('<!-- This comment should be removed -->', result)
        self.assertNotIn('<!-- Another comment -->', result)
        self.assertNotIn('<!-- Final comment -->', result)

        self.assertIn('<title>Test</title>', result)
        self.assertIn('https://example.com', result)
    
    def test_file_processing(self):
        """Test processing a file."""

        test_file = self.test_dir / "test.py"
        test_file.write_text('''# Comment to remove
def test():
    return "https://example.com"
''')
        

        result = self.remover.process_file(test_file)
        self.assertTrue(result)
        

        processed_content = test_file.read_text()
        self.assertNotIn('# Comment to remove', processed_content)
        self.assertIn('# URL preserved', processed_content)
    
    def test_preserve_patterns(self):
        """Test that preserve patterns work correctly."""

        custom_patterns = [r'#TODO.*', r'#FIXME.*']
        remover = CommentRemover(preserve_patterns=custom_patterns)
        
        python_code = '''# Regular comment

def test():
    pass

'''
        
        result = remover.remove_python_comments(python_code)

        self.assertNotIn('# Regular comment', result)
        self.assertNotIn('# Another comment', result)

        self.assertIn('#TODO: This should be preserved', result)
        self.assertIn('# FIXME: This should also be preserved', result)


class TestBackupFunctionality(unittest.TestCase):
    """Test backup and restore functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = Path.cwd()
        os.chdir(self.test_dir)
        self.remover = CommentRemover()
    
    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_backup_creation(self):
        """Test that backups are created correctly."""

        test_file = self.test_dir / "test.py"
        original_content = '''# Comment
def test():
    pass
'''
        test_file.write_text(original_content)
        

        result = self.remover.create_backup(test_file)
        self.assertTrue(result)
        

        backup_file = self.test_dir / '.backup' / 'test.py'
        self.assertTrue(backup_file.exists())
        

        backup_content = backup_file.read_text()
        self.assertEqual(backup_content, original_content)


if __name__ == '__main__':
    unittest.main()
