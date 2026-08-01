#!/usr/bin/env python3
"""
Blog Post Converter for Zola
Converts raw markdown blog posts to Zola format with proper front matter.

This script:
1. Reads all .md files from raw_blogs/
2. Extracts metadata from filenames and content
3. Generates proper Zola front matter
4. Writes converted files to content/
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class BlogConverter:
    def __init__(self, raw_dir: str = "raw_blogs", output_dir: str = "content"):
        self.raw_dir = Path(raw_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Tag mapping for common topics
        self.tag_mapping = {
            'openbsd': ['openbsd', 'bsd', 'unix'],
            'freebsd': ['freebsd', 'bsd', 'unix'],
            'wireguard': ['wireguard', 'vpn', 'networking'],
            'docker': ['docker', 'containers', 'devops'],
            'dns': ['dns', 'networking'],
            'dhcp': ['dhcp', 'networking'],
            'firewall': ['firewall', 'security', 'networking'],
            'iptables': ['iptables', 'firewall', 'networking'],
            'vpn': ['vpn', 'networking', 'security'],
            'vps': ['vps', 'hosting', 'cloud'],
            'ssh': ['ssh', 'security'],
            'nginx': ['nginx', 'web-server'],
            'apache': ['apache', 'web-server'],
            'lxc': ['lxc', 'containers'],
            'samba': ['samba', 'file-sharing'],
            'nat': ['nat', 'networking'],
            'vlan': ['vlan', 'networking'],
            'tunnel': ['tunnel', 'networking'],
            'debugging': ['debugging', 'troubleshooting'],
            'backup': ['backup', 'storage'],
            'ubuntu': ['ubuntu', 'linux'],
            'nixos': ['nixos', 'linux'],
        }

    def extract_title_from_filename(self, filename: str) -> str:
        """Convert filename to title case."""
        # Remove .md extension
        title = filename.replace('.md', '')
        # Replace dashes and underscores with spaces
        title = re.sub(r'[-_]', ' ', title)
        # Title case
        return title.title()

    def extract_tags_from_content(self, content: str) -> List[str]:
        """Extract relevant tags from content."""
        content_lower = content.lower()
        tags = set()
        
        # Check for tag mapping keywords
        for keyword, tag_list in self.tag_mapping.items():
            if keyword in content_lower:
                tags.update(tag_list)
        
        # Add common technical tags
        if 'tutorial' in content_lower or 'setup' in content_lower or 'guide' in content_lower:
            tags.add('tutorial')
        
        if 'debug' in content_lower or 'troubleshoot' in content_lower:
            tags.add('debugging')
        
        if 'architecture' in content_lower or 'design' in content_lower:
            tags.add('architecture')
        
        return sorted(list(tags))

    def extract_description(self, content: str) -> str:
        """Extract a description from the first paragraph."""
        # Split into paragraphs
        paragraphs = content.split('\n\n')
        
        # Find first non-empty paragraph that's not a heading
        for para in paragraphs:
            para = para.strip()
            if para and not para.startswith('#') and len(para) > 20:
                # Clean up the paragraph
                desc = re.sub(r'[#*`]', '', para)  # Remove markdown formatting
                desc = re.sub(r'\s+', ' ', desc)    # Normalize whitespace
                return desc[:200] + '...' if len(desc) > 200 else desc
        
        return "Technical blog post about networking and system administration."

    def generate_slug(self, filename: str) -> str:
        """Generate a URL-friendly slug from filename."""
        # Remove .md extension
        slug = filename.replace('.md', '')
        # Convert to lowercase
        slug = slug.lower()
        # Replace spaces and special chars with hyphens
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s-]+', '-', slug)
        return slug.strip('-')

    def create_front_matter(self, filename: str, content: str) -> str:
        """Create Zola TOML front matter."""
        title = self.extract_title_from_filename(filename)
        tags = self.extract_tags_from_content(content)
        description = self.extract_description(content)
        slug = self.generate_slug(filename)
        # Use today's date for all posts (you can modify this later)
        date = datetime.now().strftime('%Y-%m-%d')
        # Top-level TOML keys (no [taxonomies] block)
        toml_lines = []
        toml_lines.append(f'title = "{title}"')
        toml_lines.append(f'date = "{date}"')
        toml_lines.append(f'description = "{description}"')
        if tags:
            toml_lines.append(f'tags = {tags}')
        else:
            toml_lines.append('tags = []')
        toml_lines.append('categories = ["technical"]')
        return "\n".join(toml_lines)

    def is_draft(self, content: str) -> bool:
        """Check if content is marked as draft."""
        # Check for draft indicators in the first few lines
        lines = content.split('\n')[:5]
        for line in lines:
            if re.search(r'#\s*DRAFT', line, re.IGNORECASE):
                return True
        return False

    def convert_file(self, filename: str) -> None:
        """Convert a single blog post file."""
        input_path = self.raw_dir / filename
        output_path = self.output_dir / filename
        if not input_path.exists():
            print(f"Warning: {input_path} not found")
            return
        # Read content
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Skip empty files
        if not content.strip():
            print(f"Skipping empty file: {filename}")
            return
        # Skip draft files
        if self.is_draft(content):
            print(f"Skipping draft file: {filename}")
            return
        # Create front matter
        front_matter = self.create_front_matter(filename, content)
        # Combine front matter and content with TOML +++ delimiters
        zola_content = f"+++\n{front_matter}\n+++\n\n{content.strip()}\n"
        # Write to output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(zola_content)
        print(f"Converted: {filename}")

    def convert_all(self) -> None:
        """Convert all markdown files in raw_blogs directory."""
        if not self.raw_dir.exists():
            print(f"Error: {self.raw_dir} directory not found")
            return
        
        # Find all .md files
        md_files = list(self.raw_dir.glob('*.md'))
        
        if not md_files:
            print(f"No .md files found in {self.raw_dir}")
            return
        
        print(f"Found {len(md_files)} files to convert...")
        
        for file_path in md_files:
            self.convert_file(file_path.name)
        
        print(f"\nConversion complete! Files written to {self.output_dir}/")


def main():
    """Main function to run the converter."""
    converter = BlogConverter()
    converter.convert_all()


if __name__ == "__main__":
    main() 