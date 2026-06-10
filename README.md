# Slack To Repository Workflow

A Python-based automation workflow that transforms Slack project channels into structured, searchable, and AI-ready project repositories.

The workflow exports project discussions, thread conversations, and shared files from Slack, then organizes them into a consistent repository structure while generating documentation artifacts such as timelines, project summaries, file indexes, and technical decision logs.

---

## Overview

Engineering and R&D teams often manage project communication through Slack channels. Over time, valuable project knowledge becomes scattered across messages, threads, and file attachments.

This workflow solves that problem by automatically converting Slack project channels into structured repositories that can be archived, analyzed, searched, and reused.

The generated repository becomes a centralized project knowledge base containing:

* Slack message history
* Thread discussions
* Shared project files
* Technical documentation
* Project timelines
* Technical decision records
* AI-readable project context

---

## Features

### Slack Data Export

* Export channel messages
* Export threaded discussions
* Preserve timestamps
* Support configurable date ranges
* Support private project channels

### File Collection

* Download project files from Slack
* Organize files by category
* Preserve original filenames
* Support engineering file formats

Supported categories:

* CAD Models
* Technical Drawings
* Images
* Archives
* Videos
* Other Documents

### Documentation Generation

Automatically generates:

* Project Timeline
* Project Summary
* File Index
* Technical Decisions
* Repository README

### AI-Ready Knowledge Base

Creates structured documentation suitable for:

* Knowledge management
* Project archiving
* Engineering documentation
* Future AI integrations
* Project onboarding

---

## Generated Repository Structure

```text
project-name/
│
├── slack/
│   ├── messages.json
│   └── threads.json
│
├── files/
│   ├── cad/
│   ├── drawings/
│   ├── images/
│   ├── archives/
│   ├── videos/
│   └── other/
│
├── ai_context/
│   └── file_index.md
│
├── docs/
│   ├── timeline.md
│   ├── project_summary.md
│   └── technical_decisions.md
│
└── README.md
```

---

## Workflow Architecture

```text
Slack Channel
      │
      ▼
Message Export
      │
      ▼
Thread Export
      │
      ▼
File Download
      │
      ▼
Repository Organization
      │
      ▼
Documentation Generation
      │
      ▼
AI-Ready Project Repository
```

---

## Requirements

### Python

* Python 3.10 or higher

### Dependencies

Install required packages:

```bash
pip install slack-sdk requests
```

---

## Configuration

Create a configuration file using the provided template.

### sample_config.json

```json
{
    "project_name": "sample-project",
    "channel_id": "CXXXXXXXXXX",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "token": "xoxb-your-bot-token"
}
```

### Setup

1. Copy `sample_config.json`
2. Rename it to `config.json`
3. Insert your Slack Bot Token
4. Insert your Slack Channel ID
5. Save the file

---

## Usage

Run the entire workflow:

```bash
python run_workflow.py
```

The workflow will execute the following steps:

1. Create repository structure
2. Export Slack messages
3. Export Slack threads
4. Download project files
5. Generate file index
6. Generate project timeline
7. Generate project summary
8. Generate technical decisions
9. Generate repository documentation

---

## Example Outputs

### Timeline

```text
2024-05-01
- Encoder selection discussion
- Homing sensor evaluation

2024-05-03
- Mechanical assembly review
```

### Technical Decisions

```text
Decision Candidate 1
Topic:
Encoder Index vs Homing Sensor

Discussion:
Team discussed replacing a dedicated homing sensor with encoder index feedback.
```

---

## Use Cases

### Engineering Teams

* Mechanical Engineering
* Electrical Engineering
* Robotics
* Embedded Systems
* R&D Projects

### Knowledge Management

* Project Archiving
* Team Onboarding
* Documentation Automation
* Historical Project Analysis

### AI Applications

* Retrieval-Augmented Generation (RAG)
* Knowledge Bases
* Project Intelligence Systems
* Engineering Assistants

---

## Security Considerations

Never commit the following to public repositories:

* Real Slack Tokens
* Company Data
* Exported Messages
* Downloaded Project Files
* Internal Documentation

Use `.gitignore` to exclude sensitive content.

---

## Future Improvements

Planned enhancements:

* GitHub repository creation
* Automated commit generation
* Semantic project analysis
* Component extraction
* Risk analysis generation
* AI-powered technical summaries
* Vector database integration
* Multi-channel support

---

## Technologies

* Python
* Slack SDK
* Slack Web API
* JSON
* Markdown

---

## Author

**Bedirhan Gökberk Altakhan**

Software Engineering Student

Backend Development • Automation • Knowledge Management • AI-Ready Systems

---

## License

This project is provided for educational and portfolio purposes.

---

## Incremental Updates

The workflow supports incremental updates using a local `state.json` file.

After each successful run, the latest Slack message timestamp is stored locally.

On subsequent executions, only messages and files shared after the last recorded timestamp are fetched from Slack. This reduces processing time, prevents duplicate exports, and keeps the generated repository structure synchronized with new channel activity.

### Benefits

* Faster workflow execution
* Avoids duplicate message processing
* Downloads only newly shared files
* Keeps documentation and exports up to date
* Scales better for long-running projects
