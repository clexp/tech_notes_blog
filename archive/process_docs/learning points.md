# Learning Points

This file tracks new programming concepts, techniques, and libraries discovered during the Tech Blog project development.

## 2025-01-26

### Python File Processing and Metadata Extraction

**Frontmatter Parsing**: Learned to parse Zola frontmatter (TOML format) using custom parsing logic. The frontmatter uses `+++` delimiters and contains metadata like title, date, tags, and categories. Key techniques:

- String splitting to find frontmatter boundaries
- Custom key-value parsing with type detection
- Handling arrays (tags) vs strings vs other data types
- Graceful fallback when frontmatter parsing fails

**Pathlib for File System Operations**: Used `pathlib.Path` extensively for cross-platform file operations:

- `Path.rglob('*.md')` for recursive file searching
- `Path.relative_to()` for clean path display
- `Path.stem` for filename without extension
- `Path.exists()` for directory validation

**Collections.Counter for Tag Analysis**: Leveraged `Counter` from collections module for:

- Automatic frequency counting of tags
- Sorting by frequency and alphabetically
- Clean aggregation of data from multiple sources

**Error Handling in File Processing**: Implemented robust error handling:

- Try-catch blocks around file operations
- Warning messages for unparseable files
- Graceful continuation when individual files fail
- Fallback title extraction from content when frontmatter is missing

**Data Structure Design**: Created flexible data structures for blog posts:

- Dictionary-based post objects with consistent keys
- Separation of concerns between parsing and reporting
- Reusable functions for different post types (completed vs raw)

**Report Generation**: Built a comprehensive reporting system:

- Markdown formatting for readable output
- Multiple sorting strategies (by date, by title, by frequency)
- Summary statistics and counts
- Both file output and console display
