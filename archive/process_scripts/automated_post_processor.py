#!/usr/bin/env python3
'''
Automated Post Processor

This script helps process posts with minimal manual intervention.
'''

import os
import re
from pathlib import Path

def process_post(post_dir):
    """Process a single post directory."""
    
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
