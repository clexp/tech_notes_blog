#!/usr/bin/env python3
"""
Blog Post List Generator

This script generates three lists from the Tech Blog project:
1. Completed posts (from content/ folder and subfolders)
2. Raw posts (from raw_blogs/ folder)
3. All tags used across posts

The script parses Zola frontmatter to extract titles and tags from markdown files.
"""

import os
import re
from pathlib import Path
from collections import Counter
from typing import List, Dict, Set, Tuple


def parse_frontmatter(content: str) -> Tuple[Dict[str, any], str]:
    """
    Parse Zola frontmatter from markdown content.
    
    Args:
        content: Raw markdown content
        
    Returns:
        Tuple of (frontmatter_dict, body_content)
    """
    if not content.startswith('+++'):
        return {}, content
    
    # Find the end of frontmatter
    end_marker = content.find('+++', 3)
    if end_marker == -1:
        return {}, content
    
    frontmatter_text = content[3:end_marker]
    body = content[end_marker + 3:].lstrip('\n')
    
    # Parse frontmatter (simple key-value parser)
    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            # Handle different value types
            if value.startswith('[') and value.endswith(']'):
                # Array value
                value = value[1:-1]
                if value:
                    # Split by comma and clean up
                    items = [item.strip().strip("'\"") for item in value.split(',')]
                    frontmatter[key] = items
                else:
                    frontmatter[key] = []
            elif value.startswith('"') and value.endswith('"'):
                # String value
                frontmatter[key] = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                # String value
                frontmatter[key] = value[1:-1]
            else:
                # Try to parse as other types
                if value.lower() in ['true', 'false']:
                    frontmatter[key] = value.lower() == 'true'
                elif value.isdigit():
                    frontmatter[key] = int(value)
                else:
                    frontmatter[key] = value
    
    return frontmatter, body


def extract_title_from_content(content: str, filename: str) -> str:
    """
    Extract title from content, either from frontmatter or first heading.
    
    Args:
        content: Raw markdown content
        filename: Name of the file (used as fallback)
        
    Returns:
        Extracted title
    """
    frontmatter, body = parse_frontmatter(content)
    
    # Try frontmatter title first
    if 'title' in frontmatter:
        return frontmatter['title']
    
    # Try to find first heading
    lines = body.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
        elif line.startswith('## '):
            return line[3:].strip()
    
    # Fallback to filename (without extension)
    return Path(filename).stem.replace('_', ' ').replace('-', ' ').title()


def get_completed_posts(content_dir: Path) -> List[Dict[str, any]]:
    """
    Extract completed posts from content directory and subdirectories.
    
    Args:
        content_dir: Path to content directory
        
    Returns:
        List of post dictionaries with title, path, and tags
    """
    posts = []
    
    for md_file in content_dir.rglob('*.md'):
        # Skip index files and special files
        if md_file.name in ['_index.md', 'tags.md']:
            continue
            
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter, _ = parse_frontmatter(content)
            title = frontmatter.get('title', extract_title_from_content(content, md_file.name))
            tags = frontmatter.get('tags', [])
            
            # Get relative path for display
            rel_path = md_file.relative_to(content_dir)
            
            posts.append({
                'title': title,
                'path': str(rel_path),
                'tags': tags,
                'date': frontmatter.get('date', 'No date')
            })
            
        except Exception as e:
            print(f"Warning: Could not parse {md_file}: {e}")
            continue
    
    return posts


def get_raw_posts(raw_blogs_dir: Path) -> List[Dict[str, any]]:
    """
    Extract raw posts from raw_blogs directory.
    
    Args:
        raw_blogs_dir: Path to raw_blogs directory
        
    Returns:
        List of post dictionaries with title and path
    """
    posts = []
    
    for md_file in raw_blogs_dir.glob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter, _ = parse_frontmatter(content)
            title = frontmatter.get('title', extract_title_from_content(content, md_file.name))
            tags = frontmatter.get('tags', [])
            
            posts.append({
                'title': title,
                'path': md_file.name,
                'tags': tags,
                'date': frontmatter.get('date', 'No date')
            })
            
        except Exception as e:
            print(f"Warning: Could not parse {md_file}: {e}")
            continue
    
    return posts


def collect_all_tags(posts: List[Dict[str, any]]) -> Counter:
    """
    Collect all tags from posts and count their frequency.
    
    Args:
        posts: List of post dictionaries
        
    Returns:
        Counter object with tag frequencies
    """
    all_tags = []
    for post in posts:
        all_tags.extend(post.get('tags', []))
    return Counter(all_tags)


