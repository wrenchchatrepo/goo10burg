---
author: dion@wrench.chat
tagline_required: 1
update_date: 1/9/2025
version: 1
---

# Looker Instance Backup and Deployment Tools

## Description
This repository contains two Python scripts for managing Looker instance content:
1. `get_Looker.py`: Reads your Looker instance metadata and writes it to JSON files
2. `deploy_looker.py`: Deploys content back to your Looker instance

## Objective
To provide a reliable way to back up and restore your Looker instance content and metadata, enabling version control and safe deployment of changes.

## Input Parameters
- Looker privileges and credentials (client ID, client secret)
- Looker instance URL
- Access to Looker API endpoints

## Output Parameters
- JSON files containing Looker metadata including:
  - Projects and their configurations
  - Git branch information
  - LookML models
  - Folders structure
  - Looks and dashboards
  - Other instance-specific metadata

## Usage
These scripts are particularly useful when you need to:
1. Back up your Looker instance for disaster recovery
2. Version control your Looker content
3. Migrate content between Looker instances
4. Make bulk changes to Looker content programmatically
5. Audit your Looker instance configuration

The workflow typically involves:
1. Using `get_Looker.py` to extract and save instance metadata as JSON
2. Making any necessary modifications to the JSON files
3. Using `deploy_looker.py` to apply changes back to your Looker instance

## Labels
#devops
#looker
#platform
#readme
