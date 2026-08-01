#!/usr/bin/env python3
"""
Narrative Mapper for Tech Blog

This script analyzes ChatGPT conversations and existing blog posts to create
a comprehensive narrative map showing story arcs, overlaps, and potential
post boundaries.

Usage:
    python3 narrative_mapper.py [path_to_chatgpt_export.zip]
"""

import json
import zipfile
import os
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional
import argparse


class ChatAnalyzer:
    """Analyzes ChatGPT conversations for narrative mapping."""
    
    def __init__(self):
        self.chats = []
        self.existing_posts = []
        self.topic_keywords = {
            'networking': ['dhcp', 'dns', 'vlan', 'nat', 'router', 'switch', 'firewall', 'wireguard', 'tailscale'],
            'system-admin': ['freebsd', 'openbsd', 'ubuntu', 'linux', 'server', 'backup', 'restore', 'zfs'],
            'hardware': ['motherboard', 'firmware', 'bios', 'hardware', 'spec', 'probook', 'server'],
            'containers': ['docker', 'lxc', 'container', 'samba', 'pihole'],
            'troubleshooting': ['debug', 'debugging', 'troubleshoot', 'error', 'fix', 'issue', 'problem'],
            'security': ['security', 'firewall', 'vpn', 'wireguard', 'ssl', 'https'],
            'web-dev': ['zola', 'css', 'sass', 'html', 'website', 'blog', 'deployment']
        }
    
    def load_chatgpt_export(self, zip_path: str) -> List[Dict]:
        """Load and parse ChatGPT export zip file."""
        chats = []
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                # Look for JSON files in the zip
                json_files = [f for f in zip_file.namelist() if f.endswith('.json')]
                
                if not json_files:
                    print("❌ No JSON files found in the export")
                    return []
                
                for json_file in json_files:
                    try:
                        with zip_file.open(json_file) as f:
                            data = json.load(f)
                            
                        # Extract chat information
                        chat_info = self._extract_chat_info(data, json_file)
                        if chat_info:
                            chats.append(chat_info)
                            
                    except Exception as e:
                        print(f"⚠️  Could not parse {json_file}: {e}")
                        continue
                        
        except Exception as e:
            print(f"❌ Could not open zip file: {e}")
            return []
        
        return chats
    
    def _extract_chat_info(self, data: Dict, filename: str) -> Optional[Dict]:
        """Extract relevant information from a ChatGPT conversation."""
        try:
            # Handle different ChatGPT export formats
            if 'conversations' in data:
                # New format
                conversations = data['conversations']
                if not conversations:
                    return None
                
                # Get the first conversation
                conv = conversations[0]
                title = conv.get('title', 'Untitled')
                messages = conv.get('mapping', {})
                
            elif 'mapping' in data:
                # Older format
                title = data.get('title', 'Untitled')
                messages = data.get('mapping', {})
            else:
                return None
            
            # Count messages and extract content
            message_count = len([m for m in messages.values() if m.get('message')])
            
            # Extract topics from message content
            topics = self._extract_topics_from_messages(messages)
            
            # Estimate reading time (rough: 200 words per minute)
            total_words = sum(len(str(m.get('message', {}).get('content', '')).split()) for m in messages.values() if m.get('message'))
            estimated_read_time = max(1, total_words // 200)
            
            return {
                'filename': filename,
                'title': title,
                'message_count': message_count,
                'topics': topics,
                'estimated_read_time': estimated_read_time,
                'total_words': total_words,
                'created_date': self._extract_date(data),
                'messages': messages
            }
            
        except Exception as e:
            print(f"⚠️  Error extracting chat info from {filename}: {e}")
            return None
    
    def _extract_topics_from_messages(self, messages: Dict) -> Set[str]:
        """Extract topics from message content."""
        topics = set()
        
        for message_data in messages.values():
            if not message_data.get('message'):
                continue
                
            content = str(message_data['message'].get('content', '')).lower()
            
            # Check against topic keywords
            for topic, keywords in self.topic_keywords.items():
                if any(keyword in content for keyword in keywords):
                    topics.add(topic)
        
        return topics
    
    def _extract_date(self, data: Dict) -> str:
        """Extract creation date from chat data."""
        # Try different date fields
        for date_field in ['create_time', 'created_at', 'timestamp']:
            if date_field in data:
                try:
                    timestamp = data[date_field]
                    if isinstance(timestamp, (int, float)):
                        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                    elif isinstance(timestamp, str):
                        return timestamp[:10]  # Take just the date part
                except:
                    continue
        
        return 'Unknown'
    
    def load_existing_posts(self, content_dir: Path) -> List[Dict]:
        """Load existing blog posts for comparison."""
        posts = []
        
        for md_file in content_dir.rglob('*.md'):
            if md_file.name in ['_index.md', 'tags.md']:
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse frontmatter
                frontmatter, body = self._parse_frontmatter(content)
                
                posts.append({
                    'title': frontmatter.get('title', md_file.stem),
                    'path': str(md_file.relative_to(content_dir)),
                    'tags': frontmatter.get('tags', []),
                    'date': frontmatter.get('date', 'No date'),
                    'word_count': len(body.split()),
                    'estimated_read_time': max(1, len(body.split()) // 200)
                })
                
            except Exception as e:
                print(f"⚠️  Could not parse {md_file}: {e}")
                continue
        
        return posts
    
    def _parse_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Simple frontmatter parser."""
        if not content.startswith('+++'):
            return {}, content
        
        end_marker = content.find('+++', 3)
        if end_marker == -1:
            return {}, content
        
        frontmatter_text = content[3:end_marker]
        body = content[end_marker + 3:].lstrip('\n')
        
        frontmatter = {}
        for line in frontmatter_text.split('\n'):
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                if value.startswith('[') and value.endswith(']'):
                    value = value[1:-1]
                    if value:
                        items = [item.strip().strip("'\"") for item in value.split(',')]
                        frontmatter[key] = items
                    else:
                        frontmatter[key] = []
                elif value.startswith('"') and value.endswith('"'):
                    frontmatter[key] = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    frontmatter[key] = value[1:-1]
                else:
                    frontmatter[key] = value
        
        return frontmatter, body
    
    def generate_narrative_map(self, chats: List[Dict], posts: List[Dict]) -> str:
        """Generate a comprehensive narrative map."""
        report = []
        report.append("# Narrative Map: ChatGPT Conversations → Blog Posts")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary statistics
        report.append("## Summary Statistics")
        report.append(f"- **Total Chats**: {len(chats)}")
        report.append(f"- **Total Messages**: {sum(c['message_count'] for c in chats)}")
        report.append(f"- **Total Words**: {sum(c['total_words'] for c in chats):,}")
        report.append(f"- **Existing Posts**: {len(posts)}")
        report.append("")
        
        # Chat analysis
        report.append("## Chat Analysis")
        report.append("")
        
        # Sort chats by message count (most complex first)
        sorted_chats = sorted(chats, key=lambda x: x['message_count'], reverse=True)
        
        for i, chat in enumerate(sorted_chats, 1):
            report.append(f"### {i}. {chat['title']}")
            report.append(f"- **File**: `{chat['filename']}`")
            report.append(f"- **Messages**: {chat['message_count']}")
            report.append(f"- **Read Time**: ~{chat['estimated_read_time']} minutes")
            report.append(f"- **Topics**: {', '.join(sorted(chat['topics'])) if chat['topics'] else 'None detected'}")
            report.append(f"- **Date**: {chat['created_date']}")
            report.append("")
        
        # Topic analysis
        report.append("## Topic Analysis")
        report.append("")
        
        all_topics = []
        for chat in chats:
            all_topics.extend(chat['topics'])
        
        topic_counter = Counter(all_topics)
        
        report.append("### Topics by Frequency")
        for topic, count in topic_counter.most_common():
            report.append(f"- **{topic}**: {count} chats")
        report.append("")
        
        # Potential story combinations
        report.append("## Potential Story Combinations")
        report.append("")
        
        # Group chats by topics
        topic_groups = defaultdict(list)
        for chat in chats:
            for topic in chat['topics']:
                topic_groups[topic].append(chat)
        
        for topic, topic_chats in topic_groups.items():
            if len(topic_chats) > 1:
                report.append(f"### {topic.title()} Stories ({len(topic_chats)} chats)")
                for chat in topic_chats:
                    report.append(f"- {chat['title']} ({chat['message_count']} messages)")
                report.append("")
        
        # Existing posts comparison
        report.append("## Existing Posts Status")
        report.append("")
        
        for post in sorted(posts, key=lambda x: x['date']):
            report.append(f"- **{post['title']}**")
            report.append(f"  - Path: `{post['path']}`")
            report.append(f"  - Read Time: ~{post['estimated_read_time']} minutes")
            report.append(f"  - Tags: {', '.join(post['tags']) if post['tags'] else 'None'}")
            report.append("")
        
        # Recommendations
        report.append("## Recommendations")
        report.append("")
        report.append("### High-Priority Stories (Most Complete)")
        high_priority = [c for c in sorted_chats if c['message_count'] >= 20 and len(c['topics']) >= 2]
        for chat in high_priority[:5]:
            report.append(f"- **{chat['title']}** ({chat['message_count']} messages, {len(chat['topics'])} topics)")
        report.append("")
        
        report.append("### Potential Merges")
        for topic, topic_chats in topic_groups.items():
            if len(topic_chats) >= 3:
                report.append(f"- **{topic.title()}**: {len(topic_chats)} chats could be combined")
        report.append("")
        
        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description='Generate narrative map from ChatGPT conversations')
    parser.add_argument('chatgpt_zip', nargs='?', help='Path to ChatGPT export zip file')
    parser.add_argument('--content-dir', default='content', help='Path to content directory')
    
    args = parser.parse_args()
    
    analyzer = ChatAnalyzer()
    
    # Load existing posts
    content_dir = Path(args.content_dir)
    if not content_dir.exists():
        print(f"❌ Content directory not found: {content_dir}")
        return
    
    print("📝 Loading existing posts...")
    posts = analyzer.load_existing_posts(content_dir)
    print(f"✅ Loaded {len(posts)} existing posts")
    
    # Load ChatGPT conversations
    chats = []
    if args.chatgpt_zip and Path(args.chatgpt_zip).exists():
        print("📥 Loading ChatGPT conversations...")
        chats = analyzer.load_chatgpt_export(args.chatgpt_zip)
        print(f"✅ Loaded {len(chats)} conversations")
    else:
        print("⚠️  No ChatGPT export provided or file not found")
        print("   Usage: python3 narrative_mapper.py path/to/chatgpt_export.zip")
    
    # Generate narrative map
    print("🗺️  Generating narrative map...")
    narrative_map = analyzer.generate_narrative_map(chats, posts)
    
    # Save to file
    output_file = Path('narrative_map.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(narrative_map)
    
    print(f"✅ Narrative map saved to: {output_file}")
    print("\n" + "="*50)
    print(narrative_map)


if __name__ == "__main__":
    main()
