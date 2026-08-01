# Narrative Mapping Guide

This guide helps you map your ChatGPT conversations to blog posts and create a comprehensive narrative overview.

## Quick Start

### 1. Export Your ChatGPT Conversations

1. Go to [ChatGPT](https://chatgpt.com)
2. Click on your profile (bottom left)
3. Go to "Settings" → "Data controls"
4. Click "Export" and download your data
5. You'll get a zip file (usually named something like `chatgpt-export-YYYY-MM-DD.zip`)

### 2. Run the Narrative Mapper

```bash
# Basic usage (analyzes existing posts only)
python3 narrative_mapper.py

# With ChatGPT data
python3 narrative_mapper.py path/to/your/chatgpt-export.zip
```

### 3. Review the Output

The script generates `narrative_map.md` with:

- **Chat Analysis**: All your conversations with topics, message counts, and reading times
- **Topic Analysis**: Which topics appear most frequently
- **Potential Story Combinations**: Chats that could be merged
- **Existing Posts Status**: Current blog posts with reading times and tags
- **Recommendations**: High-priority stories and potential merges

## Understanding the Output

### Chat Analysis

Each chat shows:

- **Title**: The chat title (often needs updating)
- **Messages**: Number of messages (complexity indicator)
- **Read Time**: Estimated reading time (~10 minutes is ideal)
- **Topics**: Detected topics (networking, system-admin, etc.)
- **Date**: When the chat was created

### Story Prioritization Strategy

**High-Priority Stories** (tackle first):

- 20+ messages AND 2+ topics
- Complete story arcs
- Good command examples and troubleshooting

**Medium-Priority Stories**:

- 10-20 messages
- Single topic focus
- Can be combined with related chats

**Low-Priority Stories**:

- <10 messages
- Incomplete or tangential
- Consider merging or skipping

### Story Combination Rules

**Combine when**:

- Same topic, different aspects (setup vs troubleshooting)
- Sequential parts of same journey
- <30 minutes total reading time when combined

**Separate when**:

- Different end goals
- Different time periods
- > 30 minutes total reading time

## Next Steps After Mapping

1. **Review the narrative map** and identify 3-5 high-priority stories
2. **For each story**:
   - Dictate the core narrative (5-10 minutes)
   - Add command examples and troubleshooting
   - Include screenshots and photos
   - Link to related posts
3. **Update chat titles** to reflect actual content
4. **Archive completed chats** to reduce cognitive load

## Troubleshooting

**"No JSON files found"**: The ChatGPT export format may have changed. Check the zip contents.

**"Could not parse"**: Some chats may have unusual formatting. The script will continue with others.

**Missing topics**: The script uses keyword matching. You may need to manually add topics for specialized content.

## Customization

Edit `narrative_mapper.py` to:

- Add more topic keywords
- Change reading time estimates
- Modify story combination logic
- Add new analysis features

## Example Workflow

1. **Week 1**: Export data, run mapper, review output
2. **Week 2**: Dictate 2-3 high-priority stories
3. **Week 3**: Add commands, screenshots, links
4. **Week 4**: Review and publish first batch
5. **Repeat**: Continue with medium-priority stories

This approach gives you a systematic way to tackle the "rats nest" while maintaining your voice and storytelling approach.
