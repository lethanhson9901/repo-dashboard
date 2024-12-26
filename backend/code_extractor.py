import os
from pathlib import Path
import datetime


def extract_code_to_markdown(src_dir, output_file):
    """
    Extract all code files from the specified directory and its subdirectories,
    then write them to a single markdown file with proper formatting.
    
    Args:
        src_dir (str): Source directory path
        output_file (str): Output markdown file path
    """
    # Get absolute paths
    src_path = Path(src_dir).resolve()
    
    # List of common code file extensions to look for
    code_extensions = {
        # JavaScript/TypeScript
        '.js', '.jsx', '.ts', '.tsx',
        # Python
        '.py',
        # Web
        '.html', '.css',
        # Configuration
        '.json', '.yml', '.yaml',
        # Other
        '.md', '.txt'
    }
    
    def get_language(file_ext):
        """Determine language for markdown code block based on file extension"""
        lang_map = {
            '.js': 'javascript',
            '.jsx': 'jsx',
            '.ts': 'typescript',
            '.tsx': 'tsx',
            '.py': 'python',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.md': 'markdown',
            '.txt': 'text'
        }
        return lang_map.get(file_ext, '')

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Write header
        outfile.write(f"# Code Export from {src_path}\n\n")
        outfile.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Walk through directory
        for root, _, files in os.walk(src_path):
            for file in files:
                file_path = Path(root) / file
                
                # Check if file extension is in our list
                if file_path.suffix.lower() in code_extensions:
                    # Get relative path from src directory
                    relative_path = file_path.relative_to(src_path)
                    
                    try:
                        # Read file content
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Write to markdown with file path as header
                        outfile.write(f"\n## {relative_path}\n\n")
                        outfile.write(f"```{get_language(file_path.suffix)}\n")
                        outfile.write(content)
                        outfile.write("\n```\n")
                        
                    except Exception as e:
                        outfile.write(f"\n## {relative_path}\n\n")
                        outfile.write(f"Error reading file: {str(e)}\n")

if __name__ == "__main__":
    # Configure paths
    src_directory = "../src"
    output_markdown = "code_export.md"
    
    # Extract code
    extract_code_to_markdown(src_directory, output_markdown)
    print(f"Code extraction complete. Output written to: {output_markdown}")
