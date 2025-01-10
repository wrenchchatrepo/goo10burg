# goo10burg

A Python application for generating technical articles and scripts using Gemini 2.0 and Eraser.io AI diagram generation.

## Overview

goo10burg automates the creation of technical documentation by using YAML metadata files to generate customized articles and scripts. Each generated file is assigned a unique, five-character alphanumeric identifier (pk). The application leverages Gemini 2.0 for content generation and Eraser.io's API for creating technical diagrams.

## Process Flow

goo10burg uses a unified generator that processes multiple YAML configuration files:

1. **Content Generation**:
   - Reads YAML files from `/source_files/yaml/`
   - Supports markdown articles and Python scripts
   - References existing files from `/source_files/{markdown,scripts}/` for updates
   - Generates new content using Gemini API
   - Saves output to `/finished_files/{markdown,scripts}/`

2. **Diagram Generation**:
   - Processes diagram.yaml for diagram configurations
   - Uses Eraser.io API to generate diagrams
   - Links diagrams to content via pk references
   - Saves diagrams to `/finished_files/images/`

3. **Package Management**:
   - Tracks all content relationships in package.yaml
   - Maintains pk references between content and diagrams
   - Ensures content integrity across generations

The generator provides real-time progress updates and detailed error reporting during the generation process.

## Writing Style Guidelines

- All prose is written in active voice, present tense, avoiding business jargon and superfluous language; economy of words is preferred.
- Every article is on a topic that serves a purpose, built with assertions, and supported by evidence.
- When writing a script or markdown document based on an existing file, sanitize any details with obvious dummy names and any parameter values with standard placeholder names.
- Every generated script includes comments describing its functionality and purpose, along with 1 to 5 labels. Every markdown file is assigned 1 to 5 labels.
- If scripts or markdown documents require a tagline (a one-sentence high-level summary), it is included as a comment at the top of the script or the document.

## Features

- **Unified Generator**:
  - Single command to process all content types
  - Real-time progress tracking
  - Detailed error reporting
  - Automatic file relationship management

- **Content Generation**:
  - Technical articles with structured sections
  - Python scripts with documentation
  - Support for content updates using existing files
  - Customizable parameters for word count and structure

- **Diagram Integration**:
  - Automatic diagram generation via Eraser.io API
  - Bi-directional linking with content
  - Support for multiple diagrams per document

- **Metadata Management**:
  - Comprehensive YAML configuration
  - Package tracking system
  - Label and hashtag management
  - Version control support

## Prerequisites

- Python 3.8+
- Gemini 2.0 API access
- Eraser.io API token
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/wrenchchatrepo/goo10burg.git
cd goo10burg
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the `.env.template` file to create your `.env` file:
```bash
cp .env.template .env
```

2. Fill in your API keys in the `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key
ERASER_API_KEY=your_eraser_key
# ... other API keys as needed
```

⚠️ **IMPORTANT**: Never commit your `.env` file or any API keys to version control. The `.env` file is listed in `.gitignore` to prevent accidental commits.

3. Configure your YAML metadata file (see examples in `examples/`)

3. To change the LLM being used, set the `LLM` environment variable. For example, to use Claude Sonnet 3.5, set `LLM=anthropic`, or to use OpenAI, set `LLM=openai`:
```bash
export LLM=anthropic
```
```bash
export LLM=openai
```
The default LLM is Gemini.

4. To use OpenRouter, set the `LLM` environment variable to `openrouter` and set the `OPENROUTER_API_KEY` environment variable:
```bash
export LLM=openrouter
export OPENROUTER_API_KEY=your_openrouter_api_key
```

5. To use a local LLM with LM Studio, set the `LLM` environment variable to `lmstudio` and set the `LMSTUDIO_API_URL` environment variable to the URL of your LM Studio server:
```bash
export LLM=lmstudio
export LMSTUDIO_API_URL=http://localhost:1234 # Replace with your LM Studio server URL
```

## Usage

### Command Line
```bash
# Activate virtual environment
source venv_gemini/bin/activate

# Set LLM to use (default is Gemini)
export LLM=gemini

# Run the generator
python -m src.generator
```

The generator will:
1. Process all YAML files in source_files/yaml/
2. Generate new content and diagrams
3. Show progress for each file
4. Update package tracking

## YAML Configuration Fields

These are the fields by YAML config file:

### script:
- pk
- type
- language
- new_filename
- existing_filename
- update_date
- version
- description
- author
- objective
- input
- process
- output
- number_of_diagrams
- diagram_prompt_1
- tagline_required
- old_filepath
- new_filepath
- labels
- diagram_1_pk
- zipfile

### markdown:
- pk
- type
- new_filename
- existing_filename
- update_date
- version
- description
- author
- number_assertions
- assertion_1_sentence
- assertion_2_sentence
- paragraph_per_assertions
- intro_paragraph
- concluding_paragraph
- approx_words_per_paragraphs
- total_paragraphs
- approx_total_words
- number_of_diagrams
- diagram_prompt_#
- diagram_1_pk
- tagline_required
- old_filepath
- new_filepath
- labels
- zipfile

### image:
- pk
- new_filename
- new_filepath


## Metadata Structure

### Article Metadata
```yaml
article_meta_data:
  author: dion edge
  article_title: Your Title
  article_description: Description
  # ... additional fields
```

### Script Metadata
```yaml
script_metadata:
  author: dion edge
  script_name: script_name
  script_description: Description
  # ... additional fields
```

## Project Structure
```
goo10burg/
├── finished_files/          # Generated output files
│   ├── images/             # Generated diagrams
│   ├── markdown/           # Generated markdown files
│   └── scripts/            # Generated Python scripts
├── source_files/           # Source files and configurations
│   ├── markdown/           # Source markdown files
│   ├── scripts/            # Source Python scripts
│   └── yaml/               # YAML configuration files
│       ├── diagram.yaml    # Diagram configurations
│       ├── image.yaml      # Image references
│       ├── markdown.yaml   # Markdown configurations
│       ├── package.yaml    # Package tracking
│       └── script.yaml     # Script configurations
├── src/                    # Source code
│   ├── __init__.py
│   ├── config.py          # Configuration handling
│   ├── generator.py       # Main generator
│   ├── utils/             # Utility modules
│   │   ├── eraser_api.py  # Eraser.io API client
│   │   ├── gemini_api.py  # Gemini API client
│   │   └── ...           # Other utility modules
├── tests/                 # Test files
├── .env                   # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Gemini 2.0 for content generation
- Eraser.io for diagram generation