def generate_report(completed_posts: List[Dict[str, any]], 
                   raw_posts: List[Dict[str, any]], 
                   tag_counter: Counter) -> str:
    """
    Generate a formatted report with all the lists.
    
    Args:
        completed_posts: List of completed posts
        raw_posts: List of raw posts
        tag_counter: Counter of all tags
        
    Returns:
        Formatted report string
    """
    report = []
    report.append("# Blog Post Lists Report")
    report.append(f"Generated on: {os.popen('date').read().strip()}")
    report.append("")
    
    # Completed Posts Section
    report.append("## Completed Posts")
    report.append(f"Total: {len(completed_posts)} posts")
    report.append("")
    
    if completed_posts:
        # Sort by date if available, otherwise by title
        sorted_posts = sorted(completed_posts, key=lambda x: (x.get('date', ''), x['title']))
        
        for i, post in enumerate(sorted_posts, 1):
            report.append(f"{i:2d}. **{post['title']}**")
            report.append(f"    Path: `{post['path']}`")
            if post.get('date') and post['date'] != 'No date':
                report.append(f"    Date: {post['date']}")
            if post.get('tags'):
                report.append(f"    Tags: {', '.join(post['tags'])}")
            report.append("")
    else:
        report.append("No completed posts found.")
        report.append("")
    
    # Raw Posts Section
    report.append("## Raw Posts (Unprocessed)")
    report.append(f"Total: {len(raw_posts)} posts")
    report.append("")
    
    if raw_posts:
        # Sort by title
        sorted_raw = sorted(raw_posts, key=lambda x: x['title'])
        
        for i, post in enumerate(sorted_raw, 1):
            report.append(f"{i:2d}. **{post['title']}**")
            report.append(f"    File: `{post['path']}`")
            if post.get('date') and post['date'] != 'No date':
                report.append(f"    Date: {post['date']}")
            if post.get('tags'):
                report.append(f"    Tags: {', '.join(post['tags'])}")
            report.append("")
    else:
        report.append("No raw posts found.")
        report.append("")
    
    # Tags Section
    report.append("## All Tags Used")
    report.append(f"Total unique tags: {len(tag_counter)}")
    report.append("")
    
    if tag_counter:
        # Sort by frequency (descending), then alphabetically
        sorted_tags = sorted(tag_counter.items(), key=lambda x: (-x[1], x[0]))
        
        report.append("### By Frequency")
        for tag, count in sorted_tags:
            report.append(f"- **{tag}**: {count} posts")
        report.append("")
        
        # Alphabetical list
        report.append("### Alphabetical")
        for tag, count in sorted(sorted_tags, key=lambda x: x[0]):
            report.append(f"- **{tag}**: {count} posts")
    else:
        report.append("No tags found.")
    
    return "\n".join(report)


def main():
    """Main function to generate the blog post lists."""
    # Get the project root directory
    script_dir = Path(__file__).parent
    content_dir = script_dir / 'content'
    raw_blogs_dir = script_dir / 'raw_blogs'
    
    print("🔍 Analyzing blog structure...")
    
    # Check if directories exist
    if not content_dir.exists():
        print(f"❌ Content directory not found: {content_dir}")
        return
    
    if not raw_blogs_dir.exists():
        print(f"❌ Raw blogs directory not found: {raw_blogs_dir}")
        return
    
    # Extract posts
    print("📝 Extracting completed posts...")
    completed_posts = get_completed_posts(content_dir)
    
    print("📄 Extracting raw posts...")
    raw_posts = get_raw_posts(raw_blogs_dir)
    
    print("🏷️  Collecting tags...")
    all_posts = completed_posts + raw_posts
    tag_counter = collect_all_tags(all_posts)
    
    # Generate report
    print("📊 Generating report...")
    report = generate_report(completed_posts, raw_posts, tag_counter)
    
    # Write to file
    output_file = script_dir / 'blog_post_lists.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Report generated: {output_file}")
    print(f"📈 Summary:")
    print(f"   - Completed posts: {len(completed_posts)}")
    print(f"   - Raw posts: {len(raw_posts)}")
    print(f"   - Unique tags: {len(tag_counter)}")
    
    # Also print to console
    print("\n" + "="*50)
    print(report)


if __name__ == "__main__":
    main()
