# Narrative Arc Framework Template

## For ChatGPT: Generating Post Frameworks

Use this template when asking ChatGPT to create narrative arc frameworks from your conversation summaries.

### Prompt Template

```
I need you to create a narrative arc framework for a blog post based on this conversation summary.

Please structure it as follows:

## [Arc Title]

### The Story
- **Initial Problem**: [What started this journey?]
- **The Journey**: [Key discoveries, detours, errors, learning moments]
- **The Resolution**: [What was learned, what worked, what didn't]

### Technical Content
- **Commands Used**: [List key commands with context]
- **Errors Encountered**: [Common mistakes and their solutions]
- **Troubleshooting Steps**: [Systematic debugging approach]
- **Performance Results**: [Measured outcomes, benchmarks]

### Visual Elements Needed
- [ ] Screenshot: [Description of what to capture]
- [ ] Diagram: [Network topology, process flow, etc.]
- [ ] Command Output: [Example of successful command]
- [ ] Error Output: [Example of common error and fix]

### Links to Related Content
- **Prerequisites**: [What readers should know first]
- **Follow-up Posts**: [Related stories that come next]
- **Reference Material**: [External links, documentation]

### Dictation Notes
- **Key Points to Emphasize**: [What makes this story compelling]
- **Personal Insights**: [What you learned about yourself/process]
- **Mistakes Worth Sharing**: [Humorous or educational failures]

Please create this framework for: [INSERT CONVERSATION SUMMARY HERE]
```

### Example Output Structure

```
## The Cable Detective: Why My Gigabit Wasn't Gigabit

### The Story
- **Initial Problem**: Network transfers were unexpectedly slow (5-9 MB/s) despite gigabit hardware
- **The Journey**: Suspected encryption overhead, tested with iperf3, discovered cable termination issues
- **The Resolution**: Found crossed pair in blue-tipped cable, achieved full 940 Mb/s after re-termination

### Technical Content
- **Commands Used**:
  - `iperf3 -s` (server)
  - `iperf3 -c 192.168.1.100` (client)
  - `ifconfig` (interface status)
  - `ethtool` (link negotiation)
- **Errors Encountered**:
  - Link negotiating at 100 Mb/s instead of 1000 Mb/s
  - "Operation not supported" with some ethtool commands
- **Troubleshooting Steps**:
  1. Verify physical connection
  2. Check link negotiation
  3. Test with known good cable
  4. Inspect cable termination
- **Performance Results**:
  - Good cables: 940+ Mb/s
  - Bad cable: 94 Mb/s (exactly 10x slower)

### Visual Elements Needed
- [ ] Screenshot: iperf3 output showing 940+ Mb/s
- [ ] Diagram: Cable pinout showing correct vs incorrect termination
- [ ] Command Output: `ethtool` showing link negotiation
- [ ] Error Output: Link speed showing 100 Mb/s instead of 1000 Mb/s

### Links to Related Content
- **Prerequisites**: Basic networking knowledge, cable termination tools
- **Follow-up Posts**: Network rebuild planning, switch selection
- **Reference Material**: Ethernet cable standards, iperf3 documentation

### Dictation Notes
- **Key Points to Emphasize**: How systematic testing revealed the real problem
- **Personal Insights**: Learned to trust measurements over assumptions
- **Mistakes Worth Sharing**: Initially blamed encryption when it was physical layer
```

### Usage Instructions

1. **Copy the prompt template** above
2. **Insert the conversation summary** you want to convert
3. **Send to ChatGPT** with the prompt
4. **Review the framework** and adjust as needed
5. **Use for dictation** - the framework gives you structure without being too prescriptive

This approach gives you:

- **Consistent structure** across all posts
- **Technical depth** with commands and troubleshooting
- **Visual planning** for screenshots and diagrams
- **Narrative flow** that maintains your voice
- **Systematic approach** to tackle the backlog
