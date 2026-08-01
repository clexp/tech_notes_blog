#!/usr/bin/env python3
"""
Post Reorganization Script

This script consolidates all blog posts into a single work_in_progress folder
for comprehensive analysis and planning.

Usage:
    python3 reorganize_posts.py
"""

import os
import shutil
from pathlib import Path
from datetime import datetime


def create_directory_structure(base_path):
    """Create the new directory structure."""
    directories = [
        "work_in_progress",
        "work_in_progress/finished_posts",
        "work_in_progress/raw_posts", 
        "work_in_progress/chatgpt_proposed",
        "work_in_progress/narrative_arcs",
        "assets",
        "assets/images",
        "assets/screenshots",
        "assets/diagrams"
    ]
    
    for directory in directories:
        Path(base_path / directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")


def move_finished_posts(content_dir, work_dir):
    """Move posts from content/ to work_in_progress/finished_posts/"""
    finished_dir = work_dir / "finished_posts"
    
    # Move all .md files except index files
    moved_count = 0
    for md_file in content_dir.rglob("*.md"):
        if md_file.name in ['_index.md', 'tags.md']:
            continue
            
        # Preserve directory structure
        rel_path = md_file.relative_to(content_dir)
        dest_path = finished_dir / rel_path
        
        # Create parent directories
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Move file
        shutil.move(str(md_file), str(dest_path))
        print(f"📄 Moved: {rel_path}")
        moved_count += 1
    
    print(f"✅ Moved {moved_count} finished posts")


def move_raw_posts(raw_dir, work_dir):
    """Move posts from raw_blogs/ to work_in_progress/raw_posts/"""
    raw_posts_dir = work_dir / "raw_posts"
    
    moved_count = 0
    for md_file in raw_dir.glob("*.md"):
        dest_path = raw_posts_dir / md_file.name
        shutil.move(str(md_file), str(dest_path))
        print(f"📄 Moved: {md_file.name}")
        moved_count += 1
    
    print(f"✅ Moved {moved_count} raw posts")


def move_chatgpt_chats(chat_dir, work_dir):
    """Move ChatGPT chats to work_in_progress/chatgpt_proposed/"""
    chatgpt_dir = work_dir / "chatgpt_proposed"
    
    moved_count = 0
    for md_file in chat_dir.rglob("*.md"):
        # Skip the prompt.md file
        if md_file.name == "prompt.md":
            continue
            
        dest_path = chatgpt_dir / md_file.name
        shutil.move(str(md_file), str(dest_path))
        print(f"📄 Moved: {md_file.name}")
        moved_count += 1
    
    print(f"✅ Moved {moved_count} ChatGPT chat summaries")


def create_analysis_files(work_dir):
    """Create analysis files for the consolidated posts."""
    
    # Create post inventory
    inventory_file = work_dir / "post_inventory.md"
    with open(inventory_file, 'w') as f:
        f.write("# Post Inventory\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Count posts in each category
        finished_count = len(list((work_dir / "finished_posts").rglob("*.md")))
        raw_count = len(list((work_dir / "raw_posts").glob("*.md")))
        chatgpt_count = len(list((work_dir / "chatgpt_proposed").glob("*.md")))
        
        f.write(f"## Summary\n")
        f.write(f"- **Finished Posts**: {finished_count}\n")
        f.write(f"- **Raw Posts**: {raw_count}\n")
        f.write(f"- **ChatGPT Proposed**: {chatgpt_count}\n")
        f.write(f"- **Total**: {finished_count + raw_count + chatgpt_count}\n\n")
        
        f.write("## Next Steps\n")
        f.write("1. Review all posts for content overlap\n")
        f.write("2. Identify which posts can be merged\n")
        f.write("3. Determine which posts to remove\n")
        f.write("4. Sanitize naming conventions\n")
        f.write("5. Create narrative arc frameworks\n")
    
    print(f"✅ Created: post_inventory.md")
    
    # Create merge analysis template
    merge_file = work_dir / "merge_analysis.md"
    with open(merge_file, 'w') as f:
        f.write("# Post Merge Analysis\n\n")
        f.write("## Potential Merges\n\n")
        f.write("### Network Rebuild Series\n")
        f.write("- [ ] Post 1: [Title]\n")
        f.write("- [ ] Post 2: [Title]\n")
        f.write("- [ ] Merge: [Combined Title]\n\n")
        f.write("### Server Build Series\n")
        f.write("- [ ] Post 1: [Title]\n")
        f.write("- [ ] Post 2: [Title]\n")
        f.write("- [ ] Merge: [Combined Title]\n\n")
        f.write("### Troubleshooting Series\n")
        f.write("- [ ] Post 1: [Title]\n")
        f.write("- [ ] Post 2: [Title]\n")
        f.write("- [ ] Merge: [Combined Title]\n\n")
        f.write("## Posts to Remove\n\n")
        f.write("- [ ] [Reason for removal]\n\n")
        f.write("## Naming Sanitization\n\n")
        f.write("- [ ] [Current name] → [New name]\n")
    
    print(f"✅ Created: merge_analysis.md")


def main():
    """Main reorganization function."""
    base_path = Path("/Users/clexp/Tech_Blog")
    
    print("🔄 Starting post reorganization...")
    print(f"📁 Working in: {base_path}")
    
    # Create new directory structure
    print("\n📁 Creating directory structure...")
    create_directory_structure(base_path)
    
    # Move finished posts
    print("\n📄 Moving finished posts...")
    content_dir = base_path / "content"
    if content_dir.exists():
        move_finished_posts(content_dir, base_path / "work_in_progress")
    else:
        print("⚠️  Content directory not found")
    
    # Move raw posts
    print("\n📄 Moving raw posts...")
    raw_dir = base_path / "raw_blogs"
    if raw_dir.exists():
        move_raw_posts(raw_dir, base_path / "work_in_progress")
    else:
        print("⚠️  Raw blogs directory not found")
    
    # Move ChatGPT chats
    print("\n📄 Moving ChatGPT chats...")
    chat_dir = base_path / "ChatGPT chats"
    if chat_dir.exists():
        move_chatgpt_chats(chat_dir, base_path / "work_in_progress")
    else:
        print("⚠️  ChatGPT chats directory not found")
    
    # Create analysis files
    print("\n📊 Creating analysis files...")
    create_analysis_files(base_path / "work_in_progress")
    
    print("\n✅ Reorganization complete!")
    print("\n📋 Next steps:")
    print("1. Review work_in_progress/post_inventory.md")
    print("2. Use work_in_progress/merge_analysis.md to plan merges")
    print("3. Get remaining ChatGPT summaries")
    print("4. Create narrative arc frameworks")
    
    # Ask about removing old directories
    print("\n🗑️  Old directories (content/, raw_blogs/, ChatGPT chats/) are now empty.")
    print("   You can remove them when ready with:")
    print("   rm -rf content/ raw_blogs/ 'ChatGPT chats/'")


if __name__ == "__main__":
    main()
