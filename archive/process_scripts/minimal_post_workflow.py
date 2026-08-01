#!/usr/bin/env python3
"""
Minimal Post Workflow

This script automates the creation of blog posts from existing content
with minimal manual intervention.

Usage:
    python3 minimal_post_workflow.py [post_title]
"""

import os
import re
from pathlib import Path
from datetime import datetime
import argparse


def create_post_template(title, content_sources):
    """Create a post template with binary state tracking."""
    
    # Convert title to slug
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
    slug = re.sub(r'\s+', '-', slug).strip('-')
    
    # Create post directory
    post_dir = Path(f"work_in_progress/posts/{slug}")
    post_dir.mkdir(parents=True, exist_ok=True)
    
    # Create main post file
    post_file = post_dir / "index.md"
    
    frontmatter = f"""+++
title = "{title}"
date = "{datetime.now().strftime('%Y-%m-%d')}"
draft = true
tags = ["work-in-progress"]
[workflow]
dictation = "awaiting"
commands = "awaiting"
images = "awaiting"
links = "awaiting"
source_material = "ready"
llm_weaving = "awaiting"
editorial_signoff = "awaiting"
+++

# {title}

## The Story
*[Your dictation will go here]*

## Technical Content
*[Command examples and troubleshooting will go here]*

## Visual Elements
*[Screenshots and diagrams will go here]*

## Links to Related Content
*[Cross-references will go here]*
"""
    
    with open(post_file, 'w') as f:
        f.write(frontmatter)
    
    # Create workflow status file
    status_file = post_dir / "workflow_status.md"
    status_content = f"""# Workflow Status: {title}

## Binary States
- [ ] Dictation complete
- [ ] Commands+Output awaiting
- [ ] Images awaiting
- [ ] Cross-links awaiting
- [ ] Source material ready
- [ ] LLM weaving awaiting
- [ ] Editorial sign-off awaiting

## Progress: 1/7 (14%)

## Next Action
Add dictation covering the core story

## Source Material
{content_sources}

## Notes
- Start with dictation (5-10 minutes)
- Add command examples from source material
- Include screenshots for visual appeal
- Link to related posts when ready
"""
    
    with open(status_file, 'w') as f:
        f.write(status_content)
    
    # Create source material directory
    source_dir = post_dir / "source_material"
    source_dir.mkdir(exist_ok=True)
    
    # Create placeholder files
    (source_dir / "dictation_notes.md").write_text("# Dictation Notes\n\n*Your voice input will go here*")
    (source_dir / "command_examples.md").write_text("# Command Examples\n\n*Extract from source material*")
    (source_dir / "visual_notes.md").write_text("# Visual Elements\n\n*Screenshots and diagrams needed*")
    
    return post_dir


def extract_command_examples(content_sources):
    """Extract command examples from source material."""
    examples = []
    
    # Look for code blocks and command patterns
    code_pattern = r'```(?:bash|sh|shell)?\n(.*?)\n```'
    command_pattern = r'`([^`]+)`'
    
    for source in content_sources:
        if isinstance(source, str):
            # Extract code blocks
            code_blocks = re.findall(code_pattern, source, re.DOTALL)
            for block in code_blocks:
                examples.append(block.strip())
            
            # Extract inline commands
            commands = re.findall(command_pattern, source)
            for cmd in commands:
                if any(keyword in cmd.lower() for keyword in ['sudo', 'docker', 'zfs', 'ssh', 'ping', 'dig']):
                    examples.append(cmd)
    
    return examples


def create_automated_post_processor():
    """Create a script to automate post processing."""
    
    processor_script = """#!/usr/bin/env python3
'''
Automated Post Processor

This script helps process posts with minimal manual intervention.
'''

import os
import re
from pathlib import Path

def process_post(post_dir):
    \"\"\"Process a single post directory.\"\"\"
    
    post_dir = Path(post_dir)
    if not post_dir.exists():
        print(f"Post directory not found: {post_dir}")
        return
    
    # Check workflow status
    status_file = post_dir / "workflow_status.md"
    if not status_file.exists():
        print(f"No workflow status found: {status_file}")
        return
    
    # Read current status
    with open(status_file, 'r') as f:
        status = f.read()
    
    # Update status based on what's available
    if (post_dir / "source_material" / "dictation_notes.md").exists():
        status = re.sub(r'- \[ \] Dictation complete', '- [x] Dictation complete', status)
    
    if (post_dir / "source_material" / "command_examples.md").exists():
        status = re.sub(r'- \[ \] Commands\+Output awaiting', '- [x] Commands+Output complete', status)
    
    # Write updated status
    with open(status_file, 'w') as f:
        f.write(status)
    
    print(f"Processed: {post_dir.name}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        process_post(sys.argv[1])
    else:
        print("Usage: python3 automated_post_processor.py <post_directory>")
"""
    
    with open('automated_post_processor.py', 'w') as f:
        f.write(processor_script)
    
    # Make it executable
    os.chmod('automated_post_processor.py', 0o755)


def main():
    """Main function for minimal post workflow."""
    parser = argparse.ArgumentParser(description='Create minimal post workflow')
    parser.add_argument('post_title', help='Title of the post to create')
    parser.add_argument('--sources', nargs='+', help='Source material files')
    
    args = parser.parse_args()
    
    print(f"🚀 Creating minimal post workflow for: {args.post_title}")
    
    # Create post template
    post_dir = create_post_template(args.post_title, args.sources or [])
    
    # Create automated processor
    create_automated_post_processor()
    
    print(f"✅ Post template created: {post_dir}")
    print(f"📝 Edit: {post_dir}/index.md")
    print(f"📊 Status: {post_dir}/workflow_status.md")
    print(f"🔧 Source: {post_dir}/source_material/")
    
    print("\n📋 Next Steps:")
    print("1. Dictate the core story (5-10 minutes)")
    print("2. Add command examples from source material")
    print("3. Include screenshots for visual appeal")
    print("4. Link to related posts when ready")
    print("5. Run: python3 automated_post_processor.py <post_dir>")


if __name__ == "__main__":
    main()
