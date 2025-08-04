#!/usr/bin/env python3
"""
comms.demo - Create demo files for testing the comment removal tool

Provides functionality to create sample files with comments for testing.
"""

from pathlib import Path
from typing import Dict


def create_demo_files() -> Path:
    """Create demo files with various comment types for testing."""
    demo_dir = Path("demo_files")
    demo_dir.mkdir(exist_ok=True)
    

    demo_files = {
        'test.py': '''#!/usr/bin/env python3

"""
This is a docstring that should be preserved
"""
import requests

def process_data():

    url = "https://api.example.com"
    color = "#FF5733"
    



    
    data = {
        "comment": "This # is not a comment",
        "color": "#123ABC",
        "url": "http://test.com#anchor"
    }
    
    return data


''',
        
        'test.js': '''// Single-line comment to remove
/* Multi-line comment
   that should be removed */
   
function processData() {
    // Another comment
    const url = "https://example.com";  // URL preserved
    const color = "#FF5733";  // Color preserved
    
    /* Block comment
       spanning multiple
       lines */
    
    const obj = {
        comment: "This // is not a comment",  // But this is
        url: "http://site.com#section",  // URL preserved
        color: "#ABC123"  // Color preserved
    };
    
    return obj;
}
// End comment
''',
        
        'test.c': '''// C-style single line comment
/*
 * Multi-line C comment
 * with multiple lines
 */

#include <stdio.h>  // This include should be preserved
#define MAX_SIZE 100  // This define should be preserved

int main() {
    // Local comment to remove
    char* url = "https://example.com";  // URL preserved
    char* color = "#FF5733";  // Color preserved
    
    /* Another block comment
       to be removed */
    
    printf("Color: %s\\n", color);  // Comment removed, color preserved
    
    return 0;
}
// Final comment
''',
        
        'test.html': '''<!DOCTYPE html>
<!-- HTML comment to remove -->
<html>
<head>
    <!-- Another comment -->
    <title>Test Page</title>
    <style>
        /* CSS comment to remove */
        .color-box {
            background-color: #FF5733; /* Color preserved */
            color: #123ABC; /* Another color preserved */
        }
        /* Multi-line CSS comment
           spanning several lines */
    </style>
</head>
<body>
    <!-- Body comment -->
    <div class="color-box">
        Content with URL: https://example.com
    </div>
    <!-- Final comment -->
</body>
</html>
''',
        
        'test.css': '''/* CSS file comment */
.header {
    background-color: #FF5733; /* Color should be preserved */
    background-image: url("https://example.com/image.jpg"); /* URL preserved */
}

/* Multi-line comment
   to be removed */
   
.footer {
    color: #123ABC; /* Another color preserved */
    /* Inline comment */
    margin: 10px;
}

/* Final comment */
''',
        
        'test.sh': '''#!/bin/bash




url="https://example.com"
color="#FF5733"


function process_data() {

    echo "URL: $url"
    echo "Color: $color"
}





process_data

''',
        
        'test.sql': '''-- SQL comment to remove
/* Multi-line SQL comment
   that should be removed */

SELECT
    name,  -- Column comment
    email,  -- Another comment
    url  -- URL column
FROM users
WHERE
    color = '#FF5733'  -- Color preserved
    AND url LIKE 'https://%'  -- URL pattern preserved
    
/* Final query comment */
ORDER BY name;
-- End comment
''',
        
        'test.php': '''<?php
// PHP comment to remove

/* Multi-line PHP comment
   to be removed */

$url = "https://example.com";  // URL preserved
$color = "#FF5733";

function processData() {
    // Function comment
    global $url, $color;
    
    /* Block comment
       spanning lines */
    
    echo "URL: " . $url;  // Output comment
    echo "Color: " . $color;
}

// End of file comment
?>
'''
    }
    

    for filename, content in demo_files.items():
        file_path = demo_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    

    subdir = demo_dir / "subdirectory"
    subdir.mkdir(exist_ok=True)
    
    nested_files = {
        'nested.py': '''# Nested file comment
def nested_function():

    return "https://nested.example.com"
''',
        
        'nested.js': '''// Nested JavaScript file
function nestedFunc() {
    // Comment to remove
    const color = "#ABCDEF";  // Color preserved
    return color;
}
'''
    }
    
    for filename, content in nested_files.items():
        file_path = subdir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"📁 Demo files created in: {demo_dir.absolute()}")
    print(f"📊 Created {len(demo_files)} main files + {len(nested_files)} nested files")
    print("🚀 Run 'comms demo_files' to test comment removal")
    
    return demo_dir


def show_demo_info():
    """Show information about available demo files."""
    demo_dir = Path("demo_files")
    
    if not demo_dir.exists():
        print("❌ No demo files found. Run 'comms --demo' to create them.")
        return
    
    files = list(demo_dir.rglob('*'))
    files = [f for f in files if f.is_file()]
    
    print(f"📁 Demo directory: {demo_dir.absolute()}")
    print(f"📊 Files found: {len(files)}")
    

    by_ext = {}
    for file in files:
        ext = file.suffix
        if ext not in by_ext:
            by_ext[ext] = []
        by_ext[ext].append(file)
    
    for ext, files_list in sorted(by_ext.items()):
        print(f"   {ext}: {len(files_list)} files")


def main():
    """CLI entry point for demo functionality."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--info":
        show_demo_info()
    else:
        create_demo_files()


if __name__ == "__main__":
    main()
