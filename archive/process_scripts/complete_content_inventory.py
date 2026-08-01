#!/usr/bin/env python3
"""
Complete Content Inventory

This script analyzes all content sources and creates a comprehensive inventory
for planning the blog post workflow.

Usage:
    python3 complete_content_inventory.py
"""

import json
import os
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import re


def analyze_perplexity_chats(perplexity_file):
    """Analyze Perplexity chat summaries."""
    if not Path(perplexity_file).exists():
        return []
    
    with open(perplexity_file, 'r') as f:
        content = f.read()
    
    # Extract topics from the content
    topics = []
    lines = content.split('\n')
    
    for line in lines:
        if line.strip() and not line.startswith('perplexity') and not line.startswith('date'):
            # Extract topic from line
            topic = line.strip()
            if len(topic) > 10:  # Filter out short lines
                topics.append(topic)
    
    return topics


def analyze_claude_chats(claude_file):
    """Analyze Claude chat summaries."""
    if not Path(claude_file).exists():
        return []
    
    with open(claude_file, 'r') as f:
        content = f.read()
    
    # Extract topics from numbered list
    topics = []
    lines = content.split('\n')
    
    for line in lines:
        if re.match(r'^\d+\.', line.strip()):
            topic = line.strip().split('.', 1)[1].strip()
            topics.append(topic)
    
    return topics


def analyze_chatgpt_conversations(conversations_file):
    """Analyze ChatGPT conversations.json if available."""
    if not Path(conversations_file).exists():
        return []
    
    try:
        with open(conversations_file, 'r') as f:
            data = json.load(f)
        
        # Extract conversation titles/topics
        topics = []
        if isinstance(data, list):
            for conv in data:
                if 'title' in conv:
                    topics.append(conv['title'])
        elif isinstance(data, dict) and 'conversations' in data:
            for conv in data['conversations']:
                if 'title' in conv:
                    topics.append(conv['title'])
        
        return topics
    except Exception as e:
        print(f"Error parsing conversations.json: {e}")
        return []


def analyze_existing_posts(content_dir, raw_dir):
    """Analyze existing blog posts."""
    posts = {
        'finished': [],
        'raw': []
    }
    
    # Analyze finished posts
    if content_dir.exists():
        for md_file in content_dir.rglob('*.md'):
            if md_file.name not in ['_index.md', 'tags.md']:
                posts['finished'].append({
                    'title': md_file.stem,
                    'path': str(md_file.relative_to(content_dir)),
                    'size': md_file.stat().st_size
                })
    
    # Analyze raw posts
    if raw_dir.exists():
        for md_file in raw_dir.glob('*.md'):
            posts['raw'].append({
                'title': md_file.stem,
                'path': str(md_file),
                'size': md_file.stat().st_size
            })
    
    return posts


def generate_content_inventory():
    """Generate comprehensive content inventory."""
    
    print("🔍 Analyzing all content sources...")
    
    # Analyze different sources
    perplexity_topics = analyze_perplexity_chats('perplexity_chats.md')
    claude_topics = analyze_claude_chats('claude_chats.md')
    chatgpt_topics = analyze_chatgpt_conversations('conversations.json')
    
    # Analyze existing posts
    posts = analyze_existing_posts(Path('content'), Path('raw_blogs'))
    
    # Generate inventory report
    report = []
    report.append("# Complete Content Inventory")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Summary statistics
    report.append("## Summary Statistics")
    report.append(f"- **Perplexity Chats**: {len(perplexity_topics)}")
    report.append(f"- **Claude Chats**: {len(claude_topics)}")
    report.append(f"- **ChatGPT Topics**: {len(chatgpt_topics)}")
    report.append(f"- **Finished Posts**: {len(posts['finished'])}")
    report.append(f"- **Raw Posts**: {len(posts['raw'])}")
    report.append(f"- **Total Content Sources**: {len(perplexity_topics) + len(claude_topics) + len(chatgpt_topics) + len(posts['finished']) + len(posts['raw'])}")
    report.append("")
    
    # Perplexity topics
    report.append("## Perplexity Chat Topics")
    for i, topic in enumerate(perplexity_topics, 1):
        report.append(f"{i:2d}. {topic}")
    report.append("")
    
    # Claude topics
    report.append("## Claude Chat Topics")
    for i, topic in enumerate(claude_topics, 1):
        report.append(f"{i:2d}. {topic}")
    report.append("")
    
    # ChatGPT topics
    report.append("## ChatGPT Topics")
    for i, topic in enumerate(chatgpt_topics, 1):
        report.append(f"{i:2d}. {topic}")
    report.append("")
    
    # Existing posts
    report.append("## Existing Posts")
    report.append("### Finished Posts")
    for post in posts['finished']:
        report.append(f"- **{post['title']}** ({post['size']} bytes)")
    report.append("")
    
    report.append("### Raw Posts")
    for post in posts['raw']:
        report.append(f"- **{post['title']}** ({post['size']} bytes)")
    report.append("")
    
    # Content overlap analysis
    report.append("## Content Overlap Analysis")
    all_topics = perplexity_topics + claude_topics + chatgpt_topics
    topic_counter = Counter(all_topics)
    
    report.append("### Most Common Topics")
    for topic, count in topic_counter.most_common(10):
        report.append(f"- **{topic}**: {count} mentions")
    report.append("")
    
    # Recommendations
    report.append("## Recommendations")
    report.append("")
    report.append("### High-Priority Content")
    report.append("1. **Technical Tutorials**: Perplexity chats with step-by-step solutions")
    report.append("2. **Learning Journeys**: Claude chats with decision-making processes")
    report.append("3. **Existing Posts**: Need dictation and image integration")
    report.append("")
    
    report.append("### Content Processing Strategy")
    report.append("1. **Start with existing posts** - add dictation and images")
    report.append("2. **Extract command examples** from Perplexity chats")
    report.append("3. **Use Claude chats** for narrative structure")
    report.append("4. **Process ChatGPT conversations** for technical details")
    report.append("")
    
    report.append("### Next Steps")
    report.append("1. Choose 3-5 existing posts for immediate processing")
    report.append("2. Extract command examples from relevant Perplexity chats")
    report.append("3. Use Claude chat insights for narrative structure")
    report.append("4. Create post templates with binary state tracking")
    
    return "\n".join(report)


def main():
    """Main function to generate content inventory."""
    print("📊 Generating complete content inventory...")
    
    inventory = generate_content_inventory()
    
    # Save to file
    with open('complete_content_inventory.md', 'w') as f:
        f.write(inventory)
    
    print("✅ Complete content inventory saved to: complete_content_inventory.md")
    print("\n" + "="*50)
    print(inventory)


if __name__ == "__main__":
    main()
